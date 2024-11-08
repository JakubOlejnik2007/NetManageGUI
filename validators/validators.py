def validate_ip_list(ip: list[int]) -> bool:
    for octet in ip:
        if not 0 <= octet <= 255:
            return False
    return True

def validate_method(method: str) -> bool:
    available_methods = ["SSH", "COM", "TELNET", "TFTP"]
    return method in available_methods

def validate_sshtel_port(port: int) -> bool:
    return 0 <= port <= 65535

def validate_baudrate(baudrate: int) -> bool:
    return 0 <= baudrate <= 115200

def validate_string(string: str) -> bool:
    return len(string) > 0

def validate_com_port(port: str) -> bool:
    return port != "No COM port available."

if __name__ == '__main__':
    print(validate_sshtel_port(22))
    print(validate_sshtel_port(23523423))