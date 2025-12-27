import streamlit as st

st.set_page_config(
    page_title="NeuroVision",
    layout="wide"
)

st.title("NeuroVision")

with st.sidebar:
    st.image("logo.png", width="stretch")
    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")


titl1, title2 = st.columns([1, 5])
with titl1:
    st.image("logo_sq.png")

with title2:
    st.markdown(
    """
    <h1 style="
        font-size: 48px;
        color: white;
    ">
        <span style='color:white'>Neuro</span><span style='color:#FF3B3F'>Vision</span>
    </h1>
    """,
    unsafe_allow_html=True
)
    st.markdown("""
        NeuroVision est une application web interactive qui vous permet d’analyser des images à l’aide de modèles
        d’intelligence artificielle avancés. Choisissez soit votre caméra intégrée, soit téléchargez une image depuis votre ordinateur, puis explorez automatiquement ce que l’image contient grâce à nos modèles IA.
            """)


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
        """
        <div style="
            display:flex;
            justify-content:center;
            margin-top:20px;
        ">
            <div style="
                border:2px solid #FF3B3F;
                padding:20px;
                border-radius:14px;
                max-width:700px;
                width:100%;
            ">
                <h4 style="
                    color:#FF3B3F;
                    text-align:center;
                    margin-bottom:12px;
                ">
                    Exemple d’analyse en temps réel
                </h4>

                <video width="100%" controls>
                    <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
                    Votre navigateur ne supporte pas la lecture vidéo.
                </video>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

     
but1, but2 = st.columns([1, 2], gap='small', width="stretch")

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

