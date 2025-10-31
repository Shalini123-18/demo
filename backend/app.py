from flask import Flask, render_template, jsonify, request
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

DB_PATH = "database.db"

# --- Initialize DB if missing ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL,
            longitude REAL,
            garbage_type TEXT,
            confidence REAL,
            status TEXT,
            image_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---

@app.route('/')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM detections ORDER BY timestamp DESC")
    detections = c.fetchall()
    conn.close()
    return render_template('dashboard.html', detections=detections)

@app.route('/api/detections', methods=['POST'])
def add_detection():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO detections (latitude, longitude, garbage_type, confidence, status, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("latitude"),
        data.get("longitude"),
        data.get("garbage_type"),
        data.get("confidence"),
        data.get("status"),
        data.get("image_path")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Detection added successfully"}), 201

@app.route('/api/detections', methods=['GET'])
def get_detections():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM detections ORDER BY timestamp DESC")
    detections = c.fetchall()
    conn.close()
    return jsonify(detections)

if __name__ == "__main__":
    app.run(debug=True)
