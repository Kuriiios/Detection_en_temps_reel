#APP_Streamlit/formulaire.py
import streamlit as st
def afficher_formulaire():
    with st.form(key="form_utilisateur"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prenom")
        pseudo = st.text_input("Pseudo")
        email = st.text_input("Email")
        mdp = st.text_input("Mot de passe", type="password")
        mdp_confirmation = st.text_input("Conformation du mot de passe", type="password")

        submit_button = st.form_submit_button(label="Envoyer")


    