from collections import defaultdict
import time

failed_attempts = defaultdict(list)

THRESHOLD = 5   # attempts
TIME_WINDOW = 60  # seconds

def process_log(line):
    parts = line.split()

    try:
        ip = parts[-4]  # Extract IP (works for most SSH logs)
    except:
        return

    current_time = time.time()

from collections import defaultdict
import time

failed_attempts = defaultdict(list)

THRESHOLD = 5   # attempts
TIME_WINDOW = 60  # seconds

def process_log(line):
    parts = line.split()

    try:
        ip = parts[-4]  # Extract IP (works for most SSH logs)
    except:
        return

    current_time = time.time()

    failed_attempts[ip].append(current_time)

    # Keep only recent attempts
    failed_attempts[ip] = [
        t for t in failed_attempts[ip]
        if current_time - t <= TIME_WINDOW
    ]

    if len(failed_attempts[ip]) >= THRESHOLD:
        print(f"[ALERT] Possible brute-force attack from {ip}")
