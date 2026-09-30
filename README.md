# Network Monitor & Security Tool

A Python-based network monitoring and basic security tool designed to check device availability, measure latency, scan common ports, detect services, and keep a history of scan results.

## Features

- Device online/offline detection
- Network latency measurement
- Common port scanning
- Basic service detection
- Scan logging with timestamps
- Simple and beginner-friendly Python structure

## Technologies Used

- Python
- Socket Programming
- Subprocess
- Network Monitoring
- Basic Cybersecurity Concepts
- File Logging

## How It Works

The program asks the user to enter an IP address.

It then:

1. Checks whether the device is online.
2. Measures the response latency.
3. Scans a list of common network ports.
4. Identifies common services associated with open ports.
5. Saves scan information in a log file.

## Example

```text
NETWORK MONITOR & SECURITY TOOL
---------------------------------------------

Enter IP address to monitor: 192.168.1.1

Target: 192.168.1.1
Status: ONLINE
Latency: 12.4 ms

Scanning ports...

[OPEN] Port 80 - HTTP
[OPEN] Port 443 - HTTPS

Scan complete.
