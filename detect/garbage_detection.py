"""
YOLOv8 Garbage Detection using Webcam
Author: Spider
Description:
    - Detect garbage objects from webcam feed using YOLOv8
    - Display real-time detection results
    - Save cropped detections locally
    - (Optional) Send detection data to backend API
"""

import cv2
import time
import os
import requests
from datetime import datetime
from ultralytics import YOLO

# ==============================
# CONFIGURATION
# ==============================
MODEL_PATH = "best.pt"           # Path to your YOLOv8 trained model
SAVE_DETECTIONS = True           # Whether to save cropped detections locally
SEND_TO_API = False              # Set True when backend API is ready
API_URL = "http://127.0.0.1:5000/api/detections"
SAVE_DIR = "detections"          # Folder to save cropped detections
CONFIDENCE_THRESHOLD = 0.6       # Minimum confidence to consider valid
GPS_LAT, GPS_LON = 28.6139, 77.2090  # Approx location (replace if GPS available)

os.makedirs(SAVE_DIR, exist_ok=True)

# ==============================
# LOAD YOLOv8 MODEL
# ==============================
print("[INFO] Loading YOLOv8 model...")
model = YOLO(MODEL_PATH)
print("[INFO] Model loaded successfully!")

# ==============================
# START WEBCAM CAPTURE
# ==============================
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Could not open webcam.")
    exit()

print("[INFO] Starting detection... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Failed to read frame from webcam.")
        break

    # Run YOLOv8 inference
    results = model(frame, verbose=False)

    # Draw detections on the frame
    annotated_frame = results[0].plot()

    # Iterate through all detections
    for box in results[0].boxes:
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if conf < CONFIDENCE_THRESHOLD:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cropped = frame[y1:y2, x1:x2]

        # Save cropped detection image
        if SAVE_DETECTIONS:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{class_name}_{timestamp}.jpg"
            save_path = os.path.join(SAVE_DIR, filename)
            cv2.imwrite(save_path, cropped)
            print(f"[SAVED] {save_path}")

        # (Optional) Send detection data to backend API
        if SEND_TO_API:
            try:
                _, buffer = cv2.imencode('.jpg', cropped)
                image_bytes = buffer.tobytes()
                data = {
                    "class": class_name,
                    "confidence": conf,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "lat": GPS_LAT,
                    "lon": GPS_LON
                }
                files = {"image": (filename, image_bytes, "image/jpeg")}
                res = requests.post(API_URL, data=data, files=files, timeout=5)
                print(f"[SENT] {res.status_code}: {class_name} ({conf:.2f})")
            except Exception as e:
                print("[ERROR] Failed to send to API:", e)

    # Show detection result
    cv2.imshow("YOLOv8 Garbage Detection", annotated_frame)

    # Quit if 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("[INFO] Detection stopped. Resources released.")
