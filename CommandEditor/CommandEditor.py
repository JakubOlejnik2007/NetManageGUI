from NetManage.utils.commands import COMMAND, INPUT
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout

from CommandEditor.CommandEditorField import CommandEditorField
from inputs.base_input import BaseInput
from inputs.combo_input import ComboInput
from inputs.inputs import ConnnameInput
from utils.consts import SUPPORTED_INPUTS, ASSETS_DIR


class InputsCombo(ComboInput):
    def __init__(self):
        super().__init__()

class CustomValueInput(INPUT):
    def __init__(self, id, label = None, type = None):
        super().__init__()

        self.id = id
        self.label = label if not None else ""
        self.type = type

        self.layout = QGridLayout()

        self.id_input = BaseInput(disabled=True, label="ID:")
        self.id_input.setValue(self.id)

        self.layout.addLayout(self.id_input.getLayout(), 0, 0, 1, 1)

        self.label_input = BaseInput(label=" Etykieta:")
        self.label_input.setValue(self.label)
        self.layout.addLayout(self.label_input.getLayout(), 0, 1, 1, 1)

        self.input_combo = ComboInput(label="Kontrolka:\t", items=SUPPORTED_INPUTS, value=self.type)

        self.layout.addLayout(self.input_combo.getLayout(), 1, 0, 1, 2)

    def get_values(self) -> tuple:
        return self.id_input.getValue(), self.label_input.getValue(), self.input_combo.getValue()

    def return_layout(self) -> QGridLayout:
        return self.layout

input11 = INPUT()
input11.read("TEXT;hostname;Nazwa hosta:")
input12 = INPUT()
input12.read("TEXT;ipv4;Adres hosta:")
inputs1 = [
    input11, input12
]
command1 = COMMAND(
    {"NAME": "SET SOMETHING", "TYPE": "CONFIG"},
    [
        "configure terminal",
        "hostname {hostname}",
        "ip {ipv4}",
        "exit"
    ],
    [
        "cisco_ios", "huawei"
    ],
    [
        INPUT()
    ]
)

class CommandEditor(QWidget):
    list_of_inputs = []
    def __init__(self, command: COMMAND = None):
        super().__init__()

        self.command = command

        self.values_keys: set[str] = set()
        self.setWindowTitle("Edytor połączenia")
        self.setGeometry(100, 100, 300, 350)
        self.setWindowIcon(QIcon(f"{ASSETS_DIR}/icon.ico"))

        self.setFixedSize(456, 550)

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

        self.controls_layout = QVBoxLayout()
        self.main_layout.addLayout(self.controls_layout)

    def set_set(self, values_keys: set[str]):
        self.values_keys = values_keys
        self.detected_keys_label.setText(f"Wykryte klucze:\t{", ".join(values_keys)}")

        self.clear_layout(self.controls_layout)

        present_inputs_ids = []

        for input in self.list_of_inputs:
            if input.id not in values_keys:
                self.list_of_inputs.remove(input)
                continue
            present_inputs_ids.append(input.id)

        for key in values_keys:
            if key not in present_inputs_ids:
                self.list_of_inputs.append(CustomValueInput(key))
        print("Lista", self.list_of_inputs)
        for inpt in self.list_of_inputs:
            print("Exec", inpt.id)
            self.controls_layout.addLayout(inpt.return_layout())

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def print_set(self):
        print(self.values_keys)