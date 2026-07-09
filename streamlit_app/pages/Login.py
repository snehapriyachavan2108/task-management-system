import streamlit as st

from api import APIError
from auth import login
from utils import show_message

st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if not username or not password:
        show_message("error", "Username and password are required.")
    else:
        try:
            login(username, password)
            show_message("success", "Login successful.")
            st.session_state.page = "Dashboard"
            st.switch_page("pages/Dashboard.py")
        except APIError as exc:
            show_message("error", str(exc))
