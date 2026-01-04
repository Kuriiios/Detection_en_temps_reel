import streamlit as st
import base64

st.set_page_config(
    page_title="NeuroVision",
    layout="wide"
)

with st.sidebar:
    st.image("app_streamlit/logo.png", width="stretch")
    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")


# TITLE
st.image("app_streamlit/logo_text.png", width="stretch")


col1,col2 = st.columns( [1, 2], gap='small', width="stretch")

with col1:

    st.markdown("""
        ### Détection d’objets
                
        Nous utilisons YOLOv11, un modèle de détection d’objets en temps réel, pour identifier et localiser automatiquement plusieurs objets dans une image.
        Le modèle met en évidence les objets détectés avec des boîtes englobantes et des étiquettes descriptives.

        ### Génération de descriptions textuelles

        Grâce à un modèle de génération de texte Hugging Face (Salesforce/blip-image-captioning-base) , l’application produit une description naturelle et complète de ce qui est visible dans l’image.
        Cela vous permet de comprendre rapidement le contenu visuel sans lecture manuelle détaillée.
                """)


with col2:
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
                    Exemple d’analyse en temps réel
                </h4>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.image("app_streamlit/exemp.png", width="stretch")

     
but1, but2, but3 = st.columns(3, gap='small', width="stretch")

with but2:
    button1 = st.checkbox("Comment ça marche")
    if button1:
        st.markdown("""
            - Sélectionnez la source d’image
                - Caméra en direct
                - Téléchargement depuis l’ordinateur
            - Envoyez l’image au système d’analyse
            - Visualisez les résultats
                - Objets détectés avec leurs scores de confiance
                - Description textuelle générée automatiquement
            - Explorez et téléchargez les résultats
            """)

with but1:

    button2 = st.checkbox("Technologies utilisées")

    if button2:
        st.markdown(
            """
            <div style="display:flex; gap:20px;">
                <div style="border:1px solid #FF3B3F; padding:15px; border-radius:10px;">
                    <h4 style="color:#FF3B3F;">YOLOv11</h4>
                    <p style="color:#FF3B3F;">Détection d’objets en temps réel</p>
                    <a href="https://github.com/ultralytics/ultralytics" target="_blank">Documentation</a>
                </div>
                <div style="border:1px solid #FFFFFF; padding:15px; border-radius:10px;">
                    <h4>BLIP</h4>
                    <p>Génération de descriptions d’images</p>
                    <a href="https://huggingface.co/Salesforce/blip-image-captioning-base" target="_blank">
                    Hugging Face
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True, width="stretch"
        )

with but3:

    button3 = st.checkbox("Paramètres disponibles")

    if button3:
        st.markdown(
            """
                - Choisir accurancy
                - Afficher les labels
                - Afficher les scores
                - Afficher les resultes de detection
                    - objects
                    - boxes
                    - accurancy
                    - distributions
            """)
