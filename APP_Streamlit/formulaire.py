#APP_Streamlit/formulaire.py
import streamlit as st
import re

def email_valide(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def afficher_formulaire():
    with st.form(key="form_utilisateur"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prenom")
        pseudo = st.text_input("Pseudo")
        # Verification pseudo pris ou pas 
        ville = st.text_input("Ville")
        email = st.text_input("Email")
        mdp = st.text_input("Mot de passe", type="password")
        mdp_confirmation = st.text_input("Conformation du mot de passe", type="password")

        submit_button = st.form_submit_button(label="Envoyer")

        if submit_button:
            if not all([
                nom.strip(), prenom.strip(), pseudo.strip(),ville.strip(), email.strip(), mdp.strip(), mdp_confirmation.strip()
            ]):                
                st.error("Tous les champs sont obligatoire")

            elif not email_valide(email):
                st.error("Format de l'adresse email invalide")

            elif mdp != mdp_confirmation:
                st.error("Les mots de passe ne correspondent pas")

            else:
                st.success("Compte créé avec succès !")


    