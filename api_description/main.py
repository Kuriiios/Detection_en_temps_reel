#api_description/main.py

# --- import ---
from fastapi import FastAPI, UploadFile, File,  HTTPException
import io
from PIL import Image
from pydantic import BaseModel
from typing import Union
import uvicorn
from dotenv import load_dotenv
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import logging

load_dotenv()

# --- logging --- 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # запись в файл
        logging.StreamHandler()           # вывод в консоль
    ]
)

logger = logging.getLogger(__name__)

# --- app ---
app = FastAPI()

# --- Pydantic models ---
class ImageDescriptionResponse(BaseModel):
    status: str
    message: str


# --- global variables, try to load from cache----


try:
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
except:
    processor = None
    model = None
 


# --- endpoints ---
@app.post("/process_image", response_model=Union[ImageDescriptionResponse, dict])
async def describe_image(file: UploadFile = File(...)):

    global processor, model 

# --- verification file type ---    
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        logger.error("Invalid file type.")
        raise HTTPException(status_code=422, detail={"status": "422", "message": "Invalid file type. Only JPG/PNG allowed."})

# --- verification exsistance model ---
    if processor is None or model is None:
        logger.error("Model isn't loading.")
        raise HTTPException(status_code=503, detail={"status": "503", "message": "Model isn't loading"})
    else: 
        logger.info(f"Model is loaded")

# --- lire une image ---
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        logger.info(f"File is loaded")
    except Exception as e:
        logger.error(f"Empty file: {str(e)}.")
        raise HTTPException(status_code=400, detail={"status": "400", "message": "Invalid file."})

# --- generate description ---
    try:   
        inputs = processor(images=img, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)
        logger.info(f"Description is generated")
    except Exception as e:
        logger.error(f"Cannot generate text description: {str(e)}")
        raise HTTPException(status_code=400, detail={"status": "400", "message": f"Cannot generate text description: {str(e)}"})

    return {"status": "success", "message": caption}


if __name__ == "__main__":
    try:
        port = os.getenv('API_DESCRIPTION_PORT', '8001')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "api_description.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )