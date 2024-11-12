from NetManage.utils import COM_CONNECTION, SSH_CONNECTION, TELNET_CONNECTION, TFTP_CONNECTION
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QStyle
from PyQt6.uic.properties import QtCore
from PyQt6 import QtCore

from TerminalView import TerminalView
from utils.detect_success import is_success


class CurrentConnection(QWidget):

    connection = None
    connectionFile = None
    connection_icon = None

    def __init__(self, terminal_view: TerminalView):
        super().__init__()

        self.terminal_view = terminal_view

        self.is_connected = False

        self.control_buttons_layout = None
        self.edit_connection = None
        self.close_connection = None
        self.test_connection = None
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

        self.connection_icon = QLabel()
        self.connection_icon.setPixmap(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogNoButton).pixmap(20, 20))



    def update_connection(self, connection: COM_CONNECTION | SSH_CONNECTION | TELNET_CONNECTION | TFTP_CONNECTION | None, connection_file):
        self.connection_icon = QLabel()
        self.connection_icon.setPixmap(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogNoButton).pixmap(20, 20))
        self.is_connected = False
        self.connection = connection
        self.connectionFile = connection_file
        if self.connection is None:
            self.clear_layout(self.layout)
            self.connectionFile = None
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

        title_layout = QHBoxLayout()
        title = QLabel(f"Połączenie {self.connection.METHOD}")
        title.setStyleSheet("font-size: 20px")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)


        title_layout.addWidget(self.connection_icon)
        title_layout.addWidget(title)
        self.layout.addLayout(title_layout)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Host:", self.connection.HOST)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Device:", self.connection.DEVICE)
        self.showKeyValue("EXEC:", "TAK" if self.connection.EXECPASS else "NIE")

    def showCOMConn(self):
        self.clear_layout(self.layout)

        title_layout = QHBoxLayout()
        title = QLabel(f"Połączenie {self.connection.METHOD}")
        title.setStyleSheet("font-size: 20px")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        title_layout.addWidget(self.connection_icon)
        title_layout.addWidget(title)
        self.layout.addLayout(title_layout)

        self.showKeyValue("Metoda:", self.connection.METHOD)
        self.showKeyValue("Port:", self.connection.PORT)
        self.showKeyValue("Baudrate:", self.connection.BAUDRATE)
        self.showKeyValue("Device:", self.connection.DEVICE)
        self.showKeyValue("EXEC:", "TAK" if self.connection.EXECPASS else "NIE")

    def show_control_buttons(self):

        self.control_buttons_layout = QHBoxLayout()

        self.close_connection = QPushButton("Zamknij")
        self.close_connection.setIcon(
        self.close_connection.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton.SP_DialogCancelButton))
        self.close_connection.setStyleSheet("margin-top:10px; padding: 5px;")

        self.test_connection = QPushButton("Test")
        self.test_connection.setIcon(self.test_connection.style().standardIcon(QStyle.StandardPixmap.SP_DriveNetIcon))
        self.test_connection.setStyleSheet("margin-top:10px; padding: 5px;")
        self.test_connection.clicked.connect(self.test_connection_handler)

        self.edit_connection = QPushButton("Edytuj")
        self.edit_connection.setStyleSheet("margin-top:10px; padding: 5px;")
        self.edit_connection.setIcon(self.edit_connection.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView))


        self.control_buttons_layout.addWidget(self.close_connection)
        self.control_buttons_layout.addWidget(self.test_connection)
        self.control_buttons_layout.addWidget(self.edit_connection)

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

    def test_connection_handler(self):
        print(self.connectionFile)

        self.terminal_view.run_command(f"netmanage test-conn -c .\\connections\\{self.connectionFile}")

        self.terminal_view.output_received.connect(self.handle_command_result)

    def handle_command_result(self, result):
        if is_success(result):
            print(result)
            self.connection_icon.setPixmap(
                self.style().standardIcon(QStyle.StandardPixmap.SP_DialogYesButton).pixmap(20, 20))
        else:
            print(result)
            print("Connection test failed")