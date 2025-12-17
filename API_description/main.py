from fastapi import FastAPI, UploadFile, File
app = FastAPI()

@app.post("/process_image")
async def process_image(img: UploadFile = File(...)):
    content = await img.read()
    return {
        "message": "Description reçue",
        "filename": img.filename,
        "size": len(content),
        "description": "Ceci est une description test"
    }
