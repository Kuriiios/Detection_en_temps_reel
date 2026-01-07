#app_streamlit/pages/4_webcam_temps_reel.py

import av
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import sys
from pathlib import Path

st.title("Webcam YOLO – Temps réel")

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from api_detection.model_loader import load_model

st.set_page_config(layout="wide")


@st.cache_resource
def load_yolo():
    return load_model("x")

model = load_yolo()

class YOLOVideoProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # YOLO inference
        results = model(img, conf=0.4, stream=False)
        img = results[0].plot()

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="yolo-realtime",
    video_processor_factory=YOLOVideoProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)
