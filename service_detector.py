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


def detect_service(port):
    return COMMON_SERVICES.get(port, "Unknown Service")


ports_to_check = [22, 80, 443, 3306, 3389]

for port in ports_to_check:
    service = detect_service(port)
    print(f"Port {port}: {service}")
