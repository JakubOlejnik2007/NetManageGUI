from wsgiref.validate import validator

from PyQt6 import QtCore
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QSpacerItem, QLineEdit, QSizePolicy
from PyQt6.uic.Compiler.qtproxies import QtGui
from utils.comutils import serial_ports





class NewConnectionEditor(QWidget):
    controls = []
    def __init__(self):
        super().__init__()
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
            height: 100px;
        """)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(100)
        self.main_layout.addWidget(self.title)

        self.subtitle = QLabel("Aby utworzyć połączenie należy wybrać rodzaj połączenia oraz uzupełnić formularz właściwymi danymi. Jeżeli pole ma pozostać puste (np. EXEC) to należy pozostawić je puste.")
        self.subtitle.setStyleSheet("""
                    text-align: center;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 0px;
                    width:100%;
                    height: 100px;
                """)
        self.subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setFixedHeight(100)
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

        self.main_layout.addStretch(0)

    def change_controls(self, arg):
        print(arg)
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