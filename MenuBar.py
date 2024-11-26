from NetManage.utils.connections import SSH_CONNECTION, TELNET_CONNECTION, COM_CONNECTION, TFTP_CONNECTION
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

from ConnectionsList import ConnectionsList
from CurrentConnection import CurrentConnection
from utils.consts import SHORTCUTS


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
        self.new_connection.setShortcut(SHORTCUTS["CONNECTION"]["NEW"])
        self.new_connection.triggered.connect(main.new_connection)

        self.test_connection = QAction('Test', self)
        self.test_connection.setEnabled(False)
        self.test_connection.setShortcut(SHORTCUTS["CONNECTION"]["TEST"])
        self.test_connection.triggered.connect(current_connection.test_connection_handler)

        self.edit_connection = QAction('Edycja', self)
        self.edit_connection.setEnabled(False)
        self.edit_connection.setShortcut(SHORTCUTS["CONNECTION"]["EDIT"])
        self.edit_connection.triggered.connect(main.edit_connection)

        self.close_connection = QAction('Zamknij', self)
        self.close_connection.setEnabled(False)
        self.close_connection.setShortcut(SHORTCUTS["CONNECTION"]["CLOSE"])
        self.close_connection.triggered.connect(main.close_connection)

        self.delete_connection = QAction('Usuń', self)
        self.delete_connection.setEnabled(False)
        self.delete_connection.setShortcut(SHORTCUTS["CONNECTION"]["DELETE"])
        self.delete_connection.triggered.connect(main.delete_connection)

        self.connection_menu.addAction(self.new_connection)
        self.connection_menu.addAction(self.test_connection)
        self.connection_menu.addAction(self.edit_connection)
        self.connection_menu.addAction(self.close_connection)
        self.connection_menu.addAction(self.delete_connection)

        self.command_menu = self.addMenu('Polecenia')

        self.open_new_command = QAction('Nowe')
        self.open_new_command.triggered.connect(main.open_command_editor)
        self.open_new_command.setShortcut(SHORTCUTS["COMMAND"]["NEW"])
        self.command_menu.addAction(self.open_new_command)

        self.edit_command = QAction('Edytuj')
        self.edit_command.setEnabled(False)
        self.edit_command.triggered.connect(main.open_command_editor)
        self.edit_command.setShortcut(SHORTCUTS["COMMAND"]["EDIT"])
        self.command_menu.addAction(self.edit_command)

        self.delete_command = QAction('Usuń')
        self.delete_command.setEnabled(False)
        self.delete_command.triggered.connect(main.open_command_editor)
        self.delete_command.setShortcut(SHORTCUTS["COMMAND"]["DELETE"])
        self.command_menu.addAction(self.delete_command)

        self.execute_command = QAction('Uruchom')
        self.execute_command.setEnabled(False)
        self.execute_command.triggered.connect(main.open_command_editor)
        self.execute_command.setShortcut(SHORTCUTS["COMMAND"]["RUN"])
        self.command_menu.addAction(self.execute_command)







    def toggleActionActivationConnection(self, connection: SSH_CONNECTION | TELNET_CONNECTION | COM_CONNECTION | TFTP_CONNECTION | None):
        enabled = False
        if connection is not None:
            enabled = True
        self.test_connection.setEnabled(enabled)
        self.edit_connection.setEnabled(enabled)
        self.close_connection.setEnabled(enabled)
        self.delete_connection.setEnabled(enabled)

    def toggleActionActivationCommand(self, command_file: str | None):
        enabled = False
        if command_file is not None:
            enabled = True
        self.edit_command.setEnabled(enabled)
        self.delete_command.setEnabled(enabled)
        self.execute_command.setEnabled(enabled)