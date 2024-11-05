import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QGridLayout, \
    QWidget, QMessageBox
from PyQt6.QtCore import QProcess, pyqtSignal

from CommandEditor import CommandEditor
from CommandsList import CommandList
from ConnectionsList import ConnectionsList
from CurrentConnection import CurrentConnection
from MenuBar import MenuBar
from TerminalView import TerminalView
from NetManage.utils import read_nmconn, SSHTEL_CONNECTION, COM_CONNECTION, TFTP_CONNECTION

def exception_hook(exctype, value, traceback):
    print("Błąd:", exctype, value)
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_hook

class NetManageGUI(QMainWindow):
    connection_changed = pyqtSignal(object)
    central_widget = None
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connectionFile = ""
        self.connection: SSHTEL_CONNECTION | COM_CONNECTION | TFTP_CONNECTION | None = None

    def initUI(self):
        self.central_widget = QWidget(self)
        terminal_view = TerminalView()
        command_list = CommandList()
        command_editor = CommandEditor()
        current_connection = CurrentConnection()
        connections_list = ConnectionsList(self.setConnection)


        menu_bar = MenuBar(connections_list.load_list, self.closeConnection)
        self.setMenuBar(menu_bar)
        self.setCentralWidget(self.central_widget)

        grid = QGridLayout(self.central_widget)

        self.connection_changed.connect(current_connection.update_connection)
        self.connection_changed.connect(menu_bar.toggleActionActivation)

        grid.addWidget(command_list, 0, 0, 3, 1)
        grid.addWidget(command_editor, 0, 1, 2, 2)
        grid.addWidget(terminal_view, 2, 1, 1, 2)
        grid.addWidget(current_connection, 0, 3, 1, 1)
        grid.addWidget(connections_list, 1, 3, 2, 1)


        self.setWindowIcon(QIcon("./assets/icon.ico"))
        self.setWindowTitle('NetManageGUI')
        self.setGeometry(100, 100, 1000, 750)

    def setConnection(self, connection_file):
        if self.connection is not None:
            change_conn = self.confirm_message_box("Zmiana połączenia", "Czy na pewno chcesz zmienić połączenie?")
            if not change_conn:
                return

        self.connectionFile = connection_file
        try:
            self.connection = read_nmconn(f"connections\\{connection_file}")
            #print(self.connection)
            self.connection_changed.emit(self.connection)
        except Exception as e:
            print(e)
            self.connection = None
            self.connectionFile = ""

    def closeConnection(self):

        if not self.confirm_message_box("Zamknięcie połączenia", "Czy na pewno chcesz zamknąć połączenie?"):
            return

        self.connection = None
        self.connectionFile = ""
        self.connection_changed.emit(self.connection)

    def confirm_message_box(self, title: str, message: str, yes_button_mess: str = "Tak", no_button_mess: str = "Nie") -> bool:
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetManageGUI()
    window.show()
    sys.exit(app.exec())
