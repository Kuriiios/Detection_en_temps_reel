#APP_Streamlit/pages/1_formulaire.py
import streamlit as st
from module.email_valide import email_valide
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL', '127.0.0.1')}:{os.getenv('API_INTERMEDIAIRE_PORT', '8080')}"

st.title("Formulaire connection")

with st.form(key="form_utilisateur"):
    email = st.text_input("Email")
    password = st.text_input("Mot de passe", type="password")

    submit_button = st.form_submit_button(label="Envoyer")

    user_data = {"email" : email, "password": password}
    if submit_button:
        if not all([
            email.strip(), password.strip()
        ]):                
            st.error("Tous les champs sont obligatoire")

        elif not email_valide(email):
            st.error("Format de l'adresse email invalide")

        try:
            response = requests.post(f"{BASE_URL}/login/", json=user_data)
            st.info(response.status_code)
            if response.status_code == 200:
                result = response.json()
                token = result["access_token"]
                st.session_state["access_token"] = token
                st.session_state["authenticated"] = True
                st.success("Successfully connected !")
            else:
                st.error(f"Erreur API : {response.status_code}")
        except Exception as e:
            st.error(f"Impossible de contacter l'API : {e}")


if st.session_state.get('api_result') is not None:
    if st.button(label="Sign Out"):
        headers = {
            "Authorization": f"Bearer {token['access_token']}"
        }
        response = requests.post(f"{BASE_URL}/logout/", headers=headers)

        if response.status_code == 200:
            st.session_state.pop("access_token", None)
            st.success("Logged out")
        else:
            st.error("Logout failed")
