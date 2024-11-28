from NetManage.utils.commands import INPUT
from PyQt6.QtWidgets import QGridLayout

from inputs.base_input import BaseInput
from inputs.combo_input import ComboInput
from utils.consts import SUPPORTED_INPUTS


class CustomValueInput(INPUT):
    layout = None
    def __init__(self, id, label=None, type=None):
        super().__init__()

        self.id = id
        self.label = label or ""
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
