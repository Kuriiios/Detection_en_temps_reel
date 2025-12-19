# DETECTION_en_temps_reel/API_description/tests/test_api_description.py
import io
import numpy as np
import base64
from fastapi.testclient import TestClient
from api_detection.main import app


# --- client ---
client = TestClient(app)

# --- fake model ---

class DummyYOLO:
    def __call__(self, img):
        class Result:
            def plot(self):
                return np.zeros((100, 100, 3), dtype=np.uint8)
        return [Result()] 

# --- test api access ---
def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

def test_detect_no_file():
    response = client.post("/process_image")
    assert response.status_code == 422

# --- invalid file ---
def test_detect_invalid_file():
    response = client.post(
        "/process_image",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )

    assert response.status_code == 422



# --- test success ---
from PIL import Image
def test_detect_image_success():
    # Create a fake image in memory
    buf = io.BytesIO()
    Image.new('RGB', (100, 100), color='red').save(buf, format='JPEG')
    buf.seek(0)

    response = client.post(
        "/process_image",
        files={"file": ("test.jpg", buf, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "image_base64" in data
    assert isinstance(data["image_base64"], str)

    # Проверяем, что это реально Base64
    decoded = base64.b64decode(data["image_base64"])
    assert len(decoded) > 0
