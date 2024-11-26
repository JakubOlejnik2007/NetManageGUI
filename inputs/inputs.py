from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLineEdit, QHBoxLayout, QLabel
from PyQt6.QtGui import QIntValidator
from PyQt6 import QtCore
from inputs.base_input import BaseInput
from inputs.combo_input import ComboInput
from utils.comutils import serial_ports
from utils.consts import SUPPORTED_DEVICES, COMMANDS_DIR, CONNECTIONS_DIR
from validators.validators import validate_sshtel_port, validate_baudrate, validate_string, validate_ip_list, \
    validate_subnet_list


class PortInput(BaseInput):
    def __init__(self, label, validator, hide_input=False, is_telnet=False):
        super().__init__(label, validator=validator, hide_input=hide_input, default_value="23" if is_telnet else "22", max_length=5)

    def validate(self, validate_method=validate_sshtel_port, invalid_message="Nieprawidłowy port SSH/Telnet. [0-65535]"):
        return super().validate(validate_method, invalid_message)

class BaudrateInput(BaseInput):
    def __init__(self):
        super().__init__("Baudrate", validator=QIntValidator(), default_value="9600")

    def validate(self, validate_method=validate_baudrate, invalid_message="Nieprawidłowy baudrate. [0-115200]"):
        return super().validate(validate_method, invalid_message)

class DeviceInput(ComboInput):

    def __init__(self, device = None):
        super().__init__("Urządzenie:", SUPPORTED_DEVICES, value = device)

class COMPortInput(ComboInput):
    def __init__(self):
        ports = serial_ports()
        super().__init__("Port COM:", ports if len(ports) > 0 else ["No COM port available."])


class UsernameInput(BaseInput):
    def __init__(self):
        super().__init__("Username:")

    def validate(self, validate_method=validate_string, invalid_message="Nazwa użytkownika nie może być pusta."):
        return super().validate(validate_method, invalid_message)


class NameInput(BaseInput):
    def __init__(self, disabled=False, is_command_name = False):
        self.isCommand = is_command_name
        label = "Nazwa połączenia:" if not self.isCommand else "Nazwa polecenia:"
        super().__init__(label, disabled=disabled)

    def validate(self, validate_method=validate_string, invalid_message="Nazwa nie może być pusta."):
        if not self.isCommand:
            invalid_message = f"{invalid_message} Wyjątek - połączenia TEMP."

        return super().validate(validate_method, invalid_message)


class PasswordInput(BaseInput):
    def __init__(self, label):
        super().__init__(label, hide_input=True)

    def validate(self, validate_method=validate_string, invalid_message="Hasło nie może być puste. [Wyjątek - hasło EXEC]"):
        return super().validate(validate_method, invalid_message)

class HostInput:
    values = []
    def __init__(self, label = "Host:"):
        self.main_layout = QVBoxLayout()
        self.host_layout = QHBoxLayout()
        self.hostLabel = QLabel(label)
        self.hostLabel.setStyleSheet("""
                    margin: 10px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)
        self.host_layout.addWidget(self.hostLabel, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.ips_layout = QHBoxLayout()
        for i in range(4):
            ip = QLineEdit()
            ip.setMaxLength(3)
            ip.setValidator(QIntValidator(0, 255))
            ip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            ip.setText("0")
            self.ips_layout.addWidget(ip, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
            if i < 3:
                dot = QLabel(".")
                dot.setStyleSheet("margin: 2; font-size: 24px;")
                self.ips_layout.addWidget(dot, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.host_layout.addLayout(self.ips_layout)
        self.host_layout.addStretch()
        self.host_layout.setStretch(0, 18)
        self.host_layout.setStretch(1, 12)
        for i in range(8):
            self.ips_layout.setStretch(i, 2 if i % 2 == 0 else 1)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red; font-size: 10px;")
        self.error_label.setVisible(False)
        self.main_layout.addLayout(self.host_layout)
        self.main_layout.addWidget(self.error_label)

    def getLayout(self):
        return self.main_layout

    def getValue(self):
        self.values = []
        for i in range(0, self.ips_layout.count(), 2):
            ip_field = self.ips_layout.itemAt(i).widget()
            if isinstance(ip_field, QLineEdit):
                text = ip_field.text()
                self.values.append(int(text) if text.isdigit() else 0)
                ip_field.setText(text if text.isdigit() else "0")
        self.validate()
        return self.values

    def setValue(self, values: list):
        for i in range(0, self.ips_layout.count(), 2):
            ip_field = self.ips_layout.itemAt(i).widget()
            if isinstance(ip_field, QLineEdit):
                ip_field.setText(values.pop(0))

    def validate(self, validate_method=validate_ip_list, invalid_message="Nieprawidłowy adres IPv4"):
        is_valid = validate_method(self.values)
        print(f"IP valid: {is_valid}, IP: {".".join([str(value) for value in self.values])}")
        if not is_valid:
            self.error_label.setVisible(True)
            self.error_label.setText(invalid_message)
        else:
            self.error_label.setVisible(False)
        return is_valid

class SubnetInput(HostInput):
    def __init__(self, label = "Maska:"):
        super().__init__(label)

    def validate(self, validate_method=validate_subnet_list, invalid_message="Nieprawidłowy adres IPv4"):
        super().validate(validate_method, invalid_message)