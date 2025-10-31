import sqlite3, os

db_path = os.path.join(os.path.dirname(__file__), "database.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    confidence REAL,
    status TEXT,
    latitude REAL,
    longitude REAL,
    image_path TEXT,
    timestamp TEXT
)''')

conn.commit()
conn.close()
print("✅ Database initialized successfully.")