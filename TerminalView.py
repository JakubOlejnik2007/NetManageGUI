from PyQt6.QtCore import QProcess, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit


class TerminalView(QWidget):
    output_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        layout = QVBoxLayout()
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)
        self.setLayout(layout)
        self.setWindowTitle("Terminal PyQt")
        self.resize(600, 400)
    def run_command(self, command: str):
        print(f"Command: {command}")
        if command.strip():
            self.output_area.append(f"> {command}")
            self.process.start(command)
    def read_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        print(output)
        self.output_area.append(output)
        self.output_received.emit(output)
    def read_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        print(error)
        self.output_area.append(error)
        self.output_received.emit(error)

    def disconnect_signal(self):
        try:
            self.output_received.disconnect()
        except TypeError:
            print("Rozłączenie się nie powiodło.")