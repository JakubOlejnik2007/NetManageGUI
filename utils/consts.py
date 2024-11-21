import os
import sys

SUPPORTED_DEVICES = [
    'cisco_ios', 'cisco_xe', 'cisco_asa', 'cisco_nxos', 'cisco_iosxr', 'arista_eos', 'juniper',
    'hp_procurve', 'dell_force10', 'brocade', 'fortinet', 'mikrotik', 'huawei', 'checkpoint', 'paloalto'
]

BASE_DIR = (
    os.path.dirname(os.path.dirname(sys.executable))
    if hasattr(sys, "frozen")
    else os.path.dirname(os.path.dirname(__file__))
)
CONNECTIONS_DIR = os.path.join(BASE_DIR, "connections")
COMMANDS_DIR = os.path.join(BASE_DIR, "commands")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

SUPPORTED_INPUTS = ["TEXT", "PASS", "PORT", "IPv4", "SUBNET"]