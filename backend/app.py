from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, type, confidence, status, latitude, longitude, image_path, timestamp FROM detections")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    return jsonify(get_data())

@app.route('/static/detections/<path:filename>')
def serve_detection_image(filename):
    return send_from_directory(os.path.join(app.static_folder, 'detections'), filename)

if __name__ == '__main__':
    app.run(debug=True)
