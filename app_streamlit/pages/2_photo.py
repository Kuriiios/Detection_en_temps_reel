#APP_Streamlit/pages/1_charger_image.py
import base64
import io
import streamlit as st
import numpy as np
from PIL import Image
import cv2
import requests
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()

import logging

# --- logging --- 
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # <-----------------------to file
        logging.StreamHandler()        
    ]
)

logger = logging.getLogger(__name__)

# --- page config --- 
st.set_page_config(
    page_title="NeuroVision",
    layout="wide"
)


# paramètres d'affichage des graphiques
sns.set_theme(style="dark")

BLACK = "#0B0B0B"
RED = "#E10600"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "figure.facecolor": "none",   # прозрачный фон всей фигуры
    "axes.facecolor": "none",     # прозрачный фон области графика
    "savefig.facecolor": "none",  # прозрачный фон при сохранении
    "axes.edgecolor": WHITE,
    "axes.labelcolor": RED,
    "xtick.color": RED,
    "ytick.color": RED,
    "text.color": RED,
    "grid.color": BLACK,
    "axes.grid": False
})


# --- path API_INTERMEDIAIRE_URL ---
base_url = os.getenv("API_INTERMEDIAIRE_URL")

if not base_url:
    logger.error("API_INTERMEDIAIRE_URL n’est pas définie")
    raise RuntimeError("API_INTERMEDIAIRE_URL n’est pas définie")

API_INTERMEDIAIRE_URL = base_url.rstrip("/") + "/api/process_image"


# --- SLIDERBAR ---
with st.sidebar:
    try:
        st.image("app_streamlit/logo.png", width="stretch")
    except Exception as e:
        logger.warning("logo not loaded", exc_info=e)
        st.warning("logo indisponible")

    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")

# --- TITLE ---
try:
    st.image("app_streamlit/logo_hd.jpg", width="stretch")
except Exception as e:
        logger.warning("logo_text not loaded", exc_info=e)
        st.warning("logo_text indisponible")



# --- UNITÉ DE DESSIN DES RÉSULTATS DE CHARGEMENT ET DE DÉTECTION D'IMAGES ---

data = None
image = None

col1,col2 = st.columns( 2, gap='small', width="stretch")

with col1:
    # Vérification variable d'environnement
    if not API_INTERMEDIAIRE_URL:
        logger.error("Variable d'environnement API_INTERMEDIAIRE_URL non définie")
        st.error("Variable d'environnement API_INTERMEDIAIRE_URL non définie")
        st.stop()

    mode = st.radio("Choisir votre mode", ("Uploader une image", "Webcam"))
    # ========================================
    # MODE UPLOAD
    # ========================================
    if mode == "Uploader une image":
        picture = st.file_uploader("Charger une image", type=["jpg", "jpeg", "png"])

        if picture:
            try:
                if picture.size <= 0:
                    st.error("Fichier vide")
                else:
                    image_bytes = picture.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                    st.image(image, caption=picture.name)
                    
            except Exception as e:
                st.error(f"Impossible de lire le fichier : {e}")

    # ========================================
    # MODE WEBCAM
    # ========================================

    else:
        enable = st.checkbox("Activer la webcam")
        picture = st.camera_input("Prendre une photo", disabled=not enable)

        if picture:
            try:
                image_bytes = picture.getvalue()
                image = Image.open(io.BytesIO(image_bytes))
                img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                st.image(image, caption="Image capturée")

            except Exception as e:
                st.error(f"Impossible de lire l'image de la webcam : {e}")
            

