from PyQt6.QtWidgets import QHBoxLayout, QLabel, QComboBox


class ComboInput:
    def __init__(self, label, items, disabled_if_empty=True):
        self.combo_layout = QHBoxLayout()
        self.comboLabel = QLabel(label)
        self.comboLabel.setStyleSheet("""
                    margin: 10px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 0px;
                    height: 30px;
                """)
        self.combo = QComboBox()
        self.combo.addItems(items)
        self.combo.setDisabled((len(items) == 0 or items[0] == "No COM port available.") and disabled_if_empty)
        self.combo.setStyleSheet("width: 30%;")
        self.combo_layout.addWidget(self.comboLabel)
        self.combo_layout.addWidget(self.combo)

    def getLayout(self):
        return self.combo_layout

    def getValue(self):
        return self.combo.currentText()