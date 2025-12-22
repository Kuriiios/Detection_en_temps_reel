import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL', '127.0.0.1')}:{os.getenv('API_INTERMEDIAIRE_PORT', '8080')}"

st.title('Personal Infos')

def display_infos():
    user = st.session_state['user']
    
    data = [
        ("FirstName", user.get('firstname')),
        ("LastName", user.get('lastname')),
        ("UserName", user.get('username')),
        ("Email", user.get('email')),
        ("Created at", user.get('created_at')),
        ("City", user.get('city'))
    ]
    personal_infos = pd.DataFrame(data, columns=["Property", "Value"])

    return st.table(personal_infos)

def try_auto_login():
    token = st.session_state.get("access_token")
    if not token:
        return False

    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/me", headers=headers)
        if response.status_code == 200:
            st.session_state["user"] = response.json()
            return True
        else:
            st.session_state.pop("access_token", None)
            st.session_state.pop("user", None)
            return False
    except requests.exceptions.RequestException as e:
        st.error(f"Login failed: {e}")
        return False

if "user" not in st.session_state:
    if try_auto_login():
        st.success("Auto-connected")
        display_infos()
    else:
        st.info("Please log in")
else:
    st.success(f"Welcome back, {st.session_state['user'].get('username')}!")
    display_infos()
    st.info(st.session_state["user"])
