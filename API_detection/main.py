from fastapi import FastAPI, UploadFile, File
from loguru import logger
import uvicorn
from dotenv import load_dotenv
import os
load_dotenv()

file = os.path.splitext(os.path.basename(__file__))

logger.remove()
logger.add(sink=os.getenv("LOG_PATH") + '_' +file[0] + ".log", rotation="500 MB", level="INFO")

app = FastAPI()

@app.post("/process_image")
async def process_image(img: UploadFile = File(...)):
    logger.success("Détection reçue")
    content = await img.read()
    return {
        "message": "Détection reçue",
        "filename": img.filename,
        "size": len(content),
        "detections": ["objet1", "objet2"]
    }

if __name__ == "__main__":
    try:
        port = os.getenv('API_DESCRIPTION_PORT', '8002')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "API_detection.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )
