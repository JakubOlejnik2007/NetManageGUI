from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class CommandList(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel('Lista komend')
        self.layout.addWidget(self.label)

        self.button = QPushButton('Kliknij mnie')
        self.button.clicked.connect(self.change_text)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def change_text(self):
        self.label.setText('Tekst został zmieniony!')