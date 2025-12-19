# DETECTION_en_temps_reel/API_detection/api_detection.py

# --- import ---
import io
import cv2
import base64
import numpy as np
from PIL import Image
from pathlib import Path

from fastapi import FastAPI, UploadFile, File,  HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union

from API_detection.model_loader import load_model # <---------------------- import loader

import logging
from logging.handlers import RotatingFileHandler

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


# --- global variables, try to load model: n/s/m/l/x----

try:
    model = load_model("s")
except:
    model = None

@app.post("/api/image/detection", response_model= ImageResponse)
async def detection(file: UploadFile = File(...)):

    global model 

# --- verification file type ---    
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logger.error("Invalid file type.")
        raise HTTPException(status_code=422, detail={"status": "422", "image_base64": "Invalid file type. Only JPG/PNG allowed."})

# --- verification exsistance model ---
    if model is None:
        logger.error("The model isn't loaded.")
        raise HTTPException(status_code=503, detail={"status": "503", "image_base64": "The model isn't loaded"})
    else: 
        logger.info(f"The model is loaded")

# --- lire une image ---
    try:
        contents = await file.read()

        logger.info(f"File is loaded")
    except Exception as e:
        logger.error(f"Invalid file: {str(e)}.")
        raise HTTPException(status_code=400, detail={"status": "400", "image_base64": "Invalid file."})

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
            raise HTTPException(status_code=500, detail={"status": "500", "image_base64": "Image encoding failed."})

        img_base64 = base64.b64encode(buffer).decode("utf-8")

        logger.info(f"New image with boxes are generated")

    except Exception as e:
        logger.error(f"Cannot generate new image with boxes: {str(e)}")
        raise HTTPException(status_code=400, detail={"status": "400", "image_base64": f"Cannot generate new image with boxes: {str(e)}"})

    return {"status": "success", "image_base64": img_base64}