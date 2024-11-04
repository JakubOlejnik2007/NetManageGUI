# menu_bar.py
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.file_menu = self.addMenu('Plik')

        # Tworzenie akcji
        new_action = QAction('Nowy', self)
        open_action = QAction('Otwórz', self)
        exit_action = QAction('Zamknij', self)

        # Dodawanie akcji do menu
        self.file_menu.addAction(new_action)
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(exit_action)
