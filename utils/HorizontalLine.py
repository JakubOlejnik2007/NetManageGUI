from PyQt6.QtWidgets import QFrame


class HorizontalLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: gray; height: 0.5px; border-radius: 100px; margin: 15px auto;")