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

# paramètres d'affichage des graphiques
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

# sliderbar
with st.sidebar:
    st.image("app_streamlit/logo.png", width="stretch")
    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")

# path
base_url = os.getenv("API_INTERMEDIAIRE_URL")

if not base_url:
    raise RuntimeError("API_INTERMEDIAIRE_URL n’est pas définie")

API_INTERMEDIAIRE_URL = base_url.rstrip("/") + "/api/image/process"


# TITRE
st.image("app_streamlit/logo_hd.jpg")

# bloques des images
data = None
image = None
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
        min_value=0.1,
        max_value=1.0,
        value=(0.5, 0.9)
    )

    subcol1, subcol2 = st.columns(2, gap='small', width="stretch")

    with subcol1:
        show_labels = st.checkbox("Afficher les labels", value=True)
        show_scores = st.checkbox("Afficher les scores", value=True)

    with subcol2:
        check = st.checkbox("Affisher les resultats", value=False)

    # checkbox D'ENVOI
    if check and image is not None:
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


        # base64_str = data['detection_result']["image_base64"]                
        # img_bytes = base64.b64decode(base64_str)
        # img = Image.open(io.BytesIO(img_bytes))
        # st.image(img, caption="YOLO detection result")
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        detections = data['detection_result']['result']['detections']

        boxes = detections["boxes"]
        scores = detections["scores"]
        class_names = detections["class_name"]

        # img — numpy array (BGR), полученный из uploaded_file
        for (x1, y1, x2, y2), conf, label in zip(boxes, scores, class_names):
            if confidence[0] <= conf <=confidence[1]:
                x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

                height, width = img.shape[:2]
                font_scale = max(0.5, width / 1000)
                thickness = max(1, width // 500) 
                y_text = max(y1 - int(2 * thickness + 2), int(2 * thickness + 2))

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), thickness)

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



        # Streamlit ожидает RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        st.image(img_rgb, caption="Résultat de détection", use_container_width=True)


        if response.status_code != 200:
            st.error(
                f"Erreur lors de l'envoi de l'image (status {response.status_code})"
            )

if uploaded_file is not None and data:
    description = data.get('description_result', {}).get('message', '')
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


    df = pd.DataFrame(data['detection_result']['result']['detections'])
    df["scores"] = round(df["scores"], 2)
    df["boxes"] = df["boxes"].apply(lambda coords: [round(x) for x in coords])

    if st.checkbox("Afficher les results", value=True):
        st.text("Results:")
        st.dataframe(df)

        # Visualisation
        graf1, graf2, graf3 = st.columns(3, gap = "small")
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
            # --------------------------------------

        st.metric("Inference (ms)", round(data['detection_result']["result"]["speed"]["inference"], 1))
        st.metric("Postprocess (ms)", round(data['detection_result']["result"]["speed"]["postprocess"], 1))