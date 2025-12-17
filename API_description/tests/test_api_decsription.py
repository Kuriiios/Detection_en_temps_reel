import io
import pytest
from fastapi.testclient import TestClient
from api_description import app


# --- client ---
client = TestClient(app)

# --- test api access ---
def test_docs_available():
    response = client.get("/docs")
    assert response.status_code == 200

# --- test model loading ---
def test_model_not_loaded(monkeypatch):

    monkeypatch.setattr(api_description, "processor", None)
    monkeypatch.setattr(main, "model", None)

    file = io.BytesIO(b"fake image")
    response = client.post(
        "/api/image/description",
        files={"file": ("test.jpg", file, "image/jpeg")}
    )

    assert response.status_code == 503
    assert response.json()["status"] == "loading"

# --- test file type ---
def test_invalid_media_type():
    file = io.BytesIO(b"not an image")
    response = client.post(
        "/api/image/description",
        files={"file": ("test.txt", file, "text/plain")}
    )

    assert response.status_code == 422