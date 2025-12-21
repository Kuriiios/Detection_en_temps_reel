import streamlit as st
from module.email_valide import email_valide
import requests
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL', '127.0.0.1')}:{os.getenv('API_INTERMEDIAIRE_PORT', '8080')}"

st.title('Token')

def try_auto_login():
    token = st.session_state.get("access_token")

    if not token:
        return False

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/me", headers=headers)

    if response.status_code == 200:
        st.session_state["user"] = response.json()
        return True

    st.session_state.pop("access_token", None)
    return False

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = try_auto_login()

if st.session_state["authenticated"]:
    st.success("Auto-connected")
else:
    st.info("Please log in")
