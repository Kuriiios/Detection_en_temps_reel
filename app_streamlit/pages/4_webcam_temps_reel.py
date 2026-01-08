#app_streamlit/pages/4_webcam_temps_reel.py

import av
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from transformers.models.blip.processing_blip import BlipProcessor
from transformers.models.blip.modeling_blip import BlipForConditionalGeneration

import sys
from pathlib import Path
import time
import torch
from PIL import Image
import logging

# --- logging --- 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # lire dans une fichie
        logging.StreamHandler()           # lire dans une consol
    ]
)

logger = logging.getLogger(__name__)

# --- configs --- 
st.set_page_config(page_title="Webcam YOLO – Temps réel", layout="wide")


# --- title and logo ---

st.title("Webcam YOLO – Temps réel")

# --- roots ---
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# --- loading models ---
from api_detection.model_loader import load_model

@st.cache_resource
def load_yolo():
    try:
        logger.info("Loading YOLO model...")
        model_yolo = load_model("x")
        logger.info("YOLO loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading YOLO: {e}")
        model_yolo = None
    
    return model_yolo

model_yolo = load_yolo()

@st.cache_resource
def load_blip_model():
    try:
        logger.info("Loading BLIP model...")
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        ).eval()
        logger.info("BLIP loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading BLIP: {e}")
        processor = None
        blip_model = None
        
    return processor, blip_model

processor, blip_model = load_blip_model()

class YOLOVideoProcessor(VideoProcessorBase):
    def __init__(self, confidence):
        self.confidence = confidence
        self.last_blip_time = 0
        self.last_caption = ""


    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        try:
            img = frame.to_ndarray(format="bgr24")

            # YOLO inference
            results = model_yolo(img, conf=self.confidence, stream=False)
            img_yolo = results[0].plot()

            # --- BLIP inference chaque 5 seconde ---
            current_time = time.time()

            if (
                processor is not None
                and blip_model is not None
                and current_time - self.last_blip_time >= 5
            ):
                self.last_blip_time = current_time
                # BGR → RGB → PIL
                image_pil = Image.fromarray(cv2.resize(img, (640, 480))[:, :, ::-1])

                inputs = processor(image_pil, return_tensors="pt")

                with torch.no_grad():
                    out = blip_model.generate(**inputs, max_length=50)

                self.last_caption = processor.decode(
                    out[0], skip_special_tokens=True
                )

            return av.VideoFrame.from_ndarray(img_yolo, format="bgr24")
        
        except Exception as e:
            logging.error(f"VideoProcessor error: {e}")
            st.error(f"VideoProcessor error: {e}")
            return frame

# --- slider ---
confidence = st.slider(
    "Seuil de confiance",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05
)

# 
col1, col2 = st.columns((2, 1), gap='small', width = "stretch")

# --- Detection ---
with col1:
    logger.info("Starting video processing:")
    try:
        ctx = webrtc_streamer(
            key="yolo-realtime",
            video_processor_factory=lambda: YOLOVideoProcessor(confidence),
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )
    except Exception as e:
        logger.error(f"Error starting WebRTC streamer: {e}")
        st.error(f"Cannot start video stream: {e}")

# --- Description ---
with col2:

    caption_placeholder = st.empty()

    if ctx and ctx.video_processor:
        caption = ctx.video_processor.last_caption or "Generating caption..."
        caption_placeholder.markdown(
            f"""
            <div style="display:flex; justify-content:center; margin-top:20px;">
                <div style="
                    border:2px solid #FF3B3F;
                    padding:20px;
                    border-radius:16px;
                    max-width:700px;
                    width:100%;
                ">
                    <h4 style="color:#FF3B3F; text-align:center; margin-bottom:16px;">
                        {caption}
                    </h4>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )