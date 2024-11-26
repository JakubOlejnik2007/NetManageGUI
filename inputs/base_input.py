from PyQt6.QtWidgets import QLineEdit, QSizePolicy, QHBoxLayout, QVBoxLayout, QLabel

from validators.validators import validate_string


class BaseInput:
    value = None
    def __init__(self, label, default_value=None, validator=None, hide_input=False,
                 max_length=-1, disabled=False, invalid_message="Nieprawidłowy ciąg znaków.", silent_invalid=False):
        self.main_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.invalid_message = invalid_message
        self.silent_invalid = silent_invalid

        self.input = QLineEdit()

        self.main_layout.setContentsMargins(5,5,5,5)

        self.inputLabel = QLabel(label)
        self.inputLabel.setStyleSheet("""
                    margin-left: 5px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)
        self.input_layout.addWidget(self.inputLabel)

        if max_length > -1:
            self.input.setMaxLength(max_length)
        if default_value:
            self.input.setText(default_value)
        if validator:
            self.input.setValidator(validator)
        if hide_input:
            self.input.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.input.setMinimumWidth(115)
        self.input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        if disabled:
            self.input.setDisabled(True)

        self.input_layout.addWidget(self.input)

        self.input_layout.setStretch(0, 1)
        self.input_layout.setStretch(1, 1)

        self.errorLabel = QLabel()
        self.errorLabel.setStyleSheet("color: red; font-size: 10px;")
        self.errorLabel.setVisible(False)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.errorLabel)

    def getLayout(self):
        return self.main_layout

    def getValue(self):
        self.value = self.input.text()
        self.validate()
        return self.value

    def validate(self, validate_method = validate_string, invalid_message = None):
        is_valid_value = validate_method(self.value)

        if invalid_message is None:
            invalid_message = self.invalid_message

        if not is_valid_value and not self.silent_invalid:
            self.errorLabel.setText(invalid_message)
            self.errorLabel.setVisible(True)
        else:
            self.errorLabel.setVisible(False)

        return is_valid_value

    def setValue(self, value):
        self.input.setText(value)
