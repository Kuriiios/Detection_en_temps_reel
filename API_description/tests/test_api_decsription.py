# DETECTION_en_temps_reel/API_description/tests/test_api_description.py

import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from API_description.api_description import app
from API_description import api_description

# --- client ---
client = TestClient(app)

# --- fake model ---
class DummyProcessor:
    def __call__(self, *args, **kwargs):
        return {"pixel_values": "fake"}

    def decode(self, *args, **kwargs):
        return "a cat"

class DummyModel:знеш
    def generate(self, *args, **kwargs):
        return [[1, 2, 3]]


# --- test api access ---
def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

# --- test model loading ---
def test_model_not_loaded(monkeypatch):

    monkeypatch.setattr(api_description, "processor", None)
    monkeypatch.setattr(api_description, "model", None)

    # --- fake image ---
    img = Image.new("RGB", (10, 10), color="red")
    file = io.BytesIO()
    img.save(file, format="JPEG")
    file.seek(0)

    response = client.post(
        "/api/image/description",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 503

# --- test file type ---
def test_invalid_media_type():
    file = io.BytesIO(b"not an image")
    response = client.post(
        "/api/image/description",
        files={"file": ("test.txt", file, "text/plain")}
    )

    assert response.status_code == 422


# --- test status and exsitsens message in case of success ---
def test_success(monkeypatch):

    monkeypatch.setattr(api_description, "processor", DummyProcessor())
    monkeypatch.setattr(api_description, "model", DummyModel())

    # --- fake image ---
    img = Image.new("RGB", (10, 10), color="red")
    file = io.BytesIO()
    img.save(file, format="JPEG")
    file.seek(0)

    response = client.post(
        "/api/image/description",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "success"
    assert "message" in body