from NetManage.utils.commands import COMMAND, INPUT
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QPushButton, \
    QStyle
from CommandEditor.CommandEditorField import CommandEditorField
from CommandEditor.CustomValueInput import CustomValueInput
from inputs.inputs import NameInput
from utils.AnimatedToggle import AnimatedToggle
from utils.CenteredLineWidget import CenteredLineWidget
from utils.consts import ASSETS_DIR




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
        self.list_of_inputs: list[CustomValueInput] = []

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

        self.errorLabel = QLabel("Etykiety własnych kontrolek nie mogą być puste oraz nie mogą zawierac znaku \";\".")
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setStyleSheet("color: red; font-size: 12px;")
        self.errorLabel.setVisible(False)
        self.main_layout.addWidget(self.errorLabel)

        self.buttons = QHBoxLayout()

        self.close_editor_button = QPushButton("Zamknij")
        self.close_editor_button.setIcon(
            self.close_editor_button.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton))
        self.close_editor_button.setStyleSheet("margin-top:10px; padding: 5px;")
        self.close_editor_button.clicked.connect(self.handle_close)\

        self.save_command_button = QPushButton("Zapisz")
        self.save_command_button.setIcon(
            self.save_command_button.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.save_command_button.setStyleSheet("margin-top:10px; padding: 5px;")
        self.save_command_button.clicked.connect(self.save_command)

        self.save_and_run_command_button = QPushButton("Zapisz i uruchom")
        self.save_and_run_command_button.setIcon(
            self.save_and_run_command_button.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.save_and_run_command_button.setStyleSheet("margin-top:10px; padding: 5px;")
        self.save_and_run_command_button.clicked.connect(self.handle_close)

        self.buttons.addWidget(self.close_editor_button)
        self.buttons.addWidget(self.save_command_button)
        self.buttons.addWidget(self.save_and_run_command_button)

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

    def validate_custom_inputs(self):
        for input in self.list_of_inputs:
            _, label, _ = input.get_values()
            if len(label) == 0:
                self.errorLabel.setVisible(True)
                return False
        self.errorLabel.setVisible(False)
        return True

    def get_values(self) -> dict:
        is_valid = self.validate_custom_inputs()
        command_name = self.command_name.getValue()
        self.command_name.validate()
        if not is_valid:
            return {}


        values = {
            "NAME": command_name,
            "TYPE": "CONFIG" if self.toggle_mode.isChecked else "DIAGNOSTICS",
            "INPUTS": [";".join(control_details.get_values()) for control_details in self.list_of_inputs],
            "COMMANDS": self.command_editor_field.toPlainText()
        }

        return values

    def save_command(self):
        values = self.get_values()
        print(values)
        if values.get("TYPE") is None:
            print("Stop")