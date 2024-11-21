from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout

from CommandEditor.CommandEditorField import CommandEditorField


class CommandEditor(QWidget):
    def __init__(self):
        super().__init__()

        self.values_keys: set[str] = set()
        self.setWindowTitle("Edytor połączenia")
        self.setGeometry(100, 100, 300, 350)
        self.setWindowIcon(QIcon("assets/icon.ico"))

        self.setFixedSize(416, 550)

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)

        self.title = QLabel("Edytor poleceń")
        self.title.setStyleSheet("""
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    padding: 0px;
                    width:100%;
                    height: 30px;
                """)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(40)
        self.main_layout.addWidget(self.title)

        self.subtitle = QLabel("Wprowadź lub edytuj dane polecenia.")
        self.subtitle.setStyleSheet("""
                            text-align: center;
                            font-size: 14px;
                            font-weight: bold;
                            padding: 0px;
                            width:100%;
                            height: 30px;
                        """)
        self.subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setMinimumHeight(45)
        self.subtitle.setWordWrap(True)
        self.main_layout.addWidget(self.subtitle)

        self.command_editor_field = CommandEditorField(self.set_set, self.print_set)
        self.main_layout.addWidget(self.command_editor_field)

        self.detected_keys_label = QLabel()
        self.detected_keys_label.setWordWrap(True)
        self.main_layout.addWidget(self.detected_keys_label)

        self.setLayout(self.main_layout)

    def set_set(self, values_keys: set[str]):
        self.values_keys = values_keys
        self.detected_keys_label.setText(f"Wykryte klucze:\t{", ".join(values_keys)}")
    def print_set(self):
        print(self.values_keys)