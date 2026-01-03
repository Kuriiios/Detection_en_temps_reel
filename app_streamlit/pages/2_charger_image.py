#APP_Streamlit/pages/1_charger_image.py
import base64
import io
import streamlit as st
from PIL import Image
import requests
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()

sns.set_theme(style="dark")

BLACK = "#0B0B0B"
RED = "#E10600"
WHITE = "#FFFFFF"

plt.rcParams.update({
    "figure.facecolor": RED,
    "axes.facecolor": BLACK,
    "savefig.facecolor": BLACK,
    "axes.edgecolor": WHITE,
    "axes.labelcolor": RED,
    "xtick.color": RED,
    "ytick.color": RED,
    "text.color": RED,
    "grid.color": BLACK,
    "axes.grid": False
})

with st.sidebar:
    st.image("app_streamlit/logo.png", width="stretch")
    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")


base_url = os.getenv("API_INTERMEDIAIRE_URL")

if not base_url:
    raise RuntimeError("API_INTERMEDIAIRE_URL n’est pas définie")

API_INTERMEDIAIRE_URL = base_url.rstrip("/") + "/api/image/process"

data = None


# TITRE
st.image("app_streamlit/logo_hd.jpg")

col1,col2 = st.columns( 2, gap='small', width="stretch")

with col1:
    # Vérification variable d'environnement
    if not API_INTERMEDIAIRE_URL:
        st.error("Variable d'environnement API_INTERMEDIAIRE_URL non définie")
        st.stop()

    # UPLOAD IMAGE
    uploaded_file = st.file_uploader(
        "Charger une image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        try:
            #Vérification du type
            # if uploaded_file.type not in ["image/jpeg", "image/png", "image/jpg"]:
            #     st.error("Format de fichier non supporté. Veuillez charger un JPG ou PNG.")
            
            # Vérification taille > 0
            if uploaded_file.size <= 0:
                st.error("Fichier vide")
            else:
                # Lecture image
                image_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(image_bytes))

                # Affichage image
                st.image(image, caption=uploaded_file.name)
        except Exception:
            st.error("Impossible de lire le fichier")

    else:
        st.warning("Sélectionner une image")


with col2:
    confidence = st.slider(
        "Seuil de confiance",
        0.1, 1.0, 0.5
    )

    subcol1, subcol2 = st.columns(2, gap='small', width="stretch")

    with subcol1:
        show_labels = st.checkbox("Afficher les labels", value=True)
        show_scores = st.checkbox("Afficher les scores", value=True)

    with subcol2:
        check = st.checkbox("Envoyer l'image", value=False)

    # BOUTON D'ENVOI
    if check:
        files = {
            "file": (
                uploaded_file.name,
                image_bytes,
                uploaded_file.type
            )
        }

        response = requests.post(
            API_INTERMEDIAIRE_URL,
            files=files,
            timeout=15
        )
        data = response.json()


        base64_str = data['detection_result']["image_base64"]                
        img_bytes = base64.b64decode(base64_str)
        img = Image.open(io.BytesIO(img_bytes))
        st.image(img, caption="YOLO detection result")


        if response.status_code != 200:
            st.error(
                f"Erreur lors de l'envoi de l'image (status {response.status_code})"
            )

if uploaded_file is not None and data is not None:
    st.info(data['description_result']['message'])

    df = pd.DataFrame(data['detection_result']['result']['detections'])
    df["scores"] = round(df["scores"], 2)
    df["boxes"] = round(df["scores"], 2)

    if st.checkbox("Afficher les results", value=True):
        st.text("Results:")
        st.dataframe(df)

        # Visualisation
        graf1, graf2 = st.columns(2, gap = "small")
        with graf1:
            # --------------------------------------
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
            # --------------------------------------
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
            # --------------------------------------

            st.metric("Inference (ms)", round(data['detection_result']["result"]["speed"]["inference"], 1))
            st.metric("Postprocess (ms)", round(data['detection_result']["result"]["speed"]["postprocess"], 1))