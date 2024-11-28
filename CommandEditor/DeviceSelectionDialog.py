from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel, QGridLayout, QDialog

from utils.consts import DEVICE_GROUPS, ASSETS_DIR


class DeviceSelectionDialog(QDialog):
    def __init__(self, selected_devices, parent=None, columns=2):
        super().__init__(parent)

        self.setWindowTitle("Wybór urządzeń")
        self.setGeometry(150, 150, 600, 600)
        self.selected_devices = selected_devices
        self.columns = columns
        self.setWindowIcon(QIcon(f"{ASSETS_DIR}/icon.ico"))

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.title = QLabel("Wybierz urządzenia")
        self.title.setStyleSheet("""
            text-align: center;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.main_layout.addWidget(self.title)

        self.device_groups = DEVICE_GROUPS

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)

        self.checkboxes = {}
        self.populate_groups_in_grid()

        self.main_layout.addStretch()

        self.save_button = QPushButton("Zapisz")
        self.save_button.setStyleSheet("margin-top: 10px; padding: 5px;")
        self.save_button.clicked.connect(self.save_selection)
        self.main_layout.addWidget(self.save_button)

    def populate_groups_in_grid(self):
        row = 0
        col = 0

        for group, devices in self.device_groups.items():
            group_widget = QWidget()
            group_layout = QVBoxLayout(group_widget)

            group_checkbox = QPushButton(f"Zaznacz/Odznacz grupę: {group}")
            group_checkbox.setStyleSheet("font-weight: bold;")
            group_checkbox.clicked.connect(lambda _, g=group: self.toggle_group(g))
            group_layout.addWidget(group_checkbox)

            for device in devices:
                device_checkbox = QtWidgets.QCheckBox(device)
                if device in self.selected_devices:
                    device_checkbox.setChecked(True)
                self.checkboxes[device] = device_checkbox
                group_layout.addWidget(device_checkbox)
            group_layout.addStretch()
            self.grid_layout.addWidget(group_widget, row, col)
            col += 1
            if col >= self.columns:
                col = 0
                row += 1

    def toggle_group(self, group):
        for device in self.device_groups[group]:
            checkbox = self.checkboxes[device]
            checkbox.setChecked(not checkbox.isChecked())

    def save_selection(self):
        self.selected_devices = [
            device for device, checkbox in self.checkboxes.items() if checkbox.isChecked()
        ]
        self.close()
