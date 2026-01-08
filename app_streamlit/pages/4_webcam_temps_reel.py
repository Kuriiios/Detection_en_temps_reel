#app_streamlit/pages/4_webcam_temps_reel.py

import av
import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from transformers.models.blip.processing_blip import BlipProcessor
from transformers.models.blip.modeling_blip import BlipForConditionalGeneration
from streamlit_autorefresh import st_autorefresh

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
st_autorefresh(interval=5000, key="refresh")  # 1 сек

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
        self.last_frame = None

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        try:
            img = frame.to_ndarray(format="bgr24")

            self.last_frame = img

            results = model_yolo(img, conf=self.confidence)
            img = results[0].plot()

            return av.VideoFrame.from_ndarray(img, format="bgr24")

        except Exception as e:
            logging.exception("YOLOVideoProcessor recv error")
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
    if "caption" not in st.session_state:
        st.session_state.caption = "Waiting description…"

    if "last_blip_time" not in st.session_state:
        st.session_state.last_blip_time = 0.0

    caption_box = st.empty()
    last_blip_time = 0


    if ctx and ctx.video_processor:
        frame = ctx.video_processor.last_frame
        now = time.time()

        if frame is not None:
            st.session_state.last_blip_time = now

            image = Image.fromarray(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            )

            inputs = processor(image, return_tensors="pt")
            with torch.no_grad():
                out = blip_model.generate(**inputs, max_length=40)

            st.session_state.caption = processor.decode(
                out[0], skip_special_tokens=True
            )

        caption_box.markdown(
            f"""
            <div style="display:flex; justify-content:center; margin-top:20px;">
                <div style="
                    border:2px solid #FF3B3F;
                    padding:20px;
                    border-radius:16px;
                    max-width:700px;
                    width:100%;
                ">
                    <h4 style="color:#FF3B3F; text-align:center;">
                        {st.session_state.caption}
                    </h4>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )