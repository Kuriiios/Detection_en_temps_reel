#APP_Streamlit/app.py
import streamlit as st

pages = {
    "NeuroVision": [
        st.Page("pages/0_accueil.py", title="Description"),
    ],
    "Analyse": [
        st.Page("pages/2_charger_image.py", title="Télécharger une image"),
    ],
    "Utilisateur": [
        st.Page("pages/1_formulaire.py", title="Formulaire"),
        st.Page("pages/3_connection.py", title="Login"),
        st.Page("pages/4_user_infos.py", title="Informations utilisateur"),
        st.Page("pages/5_objects_found.py", title="Objects utilisateur"),
    ],
}

pg = st.navigation(pages)
pg.run()


