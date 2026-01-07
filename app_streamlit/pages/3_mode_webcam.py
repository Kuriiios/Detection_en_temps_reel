# APP_Streamlit/pages/3_mode_webcam.py
import base64
import io
import streamlit as st
from PIL import Image
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_INTERMEDIAIRE_URL = os.getenv("API_INTERMEDIAIRE_URL")
if API_INTERMEDIAIRE_URL:
    API_INTERMEDIAIRE_URL += "/api/process_image"

st.title("Mode temps réel : upload ou webcam")

# Vérification variable d'environnement
if not API_INTERMEDIAIRE_URL:
    st.error("Variable d'environnement API_INTERMEDIAIRE_URL non définie")
    st.stop()

# Choix du mode
mode = st.radio("Choisir votre mode", ("Uploader une image", "Webcam"))

# ========================================
# MODE UPLOAD
# ========================================
if mode == "Uploader une image":
    uploaded_file = st.file_uploader("Charger une image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        try:
            if uploaded_file.size <= 0:
                st.error("Fichier vide")
            else:
                image_bytes = uploaded_file.read()
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption=uploaded_file.name)

                if st.button("Envoyer l'image"):
                    files = {
                        "file": (uploaded_file.name, image_bytes, uploaded_file.type)
                    }
                    try:
                        response = requests.post(API_INTERMEDIAIRE_URL, files=files, timeout=30)

                        st.write("Status code:", response.status_code)

                        if response.status_code == 200:
                            st.success("Image envoyée avec succès")
                            data = response.json()

                            # Affichage YOLO si disponible
                            if "detection_result" in data and "image_base64" in data['detection_result']:
                                base64_str = data['detection_result']["image_base64"]
                                img_bytes = base64.b64decode(base64_str)
                                img = Image.open(io.BytesIO(img_bytes))
                                st.image(img, caption="Résultat détection YOLO")

                            # Affichage description si disponible
                            if "description_result" in data:
                                st.info(data['description_result'].get('message', 'Description reçue'))
                        else:
                            st.error(f"Erreur API (status {response.status_code})")

                    except requests.exceptions.RequestException as e:
                        st.error(f"Erreur de connexion à l'API : {e}")

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
            st.image(image, caption="Image capturée")

            if st.button("Envoyer l'image capturée"):
                files = {
                    "file": ("webcam.jpg", image_bytes, "image/jpeg")
                }
                try:
                    response = requests.post(API_INTERMEDIAIRE_URL, files=files, timeout=30)

                    #st.write("Status code:", response.status_code)
                    #st.write("Response text:", response.text)

                    if response.status_code == 200:
                        st.success("Image webcam envoyée avec succès")
                        data = response.json()

                        # Affichage YOLO si disponible
                        if "detection_result" in data and "image_base64" in data['detection_result']:
                            base64_str = data['detection_result']["image_base64"]
                            img_bytes = base64.b64decode(base64_str)
                            img = Image.open(io.BytesIO(img_bytes))
                            st.image(img, caption="Résultat détection YOLO")

                        # Affichage description si disponible
                        if "description_result" in data:
                            st.info(data['description_result'].get('message', 'Description reçue'))
                    else:
                        st.error(f"Erreur API (status {response.status_code})")

                except requests.exceptions.RequestException as e:
                    st.error(f"Erreur de connexion à l'API : {e}")

        except Exception as e:
            st.error(f"Impossible de lire l'image de la webcam : {e}")
