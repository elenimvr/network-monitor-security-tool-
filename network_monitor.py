import ipaddress
import platform
import shutil
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


PORTS_TO_SCAN = list(COMMON_SERVICES.keys())


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("network_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def ping_device(ip):
    ping_command = shutil.which("ping")

    if ping_command:
        system = platform.system().lower()

        if system == "windows":
            command = [ping_command, "-n", "1", "-w", "1000", ip]
        else:
            command = [ping_command, "-c", "1", "-W", "1", ip]

        start_time = time.time()

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )

            latency = round(
                (time.time() - start_time) * 1000,
                2
            )

            if result.returncode == 0:
                return True, latency

        except (subprocess.TimeoutExpired, OSError):
            pass

    # Fallback for environments such as GitHub Codespaces
    # where the ping command may not be installed.
    for port in (53, 80, 443):
        start_time = time.time()

        try:
            with socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            ) as sock:

                sock.settimeout(1)

                result = sock.connect_ex(
                    (ip, port)
                )

            latency = round(
                (time.time() - start_time) * 1000,
                2
            )

            if result == 0:
                return True, latency

        except OSError:
            continue

    return False, None


def scan_port(ip, port):
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(0.5)

            return sock.connect_ex(
                (ip, port)
            ) == 0

    except OSError:
        return False


def detect_service(port):
    return COMMON_SERVICES.get(
        port,
        "Unknown Service"
    )


def monitor_device(ip):
    print("\n" + "=" * 50)
    print("NETWORK MONITOR & SECURITY TOOL")
    print("=" * 50)

    log_message(
        f"Started scan for {ip}"
    )

    online, latency = ping_device(ip)

    print(f"Target: {ip}")

    if not online:
        print("Status: OFFLINE")

        save_scan(
            ip_address=ip,
            status="OFFLINE",
            latency=None,
            open_ports=[]
        )

        log_message(
            f"{ip} is OFFLINE"
        )

        return

    print("Status: ONLINE")
    print(f"Latency: {latency} ms")

    log_message(
        f"{ip} is ONLINE - Latency: {latency} ms"
    )

    print(
        "\nScanning common ports...\n"
    )

    open_ports = []

    for port in PORTS_TO_SCAN:
        if scan_port(ip, port):

            service = detect_service(port)

            open_ports.append(port)

            print(
                f"[OPEN] Port {port} - {service}"
            )

            log_message(
                f"{ip} - Open port: "
                f"{port} ({service})"
            )

    if not open_ports:
        print(
            "No common open ports detected."
        )

        log_message(
            f"{ip} - No common open ports detected"
        )

    save_scan(
        ip_address=ip,
        status="ONLINE",
        latency=latency,
        open_ports=open_ports
    )

    log_message(
        f"Finished scan for {ip}"
    )

    print("\nScan complete.")


def show_history():
    history = get_scan_history()

    if not history:
        print(
            "\nNo scan history found."
        )
        return

    print("\n" + "=" * 70)
    print("LAST 10 SCANS")
    print("=" * 70)

    for scan in history:

        (
            ip_address,
            status,
            latency,
            open_ports,
            scan_time
        ) = scan

        if latency is not None:
            latency_text = f"{latency} ms"
        else:
            latency_text = "N/A"

        if open_ports:
            ports_text = open_ports
        else:
            ports_text = "None"

        print(
            f"\nDate:       {scan_time}"
        )

        print(
            f"IP:         {ip_address}"
        )

        print(
            f"Status:     {status}"
        )

        print(
            f"Latency:    {latency_text}"
        )

        print(
            f"Open Ports: {ports_text}"
        )

        print("-" * 70)


def main():
    create_database()

    while True:

        print("\n" + "=" * 50)
        print(
            "NETWORK MONITOR & SECURITY TOOL"
        )
        print("=" * 50)

        print("1. New network scan")
        print("2. View scan history")
        print("3. Exit")

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            target_ip = input(
                "Enter an IP address: "
            ).strip()

            if not validate_ip(target_ip):
                print(
                    "Invalid IP address."
                )
                continue

            monitor_device(target_ip)

        elif choice == "2":

            show_history()

        elif choice == "3":

            print("\nGoodbye!")
            break

        else:

            print(
                "Invalid option. "
                "Choose 1, 2 or 3."
            )


if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:
        print(
            "\nProgram stopped by user."
        )
