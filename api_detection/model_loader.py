#api_detection/model_loader.py
from pathlib import Path
from ultralytics import YOLO

# --- dossier pour cache ---
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

def load_model(version: str):
    """
    Load YOLO model with caching in project folder
    """
    model_path = CACHE_DIR / f"yolo12{version}.pt"

    if model_path.exists():
        # load local
        model = YOLO(str(model_path))
    else:
        # load from official Ultralytics
        model = YOLO(f"yolo12{version}.pt")
        model.save(model_path)  

    return model
