# DETECTION_en_temps_reel/API_detection/api_detection.py

# --- import ---
import io
import numpy as np
from PILL import Image

from fastapi import FastAPI, UploadFile, File,  HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Union

from moduls.encoder_base64 import encode_image
from model_loader import load_model

import logging
from logging.handlers import RotatingFileHandler

# --- logging --- 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # to file
        logging.StreamHandler()           # to console
    ]
)

logger = logging.getLogger(__name__)

# --- app ---
app = FastAPI()

# --- Pydantic models ---
class ImageResponse(BaseModel):
    status: str
    image_base64: str


# --- global variables, try to load from cache----
model_path = r"cache"

try:
    model = load_model("s")
except:
    model = None

@app.post("/api/image/detection", response_model= ImageResponse)
async def describe_image(file: UploadFile = File(...)):

    global model 

# --- verification file type ---    
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logger.error("Invalid file type.")
        raise HTTPException(status_code=422, detail={"status": "422", "message": "Invalid file type. Only JPG/PNG allowed."})

# --- verification exsistance model ---
    if model is None:
        logger.error("The model isn't loaded.")
        raise HTTPException(status_code=503, detail={"status": "503", "message": "The model isn't loaded"})
    else: 
        logger.info(f"The model is loaded")

# --- lire une image ---
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img_np = np.array(img)
        logger.info(f"File is loaded")
    except Exception as e:
        logger.error(f"Invalid file: {str(e)}.")
        raise HTTPException(status_code=400, detail={"status": "400", "message": "Invalid file."})

# --- generate les resultat de detection ---
    try:   
        results = model(img_np)
        img_with_boxes = results[0].plot()
# transfomation l'image dans 
        _, buffer = cv2.imencode(".jpg", rendered)


        logger.info(f"New image with boxes are generated")
    except Exception as e:
        logger.error(f"Cannot generate new image with boxes: {str(e)}")
        raise HTTPException(status_code=400, detail={"status": "400", "message": f"Cannot generate new image with boxes: {str(e)}"})

    return {"status": "success", "image": img_plus_boxes}