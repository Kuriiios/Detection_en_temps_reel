#app_streamlit/pages/2_charger_image.py
import base64
import io
import streamlit as st
from PIL import Image
import requests
import os


if "history" not in st.session_state:
    st.session_state.history = []

    
from dotenv import load_dotenv
load_dotenv()


API_INTERMEDIAIRE_URL = os.getenv("API_INTERMEDIAIRE_URL") + "/api/image/process"

# TITRE
st.title("Charger une image et envoyer aux APIs")

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

            # BOUTON D'ENVOI
            if st.button("Envoyer l'image"):
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
                    timeout=30
                )

                if response.status_code == 200:
                    st.success("Image envoyée")

                    # ============================
                    # LECTURE JSON
                    # ============================
                    try:
                        data = response.json()
                    except ValueError:
                        st.error("Réponse API invalide (JSON)")
                        st.stop()

                    # ============================
                    # SAUVEGARDE DANS L'HISTORIQUE
                    # ============================
                    try:
                        st.session_state.history.append({
                            "filename": uploaded_file.name,
                            "image_base64": data["detection_result"]["image_base64"],
                            "description": data.get("description_result", {}).get("message", "")
                        })
                        st.success("📚 Image ajoutée à l’historique")
                    except Exception as e:
                        st.warning("Impossible d’ajouter à l’historique")
                        st.exception(e)

                    # ============================
                    # AFFICHAGE RÉSULTATS
                    # ============================
                    base64_str = data["detection_result"]["image_base64"]
                    img_bytes = base64.b64decode(base64_str)
                    img = Image.open(io.BytesIO(img_bytes))
                    st.image(img, caption="YOLO detection result")

                    st.info(data["description_result"]["message"])

                else:
                    st.error(f"Erreur API (status {response.status_code})")

            
    except Exception as e:
        st.error(f"Impossible de lire le fichier : {e}")

else:
    st.warning("Sélectionner une image")