import socket

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((ip, port))
    sock.close()

    return result == 0


target_ip = "127.0.0.1"

ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3389]

print(f"Scanning {target_ip}...\n")

for port in ports:
    if scan_port(target_ip, port):
        print(f"Port {port}: OPEN")
    else:
        print(f"Port {port}: CLOSED")
