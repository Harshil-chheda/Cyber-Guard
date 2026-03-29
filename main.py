from monitor import detect_port_scan, monitor_ssh_logs
from scapy.all import sniff
import threading

# Replace with your network interface (check with `ip a`)
NETWORK_INTERFACE = "wlan0"  

# -----------------------------
# Start packet sniffer
# -----------------------------
def start_sniffer():
    sniff(iface=NETWORK_INTERFACE, filter="tcp", prn=detect_port_scan, store=0)

# -----------------------------
# Main
# -----------------------------
def main():
    print("[*] Starting Cyber Guard IPS...")

    # SSH monitor thread
    t1 = threading.Thread(target=monitor_ssh_logs, daemon=True)
    t1.start()

    # Packet sniffer runs in main thread
    start_sniffer()

if __name__ == "__main__":
    main()
