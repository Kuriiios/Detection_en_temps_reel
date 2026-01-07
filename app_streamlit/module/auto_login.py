import streamlit as st
import requests

def try_auto_login(BASE_URL):
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
