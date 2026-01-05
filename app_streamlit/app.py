#APP_Streamlit/app.py
import streamlit as st

pages = {
    "NeuroVision": [
        st.Page("pages/0_accueil.py", title="Description"),
    ],
    "Analyse": [
        st.Page("pages/1_formulaire.py", title="Formulaire"),
        st.Page("pages/2_charger_image.py", title="Télécharger une image"),
    ],
}

pg = st.navigation(pages)
pg.run()


