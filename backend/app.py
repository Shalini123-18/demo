from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Dummy garbage detection data
detections = [
    {"id": 1, "lat": 28.6139, "lon": 77.2090, "status": "critical", "address": "Connaught Place, Delhi",
     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "image_url": "https://cdn-icons-png.flaticon.com/512/679/679922.png"},
    {"id": 2, "lat": 28.7041, "lon": 77.1025, "status": "pending", "address": "Karol Bagh, Delhi",
     "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "image_url": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route("/api/garbage")
def get_garbage():
    return jsonify(detections)

@app.route("/api/route")
def get_route():
    return jsonify({"path": [[28.6139, 77.2090], [28.7041, 77.1025]]})

@app.route("/api/alert", methods=["POST"])
def send_alert():
    return jsonify({"message": "Alert sent successfully to MCD officials!"})

if __name__ == "__main__":
    app.run(debug=True)
