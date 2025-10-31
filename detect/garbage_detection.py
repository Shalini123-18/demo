import cv2
import requests
import time
import os
from datetime import datetime
from ultralytics import YOLO

# ========== CONFIGURATION ==========
BACKEND_URL = "http://127.0.0.1:5000/api/detect"  # Flask backend
SAVE_PATH = "static/detections"                   # Folder to save snapshots
CAM_INDEX = 0                                     # Webcam index (0 = default)
CONF_THRESHOLD = 0.6                              # Confidence threshold
GARBAGE_CLASSES = ["plastic", "paper", "bottle", "garbage", "waste", "trash"]  # change as per dataset

# ===================================

# Ensure snapshot directory exists
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

# Load YOLOv8 model (choose your model variant)
model = YOLO("yolov8n.pt")  # replace with your trained model if available

# Open webcam
cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Webcam started... Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame not captured. Retrying...")
        continue

    # Run YOLOv8 inference
    results = model(frame, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]

            # Filter detections
            if conf < CONF_THRESHOLD:
                continue
            if label.lower() not in GARBAGE_CLASSES:
                continue

            # Draw detection box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Save snapshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_name = f"{label}_{timestamp}.jpg"
            img_path = os.path.join(SAVE_PATH, img_name)
            cv2.imwrite(img_path, frame)

            # Send data to backend
            try:
                payload = {
                    "lat": 28.6139,   # dummy coords for now
                    "lon": 77.2090,
                    "type": label,
                    "confidence": conf,
                    "status": "uncleaned"
                }
                res = requests.post(BACKEND_URL, data=payload, timeout=3)
                if res.status_code == 200:
                    print(f"Sent to backend: {label} ({conf:.2f})")
                else:
                    print(f"Backend error: {res.status_code}")
            except Exception as e:
                print(f"Failed to send data: {e}")

            time.sleep(1)  # avoid sending too many detections per second

    # Display feed
    cv2.imshow("Garbage Detection - YOLOv8", frame)

    # Exit key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Detection stopped.")
