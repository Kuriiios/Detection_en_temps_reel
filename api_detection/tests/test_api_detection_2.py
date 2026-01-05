# DETECTION_en_temps_reel/api_description/tests/test_api_description.py
import io
import cv2
import pytest
import numpy as np

import base64
from fastapi.testclient import TestClient
from api_detection.main import app
from api_detection.main import model

# --- client ---
client = TestClient(app)

# --- fake model ---
class DummyYOLO:
    def __call__(self, img):
        class Result:
            def plot(self):
                return np.zeros((100, 100, 3), dtype=np.uint8)
        return [Result()] 

@pytest.fixture(autouse=True)
def mock_model(monkeypatch):

    monkeypatch.setattr("api_detection.main.model", DummyYOLO())
    yield

# --- test api access ---
def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

def test_detect_no_file():
    response = client.post("/api/process_image")
    assert response.status_code == 422  


# --- invalid file ---
def test_detect_invalid_file():
    response = client.post(
        "/api/process_image",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 422

# --- empty file ---
def test_detect_empty_file():
    empty_bytes = io.BytesIO(b"")
    response = client.post(
        "/api/process_image",
        files={"file": ("empty.jpg", empty_bytes, "image/jpeg")}
    )
    assert response.status_code == 400

# --- test success ---
def test_detect_image_success():
    # --- fake image ---
    img_np = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)


    success, buffer = cv2.imencode(".jpg", img_np)
    assert success
    # --- creation une fiche pour envoier
    img_bytes = io.BytesIO(buffer.tobytes())

    response = client.post(
        "/api/process_image",
        files={"file": ("fake.jpg", img_bytes, "image/jpeg")}
    )

    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["status"] == "success"

    assert "image_base64" in data
    assert isinstance(data["image_base64"], str)

    decoded = base64.b64decode(data["image_base64"])
    assert len(decoded) > 0
