#app_streamlit/pages/6_historique_image
import streamlit as st
import base64
import io
from PIL import Image

st.set_page_config(
    page_title="Historique",
    layout="wide"
)

st.title("Historique des images traitées")


# INITIALISATION
if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("Aucune image traitée pour le moment.")
    st.stop()


# BOUTON NETTOYER
if st.button("Vider l’historique"):
    st.session_state.history.clear()
    st.success("Historique vidé")
    st.rerun()


# AFFICHAGE DES ÉLÉMENTS
for idx, item in enumerate(reversed(st.session_state.history), start=1):

    st.divider()
    st.subheader(f"Image {idx} — {item['filename']}")

    col1, col2 = st.columns([1, 2])

    with col1:
        try:
            img_bytes = base64.b64decode(item["image_base64"])
            img = Image.open(io.BytesIO(img_bytes))
            st.image(img, use_container_width=True)
        except Exception:
            st.error("Image invalide")

    with col2:
        st.markdown("** Description générée :**")
        st.info(item.get("description", "Aucune description"))

