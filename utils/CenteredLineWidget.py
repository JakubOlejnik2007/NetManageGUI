from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from utils.HorizontalLine import HorizontalLine


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