from PyQt6 import QtCore
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QLabel, QSizePolicy, QComboBox

from inputs.base_input import BaseInput
from utils.comutils import serial_ports

class PortInput(BaseInput):
    def __init__(self, label, validator, hide_input=False, is_telnet=False):
        super().__init__(label, validator=validator, hide_input=hide_input, default_value="23" if is_telnet else "22")

class BaudrateInput(BaseInput):
    def __init__(self):
        super().__init__("Baudrate", validator=QIntValidator(), default_value="9600")

class ComboInput:
    def __init__(self, label, items, disabled_if_empty=True):
        self.combo_layout = QHBoxLayout()
        self.comboLabel = QLabel(label)
        self.comboLabel.setStyleSheet("""
                    margin: 10px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)
        self.combo = QComboBox()
        self.combo.addItems(items)
        self.combo.setDisabled((len(items) == 0 or items[0] == "No COM port available.") and disabled_if_empty)
        self.combo.setStyleSheet("width: 30%;")
        self.combo_layout.addWidget(self.comboLabel)
        self.combo_layout.addWidget(self.combo)

    def getLayout(self):
        return self.combo_layout


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

        ips_layout = QHBoxLayout()
        for i in range(4):
            ip = QLineEdit()
            ip.setMaxLength(3)
            ip.setValidator(QIntValidator())
            ip.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            ips_layout.addWidget(ip, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
            if i < 3:
                dot = QLabel(".")
                dot.setStyleSheet("margin: 2; font-size: 24px;")
                ips_layout.addWidget(dot, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.host_layout.addLayout(ips_layout)
        self.host_layout.addStretch()
        self.host_layout.setStretch(0, 18)
        self.host_layout.setStretch(1, 12)
        for i in range(8):
            ips_layout.setStretch(i, 2 if i % 2 == 0 else 1)

    def getLayout(self):
        return self.host_layout