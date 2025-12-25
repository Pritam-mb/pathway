"""
Mock Medical News Site - Simulates WHO/FDA alerts
This Flask app serves as a controllable external data source for demo purposes.
"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# State file to persist alerts
STATE_FILE = Path(__file__).parent / "alerts_state.json"

# Initialize with baseline data
DEFAULT_ALERTS = [
    {
        "id": 1,
        "date": "2025-12-20",
        "source": "WHO",
        "title": "Routine Monitoring Update",
        "content": "All monitored medications remain within acceptable safety parameters. No action required.",
        "severity": "info"
    },
    {
        "id": 2,
        "date": "2025-12-22",
        "source": "FDA",
        "title": "Annual Cardiac Care Guidelines",
        "content": "Standard cardiac care protocols remain effective. Continue current prescribing practices.",
        "severity": "info"
    }
]


def load_alerts():
    """Load alerts from state file or return defaults"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_ALERTS


def save_alerts(alerts):
    """Save alerts to state file"""
    with open(STATE_FILE, 'w') as f:
        json.dump(alerts, f, indent=2)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/alerts')
def alerts_page():
    """Main alerts page - this is what Pathway scrapes"""
    alerts = load_alerts()
    return render_template('alerts.html', alerts=alerts)


@app.route('/api/alerts')
def get_alerts():
    """JSON endpoint for alerts"""
    alerts = load_alerts()
    return jsonify(alerts)


@app.route('/api/trigger_warning', methods=['POST'])
def trigger_warning():
    """Add a critical warning (used for demo)"""
    alerts = load_alerts()
    
    new_alert = {
        "id": len(alerts) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "source": "WHO",
        "title": "⚠️ URGENT: Drug-X Safety Alert",
        "content": "WARNING: Recent studies indicate Drug-X (Cardioxin) shows increased risk of cardiac arrhythmia in patients over 65 years old. Immediate review of all prescriptions recommended. Risk factors include: age >65, existing cardiac conditions, concurrent use of beta-blockers.",
        "severity": "critical"
    }
    
    alerts.insert(0, new_alert)  # Add to top
    save_alerts(alerts)
    
    return jsonify({"status": "success", "alert": new_alert})


@app.route('/api/reset', methods=['POST'])
def reset_alerts():
    """Reset to baseline state"""
    save_alerts(DEFAULT_ALERTS)
    return jsonify({"status": "success", "message": "Alerts reset to baseline"})


if __name__ == '__main__':
    # Initialize state file if it doesn't exist
    if not STATE_FILE.exists():
        save_alerts(DEFAULT_ALERTS)
    
    from config.settings import settings
    print(f"🌐 Mock Medical News Site running on http://localhost:{settings.mock_site_port}")
    print(f"📄 Alerts page: http://localhost:{settings.mock_site_port}/alerts")
    app.run(host='0.0.0.0', port=settings.mock_site_port, debug=True)
