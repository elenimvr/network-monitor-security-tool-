import platform
import socket
import subprocess
import time


COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    8080: "HTTP Alternate"
}


def ping_device(ip):
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", ip]
    else:
        command = ["ping", "-c", "1", ip]

    start_time = time.time()

    result = subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    end_time = time.time()

    latency = round((end_time - start_time) * 1000, 2)

    if result.returncode == 0:
        return True, latency

    return False, None


def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((ip, port))
    sock.close()

    return result == 0


def detect_service(port):
    return COMMON_SERVICES.get(port, "Unknown Service")


def monitor_device(ip):
    print("=" * 40)
    print("NETWORK MONITOR")
    print("=" * 40)

    online, latency = ping_device(ip)

    print(f"Target: {ip}")

    if not online:
        print("Status: OFFLINE")
        return

    print("Status: ONLINE")
    print(f"Latency: {latency} ms")

    ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 5432, 8080]

    print("\nScanning ports...\n")

    open_ports = []

    for port in ports:
        if scan_port(ip, port):
            service = detect_service(port)
            open_ports.append(port)
            print(f"[OPEN] Port {port} - {service}")

    if not open_ports:
        print("No common open ports detected.")

    print("\nScan complete.")


target_ip = input("Enter IP address to monitor: ")

monitor_device(target_ip)
