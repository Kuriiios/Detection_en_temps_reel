from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.post("/process_image")
async def process_image(img: UploadFile = File(...)):
    content = await img.read()
    return {
        "message": "Détection reçue",
        "filename": img.filename,
        "size": len(content),
        "detections": ["objet1", "objet2"]
    }
