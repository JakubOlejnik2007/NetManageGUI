from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QPainter


class AnimatedToggle(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 20)
        self._isChecked = False
        self._offset = 5
        self.animation = QPropertyAnimation(self, b"offset")
        self.animation.setDuration(200)

    def mousePressEvent(self, event):
        self._isChecked = not self._isChecked
        self.animate()
        super().mousePressEvent(event)

    def animate(self):
        start = self.offset
        end = 20 if self._isChecked else 5
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    @property
    def isChecked(self):
        return self._isChecked

    @isChecked.setter
    def isChecked(self, value):
        if self._isChecked != value:
            self._isChecked = value
            self.animate()

    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        background_color = QColor("#dddddd" if not self._isChecked else "#3cba54")
        painter.setBrush(background_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 12, 12)


        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(self._offset, 3, 15, 15)

