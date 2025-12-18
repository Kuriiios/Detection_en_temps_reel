from API_Intermediaire.modules.db_tools import add_new_user
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

@app.get('/')
def landing_page():
    return {'Placeholder': 'Welcome'}

@app.post("/create-user/", response_model = InsertResponse)
def create_user(user : UserRequest):
    response = add_new_user(user)
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
        "API_Intermediaire.main:app",
        reload = False,
        port = port,
        host = url,
        log_level="debug"
    )