from NetManage.utils import SSH_CONNECTION, TELNET_CONNECTION, COM_CONNECTION, TFTP_CONNECTION
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self, reload_connections, close_connection, delete_connection, new_connection):
        super().__init__()

        self.file_menu = self.addMenu('Plik')

        new_action = QAction('Nowy', self)
        open_action = QAction('Otwórz', self)
        exit_action = QAction('Zamknij', self)

        self.file_menu.addAction(new_action)
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)

        self.tools_menu = self.addMenu('Narzędzia')

        refresh = QAction("Odśwież", self)
        refresh.setShortcut("F5")
        refresh.triggered.connect(reload_connections)

        self.tools_menu.addAction(refresh)

        self.connection_menu = self.addMenu('Połączenie')
        self.new_connection = QAction('Nowe', self)
        self.new_connection.setShortcut("Ctrl+N")
        self.new_connection.triggered.connect(new_connection)

        self.test_connection = QAction('Test', self)
        self.test_connection.setEnabled(False)

        self.edit_connection = QAction('Edycja', self)
        self.edit_connection.setEnabled(False)

        self.close_connection = QAction('Zamknij', self)
        self.close_connection.setEnabled(False)
        self.close_connection.setShortcut("Esc")
        self.close_connection.triggered.connect(close_connection)

        self.delete_connection = QAction('Usuń', self)
        self.delete_connection.setEnabled(False)
        self.delete_connection.setShortcut("Ctrl+Del")
        self.delete_connection.triggered.connect(delete_connection)

        self.connection_menu.addAction(self.new_connection)
        self.connection_menu.addAction(self.test_connection)
        self.connection_menu.addAction(self.edit_connection)
        self.connection_menu.addAction(self.close_connection)
        self.connection_menu.addAction(self.delete_connection)

    def toggleActionActivation(self, connection: SSH_CONNECTION | TELNET_CONNECTION | COM_CONNECTION | TFTP_CONNECTION | None):
        enabled = False
        if connection is not None:
            enabled = True
        self.test_connection.setEnabled(enabled)
        self.edit_connection.setEnabled(enabled)
        self.close_connection.setEnabled(enabled)
        self.delete_connection.setEnabled(enabled)