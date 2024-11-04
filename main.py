import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QGridLayout, QWidget
from PyQt6.QtCore import QProcess

from CommandEditor import CommandEditor
from CommandsList import CommandList
from ConnectionsList import ConnectionsList
from CurrentConnection import CurrentConnection
from MenuBar import MenuBar
from TerminalView import TerminalView


class NetManageGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        terminal_view = TerminalView()
        command_list = CommandList()
        command_editor = CommandEditor()
        current_connection = CurrentConnection()
        connections_list = ConnectionsList()


        menu_bar = MenuBar(connections_list.load_list)
        self.setMenuBar(menu_bar)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid = QGridLayout(central_widget)



        grid.addWidget(command_list, 0, 0, 3, 1)
        grid.addWidget(command_editor, 0, 1, 2, 2)
        grid.addWidget(terminal_view, 2, 1, 1, 2)
        grid.addWidget(current_connection, 0, 3, 1, 1)
        grid.addWidget(connections_list, 1, 3, 2, 1)


        self.setWindowIcon(QIcon("./assets/icon.ico"))
        self.setWindowTitle('NetManageGUI')
        self.setGeometry(100, 100, 1000, 750)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NetManageGUI()
    window.show()
    sys.exit(app.exec())
