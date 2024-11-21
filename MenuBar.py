from NetManage.utils.connections import SSH_CONNECTION, TELNET_CONNECTION, COM_CONNECTION, TFTP_CONNECTION
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from ConnectionsList import ConnectionsList
from CurrentConnection import CurrentConnection


class MenuBar(QMenuBar):
    def __init__(self, connections_list: ConnectionsList, main, current_connection: CurrentConnection):
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

        refresh.triggered.connect(main.refresh_lists)

        self.tools_menu.addAction(refresh)

        self.connection_menu = self.addMenu('Połączenie')
        self.new_connection = QAction('Nowe', self)
        self.new_connection.setShortcut("Ctrl+N")
        self.new_connection.triggered.connect(main.new_connection)

        self.test_connection = QAction('Test', self)
        self.test_connection.setEnabled(False)
        self.test_connection.setShortcut("Ctrl+T")
        self.test_connection.triggered.connect(current_connection.test_connection_handler)

        self.edit_connection = QAction('Edycja', self)
        self.edit_connection.setEnabled(False)
        self.edit_connection.setShortcut("Ctrl+E")
        self.edit_connection.triggered.connect(main.edit_connection)

        self.close_connection = QAction('Zamknij', self)
        self.close_connection.setEnabled(False)
        self.close_connection.setShortcut("Esc")
        self.close_connection.triggered.connect(main.close_connection)

        self.delete_connection = QAction('Usuń', self)
        self.delete_connection.setEnabled(False)
        self.delete_connection.setShortcut("Ctrl+Del")
        self.delete_connection.triggered.connect(main.delete_connection)

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