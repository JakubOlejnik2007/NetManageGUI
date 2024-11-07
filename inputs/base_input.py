from PyQt6.QtWidgets import QLineEdit, QSizePolicy, QHBoxLayout, QLabel


class BaseInput:
    def __init__(self, label, default_value=None, validator=None, hide_input=False, input_type=QLineEdit, max_length=-1):
        self.input_layout = QHBoxLayout()
        self.inputLabel = QLabel(label)
        self.inputLabel.setStyleSheet("""
                    margin: 10px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)
        self.input_layout.addWidget(self.inputLabel)

        self.input = input_type()
        if isinstance(self.input, QLineEdit):
            if max_length > -1:
                self.input.setMaxLength(max_length)
            if default_value:
                self.input.setText(default_value)
            if validator:
                self.input.setValidator(validator)
            if hide_input:
                self.input.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
            self.input.setMinimumWidth(150)
            self.input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_layout.addWidget(self.input)

        self.input_layout.setStretch(0, 1)
        self.input_layout.setStretch(1, 1)

    def getLayout(self):
        return self.input_layout

    def getValue(self):
        return self.input.text()