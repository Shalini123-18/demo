import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create table for garbage detections
cursor.execute("""
CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL,
    longitude REAL,
    status TEXT,
    garbage_type TEXT,
    detection_id TEXT,
    image_path TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully with 'detections' table.")
