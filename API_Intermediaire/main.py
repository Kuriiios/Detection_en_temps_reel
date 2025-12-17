#API_Intermediaire/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

API_DESCRIPTION_URL = os.getenv("API_DESCRIPTION_URL")
API_DETECTION_URL = os.getenv("API_DETECTION_URL")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is running"}


@app.post("/api/image/process")
async def process_image(img: UploadFile = File(...)):
    #ON VERIFIE LE TYPE
    if img.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Format incorrect")

    #LECTURE DU FICHIER
    content = await img.read()
    if len(content) <= 0:
        raise HTTPException(status_code=400, detail="Image vide")
    
    files = {"img" : (img.filename, content, img.content_type)}

    async with httpx.AsyncClient() as client:
        try:
            #ENVOIE API DESCRIPTION
            response_desc = await client.post(API_DESCRIPTION_URL, files=files)
            response_desc.raise_for_status()
            desc_result = response_desc.json()

            #ENVOIE API DETECTION
            response_det = await client.post(API_DETECTION_URL, files=files)
            response_det.raise_for_status()
            det_result = response_det.json()

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de connexion aux APIs : {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Erreur HTTP lors de l'appel aux APIs : {e}")
        
    return {
        "message": "Image envoyée aux APIs",
        "filename": img.filename,
        "description_result": desc_result,
        "detection_result": det_result
    }
