from socket import AF_INET, SOCK_STREAM, socket


def get_first_open_port(from_port: int):
    """Get the first open port from an origin port."""
    port = from_port
    while not is_port_open(port):
        port += 1
    return port


def get_open_ports(ports: [int]):
    """Filter open ports."""
    res = []
    for port in ports:
        if is_port_open(port):
            res.append(port)
    return res


def is_port_open(port: int):
    """Indicates if the port is open."""
    sock = socket(AF_INET, SOCK_STREAM)
    address = ('localhost', port)
    res = sock.connect_ex(address)
    return not res == 0
