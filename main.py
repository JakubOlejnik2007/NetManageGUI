import os
import sys

from NetManage.utils.NMCONN_file import read_nmconn
from NetManage.utils.connections import SSH_CONNECTION, TELNET_CONNECTION, COM_CONNECTION, TFTP_CONNECTION
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QGridLayout, \
    QWidget, QMessageBox
from PyQt6.QtCore import QProcess, pyqtSignal

from CommandEditor.CommandEditor import CommandEditor as CE
from CommandsList import CommandList
from ConnectionEditor import ConnectionEditor
from ConnectionsList import ConnectionsList
from CurrentConnection import CurrentConnection
from MenuBar import MenuBar
from NewConnectionEditor import NewConnectionEditor
from TerminalView import TerminalView
from utils.consts import CONNECTIONS_DIR, ASSETS_DIR


def exception_hook(exctype, value, traceback):
    print("Błąd:", exctype, value)
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_hook

class NetManageGUI(QMainWindow):
    connection_changed = pyqtSignal(object)
    central_widget = None
    grid = None
    connection: SSH_CONNECTION | TELNET_CONNECTION | COM_CONNECTION | TFTP_CONNECTION | None = None

    def __init__(self, file_path = None):
        super().__init__()
        self.connection_editor = None
        self.new_connection_editor = None
        self.command_list = None
        self.command_editor = None
        self.current_connection = None
        self.connections_list = None
        self.terminal_view = None
        self.initUI()
        self.connectionFile = ""



        if os.path.exists(f"{CONNECTIONS_DIR}\\temp.nmconn"):
            os.remove(f"{CONNECTIONS_DIR}\\temp.nmconn")

        print(file_path)

    def initUI(self):
        self.central_widget = QWidget(self)
        self.terminal_view = TerminalView()
        self.command_list = CommandList(self)
        self.command_editor = CE()
        self.current_connection = CurrentConnection(self.terminal_view, self)
        self.new_connection_editor = NewConnectionEditor(terminal_view=self.terminal_view, main=self)
        self.connections_list = ConnectionsList(self.set_connection)



        menu_bar = MenuBar(self.connections_list, self, self.current_connection)
        self.setMenuBar(menu_bar)
        self.setCentralWidget(self.central_widget)

        self.grid = QGridLayout(self.central_widget)

        self.connection_changed.connect(lambda conn: self.current_connection.update_connection(conn, self.connectionFile))
        self.connection_changed.connect(menu_bar.toggleActionActivation)

        self.grid.addWidget(self.command_list, 0, 0, 3, 2)
        self.grid.addWidget(self.command_editor, 0, 2, 2, 3)
        self.grid.addWidget(self.terminal_view, 2, 2, 1, 3)
        self.grid.addWidget(self.current_connection, 0, 6, 1, 2)
        self.grid.addWidget(self.connections_list, 1, 6, 2, 2)


        self.setWindowIcon(QIcon(f"{ASSETS_DIR}/icon.ico"))
        self.setWindowTitle('NetManageGUI')
        self.setGeometry(100, 100, 1000, 550)

        #self.new_connection()


    def set_connection(self, connection_file):
        if self.connection is not None:
            change_conn = self.confirm_message_box("Zmiana połączenia",
                                                   "Czy na pewno chcesz zmienić połączenie?")
            if not change_conn:
                return

        self.connectionFile = connection_file
        try:
            self.connection = read_nmconn(f"{CONNECTIONS_DIR}/{connection_file}")
            print("Połączenie:")
            print(self.connection)
            self.connection_changed.emit(self.connection)
        except Exception as e:
            print(e)
            self.connection = None
            self.connectionFile = ""


    def close_connection(self, skip_confirm=False):

        if not skip_confirm and not self.confirm_message_box("Zamknięcie połączenia",
                                                             "Czy na pewno chcesz zamknąć połączenie?"):
            return

        self.connection = None
        self.connectionFile = ""
        self.connection_changed.emit(self.connection)

    def delete_connection(self):
        if not self.confirm_message_box("Usuwanie połączenia",
                                        f"Czy na pewno chcesz usunąć połączenie\n{self.connectionFile}?"):
            return


        if os.path.exists(f"{CONNECTIONS_DIR}\\{self.connectionFile}"):
            os.remove(f"{CONNECTIONS_DIR}\\{self.connectionFile}")
            self.connections_list.load_list()
        else:
            print("The file does not exist")

        self.close_connection(True)

    def edit_connection(self):
        print("Edit connection")
        print(self.connection)
        self.connection_editor = ConnectionEditor(terminal_view=self.terminal_view, main=self)
        self.connection_editor.show()

    def new_connection(self):
        print("new connection")
        self.new_connection_editor.show()

    def confirm_message_box(self, title: str, message: str, yes_button_mess: str = "Tak",
                            no_button_mess: str = "Nie", icon = QMessageBox.Icon.Question) -> bool:
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        yes_button = QPushButton(yes_button_mess)
        no_button = QPushButton(no_button_mess)

        dlg.addButton(yes_button, QMessageBox.ButtonRole.AcceptRole)
        dlg.addButton(no_button, QMessageBox.ButtonRole.RejectRole)
        dlg.setIcon(QMessageBox.Icon.Question)
        reply = dlg.exec()

        if reply - 2 == QMessageBox.ButtonRole.AcceptRole.value:
            print("Zamknięto.")
            return True
        else:
            print("Anulowano.")
            return False

    def refresh_lists(self):
        self.connections_list.load_list()
        self.command_list.load_list()

if __name__ == '__main__':
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    app = QApplication(sys.argv)
    window = NetManageGUI(file_path=file_path)
    window.show()
    sys.exit(app.exec())
