# Cyber Guard IPS

**Cyber Guard** is a mini Intrusion Detection & Prevention System (IDS/IPS) built with Python.  
It monitors **port scans** and **SSH brute-force attacks** in real-time and provides a **live web dashboard** to view alerts and blocked IPs.

---

## 🚀 Features

- Real-time **port scan detection** with alerts and auto-blocking
- **SSH brute-force detection** with alerts
- Live **web dashboard** to monitor:
  - Recent alerts
  - Currently blocked IPs
- Configurable thresholds for detection
- Logs alerts to `alerts.log` for auditing
- Modular and resume-friendly Python code
- Works on **Kali Linux** or other Linux systems with root privileges

---

## 🛠️ Technology Stack

- **Python 3**  
- **Scapy** – packet sniffing and TCP analysis  
- **Flask** – live web dashboard  
- **iptables** – blocking malicious IPs  
- **Kali Linux** – tested environment  

---

---

## ⚡ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<Harshil-chheda>/cyber-guard-ips.git
cd cyber-guard-ips

### 2. Create a Python Environment 

```bash
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

```bash
pip install -r requirements.txt

### 4 Run the main file 

```bash 
sudo python main.py

### 5 Start the dashboard 

```bash
python dashboard.py
http://localhost:5000 

---
---
## Testing The system

## 1 Port Scan test 
nmap -p 22,80,443 <your-IP>
or 
nmap -p- -T4 <your-ip>

## 2 SSH Brute-Force Test
ssh fakeuser@<your-IP>


