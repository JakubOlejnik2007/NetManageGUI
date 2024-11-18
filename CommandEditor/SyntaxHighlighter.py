from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QFont


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlightingRules = []

        commandFormat = QTextCharFormat()
        commandFormat.setForeground(Qt.GlobalColor.green)
        commandFormat.setFontWeight(QFont.Weight.Bold)
        self.addHighlightingRules([
            "interface", "ip", "router", "enable", "disable", "show", "configure", "exit",
            "access-list", "no", "set", "logging", "hostname", "version", "copy", "reload", "write"
        ], commandFormat)

        protocolFormat = QTextCharFormat()
        protocolFormat.setForeground(Qt.GlobalColor.magenta)
        self.addHighlightingRules([
            "ospf", "bgp", "eigrp", "rip", "isis", "mpls", "tcp", "udp", "icmp", "ssh", "vrf", "ipv6"
        ], protocolFormat)

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(Qt.GlobalColor.darkCyan)
        self.highlightingRules.append((QRegularExpression(r'\b\d+\.\d+\.\d+\.\d+\b'), numberFormat))  # IP
        self.highlightingRules.append((QRegularExpression(r'\b\d+\b'), numberFormat))  # Porty i inne liczby

        argumentFormat = QTextCharFormat()
        argumentFormat.setForeground(Qt.GlobalColor.lightGray)
        self.addHighlightingRules([
            "permit", "deny", "any", "host", "log", "eq", "lt", "gt", "tcp", "udp", "range", "vlan", "name"
        ], argumentFormat)

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.GlobalColor.darkGray)
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegularExpression(r'!.*'), commentFormat))

        deviceManagementFormat = QTextCharFormat()
        deviceManagementFormat.setForeground(Qt.GlobalColor.blue)
        self.addHighlightingRules([
            "hostname", "username", "password", "enable secret", "line vty", "line con", "enable", "disable"
        ], deviceManagementFormat)

        vlanFormat = QTextCharFormat()
        vlanFormat.setForeground(Qt.GlobalColor.yellow)
        self.addHighlightingRules([
            "vlan", "vlan database", "name", "access", "trunk", "switchport", "mode", "native"
        ], vlanFormat)

        stpFormat = QTextCharFormat()
        stpFormat.setForeground(Qt.GlobalColor.cyan)

        self.addHighlightingRules([
            "spanning-tree", "stp", "rstp", "bpduguard", "portfast", "root", "bridge", "priority"
        ], stpFormat)

        routingFormat = QTextCharFormat()
        routingFormat.setForeground(Qt.GlobalColor.red)
        self.addHighlightingRules([
            "ip route", "network", "redistribute", "route-map", "access-list", "subnet", "mask"
        ], routingFormat)

    def addHighlightingRules(self, words: list[str], format: QTextCharFormat):
        for word in words:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            self.highlightingRules.append((pattern, format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)
