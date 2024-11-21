import os
import sys

from NetManage.utils.NMCONN_file import read_nmconn
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QSizePolicy, QAbstractItemView

from utils.consts import CONNECTIONS_DIR


class ConnectionsList(QWidget):
    def __init__(self, setCurrConnection):
        super().__init__()
        self.setCurrConnection = setCurrConnection

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

        for conn in os.listdir(CONNECTIONS_DIR):
            connection = read_nmconn(f"{CONNECTIONS_DIR}/{conn}")

            self.listWidget.addItem(f"{connection.NAME}   [{conn}]")

    def handle_item_double_clicked(self, item):
        self.setCurrConnection(f"{item.text().split(" ")[-1][1:-1]}")