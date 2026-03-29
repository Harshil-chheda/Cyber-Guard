import time
from collections import defaultdict
from scapy.all import TCP, IP, sniff
import os
import threading

# -----------------------------
# Config
# -----------------------------
PORT_THRESHOLD = 1      # unique ports threshold
TIME_WINDOW = 1000        # seconds window
SSH_THRESHOLD = 3       # failed login attempts
SSH_TIME_WINDOW = 60    # seconds
DEBUG_MODE = True
ALERT_LOG_FILE = "alerts.log"

# Trackers
port_scan_tracker = defaultdict(list)
ssh_attempts_tracker = defaultdict(list)
blocked_ips = set()

# -----------------------------
# Port Scan Detection
# -----------------------------
def detect_port_scan(packet):
    if packet.haslayer(TCP) and packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport

        if DEBUG_MODE:
            print(f"DEBUG: Packet from {src_ip} to port {dst_port}")

        current_time = time.time()
        port_scan_tracker[src_ip].append((dst_port, current_time))

        # Keep recent entries
        port_scan_tracker[src_ip] = [
            (p, t) for (p, t) in port_scan_tracker[src_ip]
            if current_time - t <= TIME_WINDOW
        ]

        unique_ports = set(p for (p, t) in port_scan_tracker[src_ip])

        if len(unique_ports) >= PORT_THRESHOLD and src_ip not in blocked_ips:
            alert_msg = f"[ALERT] Port scan detected from {src_ip}"
            print(alert_msg)
            log_alert(alert_msg)
            block_ip(src_ip)

# -----------------------------
# SSH Brute Force Detection
# -----------------------------
def monitor_ssh_logs():
    auth_log = "/var/log/auth.log"
    print("[*] Starting SSH brute-force monitor...")
    with open(auth_log, "r") as f:
        # Seek to end of file
        f.seek(0,2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            check_ssh_line(line)

def check_ssh_line(line):
    # Example: "Failed password	 for invalid user"
    if "Failed password" in line:
        parts = line.split()
        try:
            ip_index = parts.index("from") + 1
            src_ip = parts[ip_index]
        except ValueError:
            return

        current_time = time.time()
        ssh_attempts_tracker[src_ip].append(current_time)

        # Keep only recent attempts
        ssh_attempts_tracker[src_ip] = [
            t for t in ssh_attempts_tracker[src_ip]
            if current_time - t <= SSH_TIME_WINDOW
        ]

        if len(ssh_attempts_tracker[src_ip]) >= SSH_THRESHOLD and src_ip not in blocked_ips:
            alert_msg = f"[ALERT] SSH brute-force detected from {src_ip}"
            print(alert_msg)
            log_alert(alert_msg)
            block_ip(src_ip)

# -----------------------------
# Logging
# -----------------------------
def log_alert(message):
    with open(ALERT_LOG_FILE, "a") as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f"{timestamp} {message}\n")

# -----------------------------
# Auto-block IP
# -----------------------------
def block_ip(ip):
    print(f"[BLOCK] Blocking IP {ip}")
    blocked_ips.add(ip)
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
