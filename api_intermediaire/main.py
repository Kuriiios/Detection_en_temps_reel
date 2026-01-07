from api_intermediaire.modules.db_tools import add_new_user, sign_in, sign_out, get_user_infos, get_user_objects
from api_intermediaire.middleware.auth import get_current_user
import uvicorn
from database.data.models import User
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends
from dotenv import load_dotenv
import os
import httpx
load_dotenv()

API_DESCRIPTION_URL = os.getenv("API_DESCRIPTION_URL") + "/api/process_image"
API_DETECTION_URL = os.getenv("API_DETECTION_URL") + "/api/process_image"

app = FastAPI(title="API")

class ConnectionResponse(BaseModel):
    access_token : str
    token_type : str
    expires_in : int

class InsertResponse(BaseModel):
    response : bool

class UserRequest(BaseModel):
    firstname : str
    lastname : str
    username : str
    email : str
    password : str
    city : str

class ConnectionRequest(BaseModel):
    email : str
    password : str

class DeconnectionRequest(BaseModel):
    access_token : str

@app.get('/')
def landing_page():
    return {'Placeholder': 'Welcome'}

@app.get("/me")
def get_user(current_user: dict = Depends(get_current_user)):
    return get_user_infos(current_user)

@app.get("/objects")
def get_user(current_user: dict = Depends(get_current_user)):
    return get_user_objects(current_user)

@app.post("/create-user/", response_model = InsertResponse)
def create_user(user : UserRequest):
    response = add_new_user(user)
    return response

@app.post("/login/", response_model = ConnectionResponse)
def connection(user_connection : ConnectionRequest):
    token_response = sign_in(user_connection)
    return token_response

@app.post("/logout/", response_model = InsertResponse)
def connection(deconnection : DeconnectionRequest):
    server_response = sign_out(deconnection)
    return server_response

@app.post("/api/process_image")
async def process_image(file: UploadFile = File(...)):
    #ON VERIFIE LE TYPE
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Format incorrect")

    #LECTURE DU FICHIER
    content = await file.read()
    if len(content) <= 0:
        raise HTTPException(status_code=400, detail="Image vide")
    
    files = {"file" : (file.filename, content, file.content_type)}

    async with httpx.AsyncClient(timeout=45.0) as client:
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
        "filename": file.filename,
        "description_result": desc_result,
        "detection_result": det_result
    }

@app.post("/api/objects/save")
def save_objects():
    return None

if __name__ == "__main__":
    try:
        port = os.getenv('API_INTERMEDIAIRE_PORT', '8000')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "api_intermediaire.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )