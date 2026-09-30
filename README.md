# Network Monitor & Security Tool

A Python-based network monitoring and basic security application that checks device availability, measures latency, scans common TCP ports, detects common services, stores scan results in SQLite, and keeps a local activity log.

## Features

- Check whether a device is ONLINE or OFFLINE
- Measure network latency
- Scan common TCP ports
- Detect common services such as HTTP, HTTPS, SSH and FTP
- Validate IP addresses
- Store scan results in an SQLite database
- View the latest 10 scan results
- Save activity logs with timestamps
- Interactive command-line menu
- Cross-platform ping support for Windows, Linux and macOS

## Technologies

- Python
- SQLite
- Socket Programming
- TCP/IP Networking
- Subprocess
- IP Address Validation
- File Logging

## Project Structure

```text
network-monitor-security-tool/
│
├── network_monitor.py
├── database.py
├── port_scanner.py
├── service_detector.py
├── requirements.txt
└── README.md
## How to Run

Clone the repository:

```bash
git clone https://github.com/elenimvr/network-monitor-security-tool.git
```

Open the project folder:

```bash
cd network-monitor-security-tool
```

Run the application:

```bash
python network_monitor.py
```

## Main Menu

```text
==================================================
NETWORK MONITOR & SECURITY TOOL
==================================================

1. New network scan
2. View scan history
3. Exit
```

## Example Scan

```text
Enter an IP address: 192.168.1.1

Target: 192.168.1.1
Status: ONLINE
Latency: 8.42 ms

Scanning common ports...

[OPEN] Port 80 - HTTP
[OPEN] Port 443 - HTTPS

Scan complete.
```

## Database

Scan results are automatically stored in an SQLite database.

Each scan stores:

- IP address
- Device status
- Latency
- Open ports
- Date and time

## Logging

The application creates a local `network_log.txt` file containing timestamped monitoring activity.

## Purpose

This project was developed to practice practical Python networking concepts including socket programming, TCP/IP monitoring, port scanning, service identification, SQLite data persistence and application logging.

## Future Improvements

- Graphical dashboard
- Automatic network device discovery
- Continuous monitoring
- Desktop or email alerts
- Exportable reports
- Network statistics and charts

## Disclaimer

This tool is intended for educational purposes and for use only on networks and devices that you own or have permission to test.


