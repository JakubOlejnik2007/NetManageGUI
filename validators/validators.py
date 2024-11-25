def validate_ip_list(ip: list[int]) -> bool:
    for octet in ip:
        if not 0 <= octet <= 255:
            return False
    return True

def validate_subnet_list(subnet: list[int]) -> bool:
    for idx, octet in enumerate(subnet):
        if not 0 <= octet <= 255:
            return False
        if idx > 0 and subnet[idx] > subnet[idx - 1]:
            return False
    return True

def validate_method(method: str) -> bool:
    available_methods = ["SSH", "COM", "TELNET", "TFTP"]
    return method in available_methods

def validate_sshtel_port(port: int) -> bool:
    if type(port) != int:
        port = int(port)
    return 0 <= port <= 65535

def validate_baudrate(baudrate: int) -> bool:
    if type(baudrate) != int:
        baudrate = int(baudrate)
    return 0 <= baudrate <= 115200

def validate_string(string: str) -> bool:
    return len(string) > 0

def validate_com_port(port: str) -> bool:
    return port != "No COM port available."

if __name__ == '__main__':
    print(validate_sshtel_port(22))
    print(validate_sshtel_port(23523423))