'''

@app.post("/api/objects/save")
def save_objects(file: UploadFile = File(...)):


'''
import cv2
import sqlite3 # Using SQLite as an example

def convert_to_binary(image_array):
    # Encode the image into a buffer (memory) instead of saving to disk
    success, encoded_image = cv2.imencode('.jpg', image_array)
    if success:
        return encoded_image.tobytes() # This is the BLOB format
    return None

import sqlite3
import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

# --- DATABASE SETUP ---
conn = sqlite3.connect('detections.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS object_crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT,
        confidence REAL,
        image_blob BLOB
    )
''')
conn.commit()

# --- DETECTION AND STORAGE ---
model = YOLO("yolo11x.pt")
img_path = 'dev_test.png'

# Load using PIL as you requested
pil_img = Image.open(img_path).convert("RGB")
img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

results = model.predict(img)

for r in results:
    for box in r.boxes:
        label = model.names[int(box.cls[0])]
        conf = float(box.conf[0])
        
        # Get coordinates and crop
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = img[y1:y2, x1:x2]
        
        if crop.size > 0:
            # Convert to binary
            blob_data = convert_to_binary(crop)
            
            if blob_data:
                # Insert into Database
                cursor.execute(
                    "INSERT INTO object_crops (label, confidence, image_blob) VALUES (?, ?, ?)",
                    (label, conf, blob_data)
                )
                print(f"✅ Saved {label} to database.")

conn.commit()
conn.close()