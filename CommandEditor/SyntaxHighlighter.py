from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QFont


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightingRules = []

        # Kolorowanie podstawowych poleceń routera
        commandFormat = QTextCharFormat()
        commandFormat.setForeground(Qt.GlobalColor.green)
        commandFormat.setFontWeight(QFont.Weight.Bold)
        commands = [
            "interface", "ip", "router", "enable", "disable", "show", "configure", "exit",
            "access-list", "no", "set", "logging", "hostname", "version"
        ]
        for cmd in commands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, commandFormat))

        protocolFormat = QTextCharFormat()
        protocolFormat.setForeground(Qt.GlobalColor.magenta)
        protocols = [
            "ospf", "bgp", "eigrp", "rip", "isis", "mpls", "tcp", "udp", "icmp", "ssh"
        ]
        for protocol in protocols:
            pattern = QRegularExpression(r'\b' + protocol + r'\b')
            self.highlightingRules.append((pattern, protocolFormat))

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(Qt.GlobalColor.darkCyan)
        self.highlightingRules.append((QRegularExpression(r'\b\d+\.\d+\.\d+\.\d+\b'), numberFormat))  # IP
        self.highlightingRules.append((QRegularExpression(r'\b\d+\b'), numberFormat))  # Porty i inne liczby

        argumentFormat = QTextCharFormat()
        argumentFormat.setForeground(Qt.GlobalColor.darkGreen)
        arguments = [
            "permit", "deny", "any", "host", "log", "eq", "lt", "gt", "tcp", "udp"
        ]
        for arg in arguments:
            pattern = QRegularExpression(r'\b' + arg + r'\b')
            self.highlightingRules.append((pattern, argumentFormat))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.GlobalColor.darkGray)
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegularExpression(r'!.*'), commentFormat))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)
