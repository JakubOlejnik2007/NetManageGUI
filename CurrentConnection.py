from NetManage.utils import COM_CONNECTION, SSH_CONNECTION, TELNET_CONNECTION, TFTP_CONNECTION
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QStyle
from PyQt6.uic.properties import QtCore
from PyQt6 import QtCore

class CurrentConnection(QWidget):

    connection = None

    def __init__(self):
        super().__init__()

        self.control_buttons_layout = None
        self.close_creator = None
        self.save_connection = None
        self.temp_connection = None
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

    def update_connection(self, connection: COM_CONNECTION | SSH_CONNECTION | TELNET_CONNECTION | TFTP_CONNECTION | None):
        self.connection = connection
        if self.connection is None:
            self.clear_layout(self.layout)
            return
        print(connection.getNetmikoConnDict())


        print(self.connection.METHOD)
        if self.connection.METHOD == "COM":
            self.showCOMConn()
        if self.connection.METHOD == "SSH" or self.connection.METHOD == "TELNET":
            self.showSSHTELConn()

        self.show_control_buttons()

    def showSSHTELConn(self):
        self.clear_layout(self.layout)

        title = QLabel(f"Połączenie {self.connection.METHOD}")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Host:", self.connection.HOST)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Device:", self.connection.DEVICE)
        self.showKeyValue("EXEC:", "TAK" if self.connection.EXECPASS else "NIE")

    def showCOMConn(self):
        self.clear_layout(self.layout)

        title = QLabel("Połączenie COM")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Baudrate:", self.connection.BAUDRATE)
        self.showKeyValue("Device:", self.connection.DEVICE)
        self.showKeyValue("EXEC:", "TAK" if self.connection.EXECPASS else "NIE")

    def show_control_buttons(self):

        self.control_buttons_layout = QHBoxLayout()

        self.save_connection = QPushButton("Zamknij")
        self.save_connection.setIcon(
        self.save_connection.style().standardIcon(QStyle.StandardPixmap.SP_LineEditClearButton))
        self.save_connection.setStyleSheet("margin-top:10px; padding: 5px;")

        self.temp_connection = QPushButton("Usuń")
        self.temp_connection.setIcon(self.temp_connection.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
        self.temp_connection.setStyleSheet("margin-top:10px; padding: 5px;")

        self.close_creator = QPushButton("Test")
        self.close_creator.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_creator.setIcon(self.close_creator.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))

        self.control_buttons_layout.addWidget(self.close_creator)
        self.control_buttons_layout.addWidget(self.temp_connection)
        self.control_buttons_layout.addWidget(self.save_connection)

        self.layout.addLayout(self.control_buttons_layout)

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