from NetManage.utils import COM_CONNECTION, SSHTEL_CONNECTION, TFTP_CONNECTION
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.uic.properties import QtCore
from PyQt6 import QtCore

class CurrentConnection(QWidget):

    connection = None

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel('Obecne połączenie')
        self.layout.addWidget(self.label)

        self.button = QPushButton('Kliknij mnie')
        self.button.clicked.connect(self.change_text)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def change_text(self):
        self.label.setText('Tekst został zmieniony!')

    def update_connection(self, connection: COM_CONNECTION | SSHTEL_CONNECTION | TFTP_CONNECTION | None):
        print(connection.getNetmikoConnDict())
        self.connection = connection

        print(self.connection.METHOD)
        if self.connection.METHOD == "COM":
            self.showCOMConn()
        if self.connection.METHOD == "SSH" or self.connection.METHOD == "TELNET":
            self.showSSHTELConn()
    def showSSHTELConn(self):
        self.clear_layout(self.layout)

        title = QLabel(f"Połączenie {self.connection.METHOD}")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Host:", self.connection.HOST)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Username:", self.connection.USERNAME)
        self.showKeyValue("Device:", self.connection.DEVICE)

    def showCOMConn(self):
        self.clear_layout(self.layout)

        title = QLabel("Połączenie COM")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Baudrate:", self.connection.BAUDRATE)
        self.showKeyValue("Device:", self.connection.DEVICE)



    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def showKeyValue(self, key, value):
        hlayout = QHBoxLayout()
        label1 = QLabel(key)
        label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        label2 = QLabel(value)
        label2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        hlayout.addWidget(label1)
        hlayout.addWidget(label2)
        self.layout.addLayout(hlayout)