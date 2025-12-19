# DETECTION_en_temps_reel/API_description/tests/test_api_description.py

import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from API_description.main import app
from API_description import main

# --- client ---
client = TestClient(app)

# --- fake model ---
class DummyProcessor:
    def __call__(self, *args, **kwargs):
        return {"pixel_values": "fake"}

    def decode(self, *args, **kwargs):
        return "a cat"

class DummyModel:
    def generate(self, *args, **kwargs):
        return [[1, 2, 3]]


# --- test api access ---
def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

# --- test model loading ---
def test_model_not_loaded(monkeypatch):

    monkeypatch.setattr(main, "processor", None)
    monkeypatch.setattr(main, "model", None)

    # --- fake image ---
    img = Image.new("RGB", (10, 10), color="red")
    file = io.BytesIO()
    img.save(file, format="JPEG")
    file.seek(0)

    response = client.post(
        "/process_image",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 503

# --- test file type ---
def test_invalid_media_type():
    file = io.BytesIO(b"not an image")
    response = client.post(
        "/process_image",
        files={"file": ("test.txt", file, "text/plain")}
    )

    assert response.status_code == 422


# --- test status and exsitsens message in case of success ---
def test_success(monkeypatch):

    monkeypatch.setattr(main, "processor", DummyProcessor())
    monkeypatch.setattr(main, "model", DummyModel())

    # --- fake image ---
    img = Image.new("RGB", (10, 10), color="red")
    file = io.BytesIO()
    img.save(file, format="JPEG")
    file.seek(0)

    response = client.post(
        "/process_image",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert "message" in body