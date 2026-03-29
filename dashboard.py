from flask import Flask, render_template
from monitor import blocked_ips, ALERT_LOG_FILE

app = Flask(__name__)

# -----------------------------
# Home page showing alerts
# -----------------------------
@app.route("/")
def home():
    # Read alerts from log file
    try:
        with open(ALERT_LOG_FILE, "r") as f:
            alerts = f.readlines()[-20:]  # last 20 alerts
    except FileNotFoundError:
        alerts = []

    return render_template("dashboard.html", alerts=alerts, blocked_ips=list(blocked_ips))

# -----------------------------
# Run Flask server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
