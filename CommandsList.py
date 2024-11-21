import os
import sys

from NetManage.utils.NMCOMM_file import read_NMCOMM
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QSizePolicy, QAbstractItemView, QListWidgetItem

from utils.consts import SUPPORTED_DEVICES


class CommandList(QWidget):

    def __init__(self, main):
        super().__init__()

        self.main = main

        self.listWidget = QListWidget(self)
        self.listWidget.itemDoubleClicked.connect(self.handle_item_double_clicked)
        self.listWidget.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)

        self.layout = QVBoxLayout(self)
        self.label = QLabel('Zapisane polecenia')

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listWidget)

        self.load_list()

        self.setLayout(self.layout)

    def load_list(self):
        self.listWidget.clear()
        grouped_commands = self.group_commands_by_type_and_device()

        for type_name, devices in grouped_commands.items():
            type_item = QListWidgetItem(f"{type_name}")
            type_item.setFlags(type_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            type_item.setFont(QFont('Arial', 12, QFont.Weight.Bold))
            self.listWidget.addItem(type_item)

            for device_name, commands in devices.items():
                device_item = QListWidgetItem(f"  {device_name}")
                device_item.setFont(QFont('Arial', 11, QFont.Weight.Bold))
                device_item.setFlags(device_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)

                if self.main.connection is not None and device_name != self.main.connection.DEVICE:
                    device_item.setFlags(device_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                self.listWidget.addItem(device_item)

                for command in commands:
                    command_item = QListWidgetItem(f"    {command}")
                    if self.main.connection is not None and device_name != self.main.connection.DEVICE:
                        command_item.setFlags(command_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                    self.listWidget.addItem(command_item)

    def group_commands_by_type_and_device(self):
        grouped = {}

        base_dir = os.path.dirname(sys.executable) if hasattr(sys, "frozen") else os.path.dirname(__file__)
        commands_dir = os.path.join(base_dir, "commands")

        for comm in os.listdir(commands_dir):
            command = read_NMCOMM(f"{commands_dir}/{comm}")

            type_name = command.TYPE
            if type_name not in grouped:
                grouped[type_name] = {}

            for device in SUPPORTED_DEVICES:
                if device in command.devices:
                    if device not in grouped[type_name]:
                        grouped[type_name][device] = []
                    grouped[type_name][device].append(f"{command.NAME}   [{comm}]")

        return grouped

    def handle_item_double_clicked(self, item):
        self.setCurrConnection(item.text())
