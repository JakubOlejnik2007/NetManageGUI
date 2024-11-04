from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self, reload_connections):
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
