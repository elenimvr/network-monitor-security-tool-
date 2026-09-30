import platform
import subprocess
import time

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
        return "ONLINE", latency
    else:
        return "OFFLINE", None


target_ip = "8.8.8.8"

status, latency = ping_device(target_ip)

print(f"Device: {target_ip}")
print(f"Status: {status}")

if latency is not None:
    print(f"Latency: {latency} ms")
