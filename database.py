import sqlite3
from datetime import datetime


DB_NAME = "network_monitor.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            status TEXT NOT NULL,
            latency REAL,
            open_ports TEXT,
            scan_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_scan(ip_address, status, latency, open_ports):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scans (
            ip_address,
            status,
            latency,
            open_ports,
            scan_time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        ip_address,
        status,
        latency,
        ",".join(map(str, open_ports)),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
