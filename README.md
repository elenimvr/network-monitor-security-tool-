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