with col2:
    # --- paramètres de configuration de la détection ---
    confidence = st.slider(
        "Seuil de confiance",
        min_value=0.1,
        max_value=1.0,
        value=(0.5, 0.9)
    )

    subcol1, subcol2 = st.columns(2, gap='small', width="stretch")

    with subcol1:
        show_labels = st.checkbox("Afficher les labels", value=True)
        show_scores = st.checkbox("Afficher les scores", value=True)

    with subcol2:
        check = st.checkbox("Afficher les results de traitement", value=True)

    if check and image is not None:
        if "access_token" not in st.session_state:
            st.error("Veuillez vous connecter pour utiliser cette fonctionnalité.")
            st.stop()
        
        token = st.session_state["access_token"]
        try:
            logger.info(f"Starting image processing: {picture.name}, type={picture.type}")
            files = {
                "file": (
                    picture.name,
                    image_bytes,
                    picture.type
                )
            }
            headers = {
                "Authorization": f"Bearer {token}"
            }
    
            response = requests.post(
                API_INTERMEDIAIRE_URL,
                files=files,
                headers=headers,
                timeout=15
            )
            logger.info("Sending image to API")

        # --- prendre response ---
            if response.status_code != 200:
                logger.error(f"API error: {response.text}")
                raise RuntimeError("Server returned an error while processing the image")

            try:
                data = response.json()
            except ValueError:
                logger.exception("Failed to decode JSON from API response")
                raise RuntimeError("Invalid JSON returned from server")

            try:
                detections = data["detection_result"]["result"]["detections"]
                boxes = detections["boxes"]
                scores = detections["scores"]
                class_names = detections["class_name"]
            except KeyError as e:
                logger.exception("Unexpected API response structure")
                raise RuntimeError(f"Missing key in response: {e}")

            # résultats de détection de rendu selon les paramètres sélectionnés
            for (x1, y1, x2, y2), conf, label in zip(boxes, scores, class_names):
                # verification accurancy
                if confidence[0] <= conf <=confidence[1]:
                    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

                    # choisir la taille de la police pour les dessins et les inscriptions
                    height, width = img.shape[:2]
                    font_scale = max(0.5, width / 1000)
                    thickness = max(1, width // 500) 
                    y_text = max(y1 - int(2 * thickness + 2), int(2 * thickness + 2))

                    # dessiner une boxes
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness)

                    # ecrire les lables et accurancy
                    if  not show_labels :
                        label = ''

                    if  not show_scores:
                        conf = ''
                    else: conf = round(conf, 2)

                    cv2.putText(img, f"{label} {conf}", (x1, y_text), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale,
                        (0, 0, 255),
                        thickness,
                        cv2.LINE_AA
                    )

            # changer le format d'image pour Streamlit 
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            st.image(img_rgb, caption="Résultat de détection", width='stretch')

        except requests.exceptions.Timeout:
            logger.exception("Timeout occurred while calling API")
            st.error("Server is not responding. Please try again later.")

        except requests.exceptions.ConnectionError:
            logger.exception("Connection error while accessing API")
            st.error("Could not connect to the server.")

        except Exception as e:
            logger.exception("Unexpected error during image processing")
            st.error(str(e))

# --- RÉSULTAT DE LA GÉNÉRATION DE TEXTE ---
if picture is not None and data:
    try:
        logger.info(f"Processing description for file: {picture.name}")

        description_result = data.get("description_result", {})
        description = description_result.get("message", "")

        if not description:
            logger.warning("No description returned from API")
            st.warning("No description available for this image.")
        else:
            logger.info("Description successfully retrieved from API")

    except Exception as e:
        logger.exception("Unexpected error while processing image description")
        st.error(f"An error occurred while generating description: {e}")

    if description:
        st.markdown(
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
                        {description}
                    </h4>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# AFFICHAGE D'INFORMATIONS SUPPLÉMENTAIRES
    df = pd.DataFrame(data['detection_result']['result']['detections'])
    df["scores"] = round(df["scores"], 2)
    df["boxes"] = df["boxes"].apply(lambda coords: [round(x) for x in coords])
    st.divider()

    if st.checkbox("Afficher des informations supplémentaires de detection", value=False):
        try:
            # Affichage le dataFrame
            st.text("Objets detectés:")
            st.dataframe(df)

            # Visualisation les grafiques
            graf1, graf2, graf3 = st.columns(3, gap = "small")

            with graf1:
                fig, ax = plt.subplots()
                sns.histplot(
                    data=df,
                    x="scores",
                    bins=20,
                    kde=True,
                    ax=ax,
                    color=RED
                )
                ax.set_title("Distribution des confiances")
                ax.set_xlabel("Confidence")
                ax.set_ylabel("Nombre d'objets")

                st.pyplot(fig)

            with graf3:
                fig, ax = plt.subplots()
                sns.countplot(
                    data=df,
                    x="class_name",
                    order=df["class_name"].value_counts().index,
                    ax=ax,
                    color=RED
                )

                ax.set_title("Nombre d'objets par classe")
                ax.set_ylabel("Count")
                ax.set_xlabel("Classe")

                st.pyplot(fig)

            with graf2:
                fig, ax = plt.subplots()

                sns.boxplot(
                    data=df,
                    y="scores",
                    x="class_name",
                    ax=ax,
                    color=RED
                )

                ax.set_title("Confidence par classe")
                ax.set_ylabel("Confidence")
                ax.set_xlabel("Classe")

                st.pyplot(fig)

            # Visualisation les metric
            st.metric("Inference (ms)", round(data['detection_result']["result"]["speed"]["inference"], 1))
            st.metric("Postprocess (ms)", round(data['detection_result']["result"]["speed"]["postprocess"], 1))

        except Exception as e:
            logging.error("Error of visualisation additional information")
            st.error(f"Error of visualisation additional information: {e}")