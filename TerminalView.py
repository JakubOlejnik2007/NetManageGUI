from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class TerminalView(QWidget):
    def __init__(self):
        super().__init__()

        # Ustawienie layoutu
        self.layout = QVBoxLayout()

        # Tworzenie etykiety
        self.label = QLabel('Widok terminala')
        self.layout.addWidget(self.label)

        # Tworzenie przycisku
        self.button = QPushButton('Kliknij mnie')
        self.button.clicked.connect(self.change_text)  # Połączenie sygnału z metodą
        self.layout.addWidget(self.button)

        # Ustawienie layoutu dla widgetu
        self.setLayout(self.layout)

    def change_text(self):
        # Zmiana tekstu etykiety
        self.label.setText('Tekst został zmieniony!')