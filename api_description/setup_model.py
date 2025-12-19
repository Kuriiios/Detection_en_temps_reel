# API_description/setup_model.py

# --- import --
import os
from transformers import BlipProcessor, BlipForConditionalGeneration

# --- path ---
CACHE_DIR = "./cache/blip"

processor_exists = os.path.exists(os.path.join(CACHE_DIR, "preprocessor_config.json"))
model_exists = os.path.exists(os.path.join(CACHE_DIR, "model.safetensors"))

# --- loading if not in cash ---
if processor_exists and model_exists:
    print(f"Model is loaded {CACHE_DIR}.")
else:
    print("Loading...")
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base",
        trust_remote_code=True,
        cache_dir=CACHE_DIR
    )
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base",
        trust_remote_code=True,
        cache_dir=CACHE_DIR
    )
    print(f"Model is loaded and saved in {CACHE_DIR}.")
