from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QWidget, QVBoxLayout, QApplication, QPlainTextEdit, QLabel
from PyQt6.QtGui import QColor, QTextFormat, QTextCharFormat, QSyntaxHighlighter, QFont, QPainter, QTextCursor, QIcon
from PyQt6.QtCore import Qt, QRect, QRegularExpression, QSize
import sys

from CommandEditor.SyntaxHighlighter import SyntaxHighlighter


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CommandEditorField(QPlainTextEdit):
    def __init__(self, set_set, print_set, text: str = None):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        self.setFont(QFont("Courier", 11))

        self.set_set = set_set
        self.print_set = print_set

        if text is not None:
            self.setPlainText(text)

        self.highlighter = SyntaxHighlighter(self.document())

        self.textChanged.connect(self.text_changed)

    def text_changed(self):
        print("changed")
        values_keys = set()
        text = self.toPlainText()
        pattern = QRegularExpression(r"\{([^\}]+)\}")
        match_iterator = pattern.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            start = match.capturedStart()
            length = match.capturedLength()
            values_keys.add(text[start+1:start+length-1])
        self.set_set(values_keys)
        self.print_set()


    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth() * 2, 0, self.lineNumberAreaWidth(), 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        #painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.GlobalColor.white)
                painter.drawText(0, int(top), self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

