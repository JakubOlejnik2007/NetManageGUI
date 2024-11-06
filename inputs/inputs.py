import PyQt6
from PyQt6 import QtCore
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel

from inputs.base_input import BaseInput
from inputs.combo_input import ComboInput
from utils.comutils import serial_ports

class PortInput(BaseInput):
    def __init__(self, label, validator, hide_input=False, is_telnet=False):
        super().__init__(label, validator=validator, hide_input=hide_input, default_value="23" if is_telnet else "22")

class BaudrateInput(BaseInput):
    def __init__(self):
        super().__init__("Baudrate", validator=QIntValidator(), default_value="9600")

class DeviceInput(ComboInput):
    devices = [
        'cisco_ios', 'cisco_xe', 'cisco_asa', 'cisco_nxos', 'cisco_iosxr', 'arista_eos', 'juniper',
        'hp_procurve', 'dell_force10', 'brocade', 'fortinet', 'mikrotik', 'huawei', 'checkpoint', 'paloalto'
    ]

    def __init__(self):
        super().__init__("Urządzenie:", self.devices)

class COMPortInput(ComboInput):
    def __init__(self):
        ports = serial_ports()
        super().__init__("Port COM:", ports if len(ports) > 0 else ["No COM port available."])


class UsernameInput(BaseInput):
    def __init__(self):
        super().__init__("Username:")


class ConnnameInput(BaseInput):
    def __init__(self):
        super().__init__("Nazwa połączenia:")


class PasswordInput(BaseInput):
    def __init__(self, label):
        super().__init__(label, hide_input=True)


class HostInput:
    def __init__(self):
        self.host_layout = QHBoxLayout()
        self.hostLabel = QLabel("Host:")
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
            ip.setValidator(QIntValidator())
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

    def getLayout(self):
        return self.host_layout

    def getValue(self):
        values = []
        for i in range(0, self.ips_layout.count(), 2):
            if isinstance(self.ips_layout.itemAt(i).widget(), QLineEdit):
                text = self.ips_layout.itemAt(i).widget().text()
                values.append(int(text) if text.isdigit() else 0)
                self.ips_layout.itemAt(i).widget().setText(text if text.isdigit() else "0")
        return values
