from API_Intermediaire.modules.db_tools import add_new_user, add_new_object
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import os
import json
load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL')}:{os.getenv('FAST_API_PORT', '8080')}"

app = FastAPI(title="API")

class InsertResponse(BaseModel):
    response : bool

class UserRequest(BaseModel):
    firstname : str
    lastname : str
    username : str
    email : str
    password : str
    city : str

class ImageRequest(BaseModel):
    img : type

class ImageResponse(BaseModel):
    description : str
    detection : type

class ObjectRequest(BaseModel):
    name : str
    url : str

@app.get('/')
def landing_page():
    return {'Placeholder': 'Welcome'}

@app.get('/register')
def register_user():
    return {'Placeholder': "Remplir le formulaire d'entree"}

@app.post("/create-user/", response_model = InsertResponse)
def create_user(user : UserRequest):
    response = add_new_user(user)
    return response

@app.get('/sign-in')
def sign_in_user():
    return {'Placeholder': "Connection"}

@app.get('/sign-out')
def sign_in_user():
    return {'Placeholder': "Connection"}

@app.get('/select-source')
def select_source():
    return {'Placeholder': "Selectionner webcam ou image"}

@app.post('/user-infos')
def display_user_infos(token):
    return {'Placeholder': "afficher mes informations"}

@app.post('/user-objects')
def display_user_objects(token):
    return {'Placeholder': "afficher mes objets"}

@app.post('/analyse-source', response_model = ImageResponse)
def analyse_source(img : ImageRequest):
    description = requests.post(BASE_URL + '/api_description', json=img)
    detection = requests.post(BASE_URL + '/api_detection', json=img)
    response_analyse = json.dumps({"requests_api_description": description, "requests_api_detection": detection})
    return response_analyse

@app.post('/insert_oject',  response_model = InsertResponse)
def add_object(object : ObjectRequest):
    response = add_new_object(object)
    return response

if __name__ == "__main__":
    try:
        port = os.getenv('FAST_API_PORT', '8000')
        port = int(port)
        url = os.getenv('API_BASE_URL', '127.0.0.1')
    except ValueError:
        print("ERREUR")
        port = 8080

    uvicorn.run(
        "API.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )