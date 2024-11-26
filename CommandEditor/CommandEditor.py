from NetManage.utils.commands import COMMAND, INPUT
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGridLayout, QScrollArea, QFrame, QHBoxLayout, QPushButton, \
    QStyle

from CommandEditor.CommandEditorField import CommandEditorField
from inputs.base_input import BaseInput
from inputs.combo_input import ComboInput
from inputs.inputs import NameInput
from utils.AnimatedToggle import AnimatedToggle
from utils.consts import SUPPORTED_INPUTS, ASSETS_DIR


class InputsCombo(ComboInput):
    def __init__(self):
        super().__init__()

class HorizontalLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: gray; height: 0.5px; border-radius: 100px; margin: 15px auto;")

class CenteredLineWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.line = HorizontalLine()
        self.line.setFixedWidth(456)
        layout.addWidget(self.line)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        parent_width = self.parent().width() if self.parent() else 456
        self.line.setFixedWidth(int(0.95 * parent_width))


class CustomValueInput(INPUT):
    layout = None
    def __init__(self, id, label=None, type=None):
        super().__init__()

        self.id = id
        self.label = label or ""  # Poprawka z `if not None`
        self.type = type


    def create_layout(self):
        self.layout = QGridLayout()

        self.id_input = BaseInput(disabled=True, label="ID:")
        self.id_input.setValue(self.id)
        self.layout.addLayout(self.id_input.getLayout(), 0, 0, 1, 1)

        self.label_input = BaseInput(label="Etykieta:", silent_invalid=True)
        self.label_input.setValue(self.label)
        self.layout.addLayout(self.label_input.getLayout(), 0, 1, 1, 1)
        self.label_input.input.textChanged.connect(self.modify_data)

        self.input_combo = ComboInput(label="Kontrolka:", items=SUPPORTED_INPUTS, value=self.type)

        self.input_combo.combo.currentTextChanged.connect(self.modify_data)
        self.layout.addLayout(self.input_combo.getLayout(), 1, 0, 1, 2)

    def modify_data(self):
        new_label = self.label_input.getValue()
        self.label = new_label

        new_type = self.input_combo.getValue()
        self.type = new_type

    def get_values(self) -> tuple:
        return self.id_input.getValue(), self.label_input.getValue(), self.input_combo.getValue()

    def return_layout(self) -> QGridLayout:
        self.create_layout()
        return self.layout


input11 = INPUT()
input11.read("TEXT;hostname;Nazwa hosta:")
input12 = INPUT()
input12.read("TEXT;ipv4;Adres hosta:")
inputs1 = [input11, input12]

command1 = COMMAND(
    {"NAME": "SET SOMETHING", "TYPE": "CONFIG"},
    [
        "configure terminal",
        "hostname {hostname}",
        "ip {ipv4}",
        "exit"
    ],
    ["cisco_ios", "huawei"],
    [INPUT()]
)


class CommandEditor(QWidget):
    def __init__(self, command: COMMAND = None):
        super().__init__()

        self.command = command
        self.values_keys: set[str] = set()
        self.list_of_inputs = []

        self.setWindowTitle("Edytor poleceń")
        self.setWindowIcon(QIcon(f"{ASSETS_DIR}/icon.ico"))
        self.setGeometry(100, 100, 300, 350)
        self.setFixedSize(456, 550)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        self.title = QLabel("Edytor poleceń")
        self.title.setStyleSheet("""
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                    padding: 0px;
                    width: 100%;
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
                    width: 100%;
                    height: 30px;
                """)
        self.subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setMinimumHeight(45)
        self.subtitle.setWordWrap(True)
        self.main_layout.addWidget(self.subtitle)

        self.command_name = NameInput(is_command_name=True)

        self.main_layout.addLayout(self.command_name.getLayout())

        self.mode_layout = QHBoxLayout()
        self.mode_layout.setContentsMargins(5, 5, 5, 5)

        label1 = QLabel("DIAGNOSTICS")
        label2 = QLabel("CONFIG")

        style = "margin:10px;font-weight: bold;"

        label1.setStyleSheet(style)
        label2.setStyleSheet(style)

        self.toggle_mode = AnimatedToggle()

        self.mode_layout.addStretch()
        self.mode_layout.addWidget(label1)
        self.mode_layout.addWidget(self.toggle_mode)
        self.mode_layout.addWidget(label2)
        self.mode_layout.addStretch()

        self.main_layout.addLayout(self.mode_layout)

        self.command_editor_field = CommandEditorField(self.set_set, self.print_set)
        self.main_layout.addWidget(self.command_editor_field)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")
        self.main_layout.addWidget(self.scroll_area)


        self.controls_widget = QWidget()
        self.controls_layout = QVBoxLayout(self.controls_widget)
        self.controls_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.controls_layout.setContentsMargins(0, 0, 0, 15)
        self.controls_widget.setLayout(self.controls_layout)

        self.scroll_area.setWidget(self.controls_widget)

        self.buttons = QHBoxLayout()

        self.close_editor = QPushButton("Zamknij")
        self.close_editor.setIcon(
            self.close_editor.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.close_editor.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_editor.clicked.connect(self.handle_close)\

        self.save_command = QPushButton("Zapisz")
        self.save_command.setIcon(
            self.save_command.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.save_command.setStyleSheet("margin-top:10px; padding: 5px;")
        self.save_command.clicked.connect(self.handle_close)

        self.save_and_run_command = QPushButton("Zapisz i uruchom")
        self.save_and_run_command.setIcon(
            self.save_and_run_command.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.save_and_run_command.setStyleSheet("margin-top:10px; padding: 5px;")
        self.save_and_run_command.clicked.connect(self.handle_close)

        self.buttons.addWidget(self.close_editor)
        self.buttons.addWidget(self.save_command)
        self.buttons.addWidget(self.save_and_run_command)

        self.main_layout.addLayout(self.buttons)
    def set_set(self, values_keys: set[str]):
        self.values_keys = values_keys


        self.clear_layout(self.controls_layout)


        present_inputs_ids = {input.id for input in self.list_of_inputs if input.id in values_keys}
        self.list_of_inputs = [input for input in self.list_of_inputs if input.id in values_keys]


        for key in values_keys - present_inputs_ids:
            self.list_of_inputs.append(CustomValueInput(key))

        self.insert_inputs()


    def insert_inputs(self):
        len_of_inputs = len(self.list_of_inputs)

        for idx, inpt in enumerate(self.list_of_inputs):
            self.controls_layout.addLayout(inpt.return_layout())

            if idx == len_of_inputs - 1:
                continue
            self.controls_layout.addWidget(CenteredLineWidget())

        self.controls_layout.update()
        print("Lista:", [input.id for input in self.list_of_inputs])

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def print_set(self):
        print(self.values_keys)

    def handle_close(self):
        self.close()