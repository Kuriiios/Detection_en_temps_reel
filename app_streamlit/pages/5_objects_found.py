import streamlit as st
from module.auto_login import try_auto_login
from module.visuals import display_user_objects
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = f"http://{os.getenv('API_BASE_URL', '127.0.0.1')}:{os.getenv('API_INTERMEDIAIRE_PORT', '8080')}"

st.title('👤 Objectedex')

if "user" not in st.session_state:
    if try_auto_login(BASE_URL):
        st.success("Auto-connected")
        display_user_objects()
    else:
        st.info("Please log in")
else:
    st.success(f"Welcome back, {st.session_state['user'].get('username')}!")
    display_user_objects()
