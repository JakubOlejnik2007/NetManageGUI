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
            "access-list", "no", "set", "logging", "hostname", "version", "copy", "reload", "write"
        ]
        for cmd in commands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, commandFormat))

        # Kolorowanie protokołów
        protocolFormat = QTextCharFormat()
        protocolFormat.setForeground(Qt.GlobalColor.magenta)
        protocols = [
            "ospf", "bgp", "eigrp", "rip", "isis", "mpls", "tcp", "udp", "icmp", "ssh", "vrf", "ipv6"
        ]
        for protocol in protocols:
            pattern = QRegularExpression(r'\b' + protocol + r'\b')
            self.highlightingRules.append((pattern, protocolFormat))

        # Kolorowanie adresów IP i portów
        numberFormat = QTextCharFormat()
        numberFormat.setForeground(Qt.GlobalColor.darkCyan)
        self.highlightingRules.append((QRegularExpression(r'\b\d+\.\d+\.\d+\.\d+\b'), numberFormat))  # IP
        self.highlightingRules.append((QRegularExpression(r'\b\d+\b'), numberFormat))  # Porty i inne liczby

        # Kolorowanie argumentów
        argumentFormat = QTextCharFormat()
        argumentFormat.setForeground(Qt.GlobalColor.lightGray)
        arguments = [
            "permit", "deny", "any", "host", "log", "eq", "lt", "gt", "tcp", "udp", "range", "vlan", "name"
        ]
        for arg in arguments:
            pattern = QRegularExpression(r'\b' + arg + r'\b')
            self.highlightingRules.append((pattern, argumentFormat))

        # Kolorowanie komentarzy
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.GlobalColor.darkGray)
        commentFormat.setFontItalic(True)
        self.highlightingRules.append((QRegularExpression(r'!.*'), commentFormat))

        # Kolorowanie zarządzania urządzeniem (hostname, użytkownicy, hasła)
        deviceManagementFormat = QTextCharFormat()
        deviceManagementFormat.setForeground(Qt.GlobalColor.blue)
        deviceManagementCommands = [
            "hostname", "username", "password", "enable secret", "line vty", "line con", "enable", "disable"
        ]
        for cmd in deviceManagementCommands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, deviceManagementFormat))

        # Kolorowanie VLAN i konfiguracja portów
        vlanFormat = QTextCharFormat()
        vlanFormat.setForeground(Qt.GlobalColor.yellow)
        vlanCommands = [
            "vlan", "vlan database", "name", "access", "trunk", "switchport", "mode", "native"
        ]
        for cmd in vlanCommands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, vlanFormat))

        # Kolorowanie protokołów STP (Spanning Tree Protocol)
        stpFormat = QTextCharFormat()
        stpFormat.setForeground(Qt.GlobalColor.cyan)
        stpCommands = [
            "spanning-tree", "stp", "rstp", "bpduguard", "portfast", "root", "bridge", "priority"
        ]
        for cmd in stpCommands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, stpFormat))

        # Kolorowanie routingu (np. dynamiczne protokoły routingu)
        routingFormat = QTextCharFormat()
        routingFormat.setForeground(Qt.GlobalColor.red)
        routingCommands = [
            "ip route", "network", "redistribute", "route-map", "access-list", "subnet", "mask"
        ]
        for cmd in routingCommands:
            pattern = QRegularExpression(r'\b' + cmd + r'\b')
            self.highlightingRules.append((pattern, routingFormat))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlightingRules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)
