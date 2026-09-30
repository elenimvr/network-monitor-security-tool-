import platform
import socket
import subprocess
import time
from datetime import datetime
from database import create_database, save_scan, get_scan_history

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


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("network_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


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
    print("=" * 45)
    print("NETWORK MONITOR & SECURITY TOOL")
    print("=" * 45)

    create_database()

    log_message(f"Started scan for {ip}")

    online, latency = ping_device(ip)

    print(f"Target: {ip}")

    if not online:
        print("Status: OFFLINE")

        log_message(f"{ip} is OFFLINE")

        save_scan(
            ip_address=ip,
            status="OFFLINE",
            latency=None,
            open_ports=[]
        )

        return

    print("Status: ONLINE")
    print(f"Latency: {latency} ms")

    log_message(f"{ip} is ONLINE - Latency: {latency} ms")

    ports = [
        21, 22, 23, 25, 53, 80, 110,
        139, 443, 445, 3306, 3389,
        5432, 8080
    ]

    print("\nScanning ports...\n")

    open_ports = []

    for port in ports:
        if scan_port(ip, port):
            service = detect_service(port)
            open_ports.append(port)

            print(f"[OPEN] Port {port} - {service}")

            log_message(
                f"{ip} - Open port detected: {port} ({service})"
            )

    if not open_ports:
        print("No common open ports detected.")
        log_message(f"{ip} - No common open ports detected")

    save_scan(
        ip_address=ip,
        status="ONLINE",
        latency=latency,
        open_ports=open_ports
    )

    print("\nScan complete.")

    log_message(f"Finished scan for {ip}")
    open_ports = []

    for port in ports:
        if scan_port(ip, port):
            service = detect_service(port)
            open_ports.append(port)

            print(f"[OPEN] Port {port} - {service}")

            log_message(
                f"{ip} - Open port detected: {port} ({service})"
            )

    if not open_ports:
        print("No common open ports detected.")
        log_message(f"{ip} - No common open ports detected")

    print("\nScan complete.")

    log_message(f"Finished scan for {ip}")


def show_history():
    create_database()
    history = get_scan_history()

    if not history:
        print("\nNo scan history found.")
        return

    print("\n" + "=" * 70)
    print("SCAN HISTORY")
    print("=" * 70)

    for scan in history:
        ip_address, status, latency, open_ports, scan_time = scan

        latency_text = f"{latency} ms" if latency is not None else "N/A"
        ports_text = open_ports if open_ports else "None"

        print(f"\nTime: {scan_time}")
        print(f"IP: {ip_address}")
        print(f"Status: {status}")
        print(f"Latency: {latency_text}")
        print(f"Open Ports: {ports_text}")
        print("-" * 70)


def main():
    while True:
        print("\n" + "=" * 45)
        print("NETWORK MONITOR & SECURITY TOOL")
        print("=" * 45)
        print("1. New Scan")
        print("2. View Scan History")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            target_ip = input("Enter IP address to monitor: ").strip()

            if target_ip:
                monitor_device(target_ip)
            else:
                print("Please enter a valid IP address.")

        elif choice == "2":
            show_history()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2 or 3.")


if __name__ == "__main__":
    main()
