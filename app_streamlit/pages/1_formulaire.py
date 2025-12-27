#APP_Streamlit/pages/1_formulaire.py
import streamlit as st
from module.email_valide import email_valide
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL', '127.0.0.1')}:{os.getenv('API_INTERMEDIAIRE_PORT', '8080')}"

with st.sidebar:
    st.image("logo.png", width="stretch")
    st.divider()
    st.caption(" • YOLOv11 • BLIP • ")

st.title("Formulaire")

with st.form(key="form_utilisateur"):
    firstname = st.text_input("Nom")
    lastname = st.text_input("Prenom")
    pseudo = st.text_input("Pseudo")
    # Verification pseudo pris ou pas 
    city = st.text_input("Ville")
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")
    confirm_password = st.text_input("Confirmation du mot de passe", type="password")

    submit_button = st.form_submit_button(label="Envoyer")

    if submit_button:
        if not all([
            firstname.strip(), lastname.strip(), pseudo.strip(),city.strip(), email.strip(), password.strip(), confirm_password.strip()
        ]):                
            st.error("Tous les champs sont obligatoire")

        elif not email_valide(email):
            st.error("Format de l'adresse email invalide")

        elif password != confirm_password:
            st.error("Les mots de passe ne correspondent pas") 
        
        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "username": pseudo,
            "email": email,
            "password": password,
            "city": city
        }
        try:
            response = requests.post(f"{BASE_URL}/create-user/", json=user_data)
            if response.status_code == 200:
                result = response.json()
                if result.get("response"):
                    st.success("Compte créé avec succès !")
                else:
                    st.error("Erreur lors de la création du compte.")
            else:
                st.error(f"Erreur API : {response.status_code}")
        except Exception as e:
            st.error(f"Impossible de contacter l'API : {e}")

