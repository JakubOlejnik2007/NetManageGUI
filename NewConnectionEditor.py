from PyQt6 import QtCore
from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QPushButton, QStyle

from TerminalView import TerminalView
from inputs.inputs import NameInput, HostInput, PortInput, UsernameInput, PasswordInput, DeviceInput, BaudrateInput, \
    COMPortInput
from utils.consts import CONNECTIONS_DIR
from utils.detect_success import is_success
from validators.validators import validate_method, validate_string, validate_sshtel_port, validate_ip_list, \
    validate_com_port, validate_baudrate


class NewConnectionEditor(QWidget):
    controls = []
    values = []
    def __init__(self, terminal_view: TerminalView, main):
        super().__init__()

        self.setWindowTitle("Kreator połączeń")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowIcon(QIcon("assets/icon.ico"))


        self.setFixedSize(416, 550)

        self.terminal_view = terminal_view

        self.main = main

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
        self.subtitle.setMinimumHeight(65)
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
        self.temp_connection.clicked.connect(lambda: self.save_connection_handler(temp=True))

        self.close_creator = QPushButton("Zamknij kreator")
        self.close_creator.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_creator.setIcon(self.close_creator.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.close_creator.clicked.connect(self.handle_close)


        self.control_buttons_layout.addWidget(self.close_creator)
        self.control_buttons_layout.addWidget(self.temp_connection)
        self.control_buttons_layout.addWidget(self.save_connection)

        self.main_layout.addStretch()
        self.main_layout.addLayout(self.control_buttons_layout)
        self.main_layout.setContentsMargins(10,10,10,10)

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
            NameInput(), HostInput(), PortInput("Port SSH:", QIntValidator(0, 65535)), UsernameInput(), PasswordInput("Hasło:"), PasswordInput("EXEC:"), DeviceInput()
        ]
        for control in self.controls:
            self.controls_layout.addLayout(control.getLayout())


    def show_telnet_controls(self):
        self.controls = [
            NameInput(), HostInput(), PortInput("Port TELNET:", QIntValidator(0, 65535), is_telnet=True), PasswordInput("Hasło:"), PasswordInput("EXEC:"), DeviceInput()
        ]
        for control in self.controls:
            self.controls_layout.addLayout(control.getLayout())

    def show_tftp_controls(self):
        pass

    def show_com_controls(self):
        self.controls = [
            NameInput(), COMPortInput(), BaudrateInput(), PasswordInput("EXEC:"), DeviceInput()
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

    def save_connection_handler(self, temp = False):
        print(self.size())
        self.get_values()
        self.terminal_view.disconnect_signal()
        self.terminal_view.output_received.connect(self.handle_command_result)
        print("temp", temp)

        if temp:
            self.values[1] = "temp"

        if self.validate_input():
            if self.values[0] == "SSH":
                command = f"./netmanage create-conn -n=\"{self.values[1]}\" -o \"{CONNECTIONS_DIR}/{self.values[1].lower().replace(" ","_")}.nmconn\" -i \"{".".join([str(item) for item in self.values[2]])}\" -m \"{self.values[0]}\" -d \"{self.values[7]}\" -po {self.values[3]} -u \"{self.values[4]}\" -pa \"{self.values[5]}\" -e \"{self.values[6]}\""
                print(command)
                self.terminal_view.run_command(command)

            elif self.values[0] == "TELNET":
                command = f"./netmanage create-conn -n=\"{self.values[1]}\" -o \"{CONNECTIONS_DIR}/{self.values[1].lower().replace(" ","_")}.nmconn\" -i \"{".".join([str(item) for item in self.values[2]])}\" -m \"{self.values[0]}\" -d \"{self.values[6]}\" -po {self.values[3]} -pa \"{self.values[4]}\" -e \"{self.values[5]}\""
                print(command)
                self.terminal_view.run_command(command)

            elif self.values[0] == "COM":
                command = f"./netmanage create-conn -n=\"{self.values[1]}\" -o \"{CONNECTIONS_DIR}/{self.values[1].lower().replace(" ","_")}.nmconn\" -m \"{self.values[0]}\" -d \"{self.values[5]}\" -po \"{self.values[2]}\" -b \"{self.values[3]}\" -e \"{self.values[4]}\""
                print(command)
                self.terminal_view.run_command(command)

        else:
            pass

        print(self.size())

    def get_values(self):
        self.values = [control.getValue() for control in self.controls]
        self.values.insert(0, self.combo.currentText())


    def validate_input(self) -> bool:
        if not validate_method(self.values[0]):
            return False

        if self.values[0] == "SSH":
            return validate_string(self.values[1]) and validate_ip_list(self.values[2]) and validate_sshtel_port(int(self.values[3])) and validate_string(self.values[4]) and validate_string(self.values[5]) and validate_string(self.values[6])

        elif self.values[0] == "TELNET":
            return validate_string(self.values[1]) and validate_ip_list(self.values[2]) and validate_sshtel_port(int(self.values[3])) and validate_string(self.values[4]) and validate_string(self.values[5])

        elif self.values[0] == "TFTP":
            pass

        elif self.values[0] == "COM":
            return validate_string(self.values[1]) and validate_com_port(self.values[2]) and validate_baudrate(int(self.values[3])) and validate_string(self.values[4])

        return False


    def handle_command_result(self, result):
        if is_success(result):
            self.main.connections_list.load_list()
            self.main.set_connection(f"{self.values[1].lower().replace(" ", "_")}.nmconn")
            self.handle_close()

    def handle_close(self):
        self.close()