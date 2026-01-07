# DETECTION_en_temps_reel/API_detection/api_detection.py

# --- import ---
import io
from datetime import datetime
import cv2
import uvicorn
import requests
import base64
import numpy as np
from PIL import Image
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from loguru import logger
load_dotenv()

from fastapi import FastAPI, UploadFile, File,  HTTPException
from pydantic import BaseModel

from api_detection.model_loader import load_model # <---------------------- import loader
from api_detection.modules.utils import convert_to_binary

import logging

API_INTERMEDIAIRE_URL = os.getenv("API_DETECTION_URL") + "/api/objects/save"

# --- logging --- 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # <-----------------------to file
        logging.StreamHandler()        
    ]
)

logger = logging.getLogger(__name__)

# --- app ---
app = FastAPI()

# --- Pydantic models ---
class ImageResponse(BaseModel):
    status: str
    image_base64: str
    result: dict


# --- global variables, try to load model: n/s/m/l/x----

try:
    model = load_model("x")
except:
    model = None

@app.post("/api/process_image", response_model= ImageResponse)
async def detection(file: UploadFile = File(...)):

    global model 

# --- verification file type ---    
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logger.error("Invalid file type.")
        raise HTTPException(status_code=422, detail={"status": "422", "image_base64": "Invalid file type. Only JPG/PNG allowed.", "result":{}})

# --- verification exsistance model ---
    if model is None:
        logger.error("The model isn't loaded.")
        raise HTTPException(status_code=503, detail={"status": "503", "image_base64": "The model isn't loaded", "result":{}})
    else: 
        logger.info(f"The model is loaded")

# --- lire une image ---
    try:
        contents = await file.read()

        logger.info(f"File is loaded")
    except Exception as e:
        logger.error(f"Invalid file: {str(e)}.")
        raise HTTPException(status_code=400, detail={"status": "400", "image_base64": "Invalid file.", "result":{}})

# --- generate les resultat de detection ---
    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img_np = np.array(img)

        results = model(img_np)
        img_with_boxes = results[0].plot()

# --- format correct ---
        if img_with_boxes.dtype != np.uint8:
            img_with_boxes = (255 * np.clip(img_with_boxes, 0, 1)).astype(np.uint8)
        img_with_boxes = cv2.cvtColor(img_with_boxes, cv2.COLOR_RGB2BGR)


# transfomation l'image avec les boites dans un text pour envoier
        success, buffer = cv2.imencode(".jpg", img_with_boxes)
        if not success:
            raise HTTPException(status_code=500, detail={"status": "500", "image_base64": "Image encoding failed.", "result":{}})

        img_base64 = base64.b64encode(buffer).decode("utf-8")

        logger.info(f"New image with boxes are generated")

# transfomation l'information suplimontaire
        r = results[0]
        
        boxes = getattr(r, "boxes", None)
        orig_shape = getattr(r, "orig_shape", img_np.shape[:2])
        speed = getattr(r, "speed", {})

        if boxes is None:
            inform = {
                "image_shape": orig_shape,
                "speed": speed,
                "detections": {"boxes": [], "scores": [], "class_name": []}
            }
        else:
            cls_list = [r.names[int(c)] for c in boxes.cls.tolist()]
            inform = {
                "image_shape": orig_shape,
                "speed": speed,
                "detections": {
                    "boxes": boxes.xyxy.cpu().tolist(),
                    "scores": boxes.conf.cpu().tolist(),
                    "class_name": cls_list
                }
            }

    except Exception as e:
        logger.error(f"Cannot generate new image with boxes: {str(e)}", )
        raise HTTPException(status_code=400, detail={"status": "400", "image_base64": f"Cannot generate new image with boxes: {str(e)}", "result":{}})
    '''
    try:
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
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

                    obj_values = {
                    "name":label,
                    "confidence":conf,
                    "img_binary":blob_data,
                    "date": datetime.today().strftime('%Y-%m-%d')
                    }

                    if blob_data:
                        response = requests.post(
                            API_INTERMEDIAIRE_URL,
                            json=obj_values,
                            timeout=15
                        )

                        if response.status_code == 200:
                            logger.info("Successfully inserted object to database")


    except Exception as e:
        logger.error(f"Cannot generate new image per boxes: {str(e)}", )
        raise HTTPException(status_code=400, detail={"status": "400", "image_base64": f"Cannot generate new image per boxes: {str(e)}", "result":{}})
    '''
    return {"status": "success", "image_base64": img_base64, "result": inform}

if __name__ == "__main__":
    try:
        port = os.getenv('API_DETECTION_PORT', '8002')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "api_detection.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )