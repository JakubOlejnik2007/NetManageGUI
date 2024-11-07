from PyQt6 import QtCore
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, QStyle

from TerminalView import TerminalView
from inputs.inputs import ConnnameInput, HostInput, PortInput, UsernameInput, PasswordInput, DeviceInput, BaudrateInput, \
    COMPortInput

class NewConnectionEditor(QWidget):
    controls = []
    values = []
    def __init__(self, terminal_view: TerminalView):
        super().__init__()
        self.terminal_view = terminal_view
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.title = QLabel("Kreator nowego połączenia")
        self.title.setStyleSheet("""
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            padding: 0px;
            width:100%;
            height: 30px;
        """)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(60)
        self.main_layout.addWidget(self.title)

        self.subtitle = QLabel("Aby utworzyć połączenie należy wybrać rodzaj połączenia oraz uzupełnić formularz właściwymi danymi. Jeżeli pole ma pozostać puste (np. EXEC) to należy pozostawić je puste.")
        self.subtitle.setStyleSheet("""
                    text-align: center;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0px;
                    width:100%;
                    height: 30px;
                """)
        self.subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setFixedHeight(40)
        self.subtitle.setWordWrap(True)
        self.main_layout.addWidget(self.subtitle)


        self.combo_layout = QHBoxLayout()
        self.comboLabel = QLabel("Rodzaj połączenia")
        self.comboLabel.setStyleSheet("""
                    margin: 10px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)

        self.combo = QComboBox()
        self.combo.addItems(["SSH", "COM", "TELNET", "TFTP"])
        self.combo.setStyleSheet("""
                width: 30%;
        """)
        self.combo.currentTextChanged.connect(self.change_controls)
        self.combo_layout.addWidget(self.comboLabel)
        self.combo_layout.addWidget(self.combo)

        self.main_layout.addLayout(self.combo_layout)

        self.controls_layout = QVBoxLayout()

        self.main_layout.addLayout(self.controls_layout)
        self.setLayout(self.main_layout)

        self.show_ssh_controls()

        self.control_buttons_layout = QHBoxLayout()

        self.save_connection = QPushButton("Zapisz połączenie")
        self.save_connection.setIcon(self.save_connection.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.save_connection.setStyleSheet("margin-top:10px; padding: 5px;")
        self.save_connection.clicked.connect(self.save_connection_handler)
        self.temp_connection = QPushButton("Tymczasowe połączenie")
        self.temp_connection.setIcon(self.temp_connection.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.temp_connection.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_creator = QPushButton("Zamknij kreator")
        self.close_creator.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_creator.setIcon(self.close_creator.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))


        self.control_buttons_layout.addWidget(self.close_creator)
        self.control_buttons_layout.addWidget(self.temp_connection)
        self.control_buttons_layout.addWidget(self.save_connection)

        self.main_layout.addLayout(self.control_buttons_layout)

        self.main_layout.addStretch(0)

    def change_controls(self, arg):
        self.clear_layout(self.controls_layout)
        if arg == "SSH":
            self.show_ssh_controls()
        elif arg == "TELNET":
            self.show_telnet_controls()
        elif arg == "TFTP":
            self.show_tftp_controls()
        elif arg == "COM":
            self.show_com_controls()

    def show_ssh_controls(self):
        self.controls = [
            ConnnameInput(), HostInput(), PortInput("Port SSH:", QIntValidator()), UsernameInput(), PasswordInput("Hasło:"), PasswordInput("EXEC:"), DeviceInput()
        ]
        for control in self.controls:
            self.controls_layout.addLayout(control.getLayout())


    def show_telnet_controls(self):
        self.controls = [
            ConnnameInput(), HostInput(), PortInput("Port TELNET:", QIntValidator(), is_telnet=True), PasswordInput("Hasło:"), PasswordInput("EXEC:"), DeviceInput()
        ]
        for control in self.controls:
            self.controls_layout.addLayout(control.getLayout())

    def show_tftp_controls(self):
        pass

    def show_com_controls(self):
        self.controls = [
            ConnnameInput(), COMPortInput(), BaudrateInput(), PasswordInput("EXEC:"), DeviceInput()
        ]
        for control in self.controls:
            self.controls_layout.addLayout(control.getLayout())

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def save_connection_handler(self):
        self.get_values()

        command = f"netmanage create-conn -n=\"{self.values[1]}\" -o \"connections/{self.values[1].lower().replace(" ","_")}.nmconn\" -i \"{".".join([str(item) for item in self.values[2]])}\" -m \"{self.values[0]}\" -d \"{self.values[6]}\" -po {self.values[3]} -pa \"{self.values[4]}\" -e \"{self.values[5]}\""

        print(command)

        self.terminal_view.run_command(command)
        self.terminal_view.output_received.connect(self.handle_command_result)


    def get_values(self):
        self.values = [control.getValue() for control in self.controls]
        self.values.insert(0, self.combo.currentText())


    def validate_input(self):
        self.get_values()



    def handle_command_result(self, result):
        isSuccess = self.is_success(result)
        print(isSuccess)


    def is_success(self, result):
        for line in result.split("\n"):
            if line.strip() == "Success":
                return True
        return False
