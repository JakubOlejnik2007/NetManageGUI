import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QSizePolicy


class ConnectionsList(QWidget):
    def __init__(self):
        super().__init__()

        self.listWidget = QListWidget(self)
        self.listWidget.itemDoubleClicked.connect(self.handle_item_double_clicked)
        self.listWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout(self)
        self.label = QLabel('Zapisane połączenia')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listWidget)

        self.load_list()

        self.setLayout(self.layout)

    def load_list(self):
        self.listWidget.clear()
        for conn in os.listdir("connections"):
            self.listWidget.addItem(conn)

    def handle_item_double_clicked(self, item):
        print(item.text())