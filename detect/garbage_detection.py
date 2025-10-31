import cv2
import sqlite3
import os
from datetime import datetime
from ultralytics import YOLO

# === PATH SETUP ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "backend", "database.db")
SAVE_DIR = os.path.join(BASE_DIR, "..", "backend", "static", "detections")
os.makedirs(SAVE_DIR, exist_ok=True)

# === YOLO MODEL LOAD ===
print("🔄 Loading YOLOv8 Waste Detection Model...")
# Option 1: Load from Hugging Face or Roboflow (online model)
# model = YOLO('turhancan97/yolov8-segment-trash-detection')

# Option 2: Load your locally downloaded model
model = YOLO(os.path.join(BASE_DIR, "yolov8m-seg.pt"))
print("✅ YOLOv8 Waste Detection model loaded successfully.")

# === CAMERA INIT ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("❌ Could not open webcam. Try a different camera index or check permissions.")

print("🎥 Webcam feed started... Press 'q' to quit.")

# === DETECTION LOOP ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Frame not captured, retrying...")
        continue

    # Run YOLO detection
    results = model.predict(source=frame, conf=0.6, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]  # e.g., "plastic", "metal", etc.

            # Draw bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # === SAVE DETECTION TO DATABASE ===
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            filename = f"detection_{timestamp.replace(':', '-')}.jpg"
            filepath = os.path.join(SAVE_DIR, filename)
            cv2.imwrite(filepath, frame)

            relative_path = f"static/detections/{filename}"

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO detections (type, confidence, status, latitude, longitude, image_path, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (label, conf, "uncleaned", 28.6139, 77.2090, relative_path, timestamp))
            conn.commit()
            conn.close()
            print(f"💾 Saved detection: {label} ({conf:.2f})")

    cv2.imshow("Garbage Detection - YOLOv8", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🛑 Exiting detection loop.")
        break

cap.release()
cv2.destroyAllWindows()
