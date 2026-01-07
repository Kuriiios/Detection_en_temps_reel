import streamlit as st
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
from api_intermediaire.modules.db_tools import get_user_objects, get_user_id

def display_user_infos():
    user = st.session_state['user']
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**First Name:** \n{user.get('firstname', 'N/A')}")
            st.markdown(f"**Username:** \n`@{user.get('username', 'N/A')}`")
            st.markdown(f"**City:** \n{user.get('city', 'N/A')}")
            
        with col2:
            st.markdown(f"**Last Name:** \n{user.get('lastname', 'N/A')}")
            st.markdown(f"**Email:** \n{user.get('email', 'N/A')}")
            st.markdown(f"**Member Since:** \n{user.get('created_at', 'N/A')}")

def display_user_objects():
    user = st.session_state.get('user')
    if not user:
        st.error("No user found in session state.")
        return

    current_user_id = get_user_id(user['email'])

    if current_user_id:
        objects = get_user_objects(current_user_id)
        if objects:
            for obj in objects:
                with st.expander(f"📦 Object: {obj.label}"):
                    st.json({"ID": obj.id, "Details": obj.description})
        else:
            st.info("No objects linked to this user.")
    else:
        st.error("Could not retrieve User ID from database.")