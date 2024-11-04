import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTextEdit, QPushButton
from PyQt6.QtCore import QProcess


class TerminalApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Wpisz komendę...")
        layout.addWidget(self.command_input)

        self.run_button = QPushButton("Uruchom", self)
        layout.addWidget(self.run_button)
        self.run_button.clicked.connect(self.run_command)

        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_stdout)
        self.process.readyReadStandardError.connect(self.read_stderr)

        self.setLayout(layout)
        self.setWindowTitle("Terminal PyQt")
        self.resize(600, 400)

    def run_command(self):
        command = self.command_input.text()
        print(f"Command: {command}")  # Wyświetlenie komendy w konsoli
        if command.strip():
            self.output_area.append(f"> {command}")
            self.process.start("cmd.exe", ["/c", command])

    def read_stdout(self):
        output = self.process.readAllStandardOutput().data().decode()
        print(output)  # Wyświetlenie wyniku w konsoli
        self.output_area.append(output)

    def read_stderr(self):
        error = self.process.readAllStandardError().data().decode()
        print(error)  # Wyświetlenie błędów w konsoli
        self.output_area.append(error)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TerminalApp()
    window.show()
    sys.exit(app.exec())
