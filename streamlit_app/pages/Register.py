import streamlit as st

from api import APIError
from auth import register
from utils import show_message

st.title("Register")

name = st.text_input("Full Name")
username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Create Account"):
    if not all([name, username, email, password]):
        show_message("error", "Please fill in all fields.")
    else:
        try:
            register({"name": name, "username": username, "email": email, "password": password})
            show_message("success", "Registration successful. Please log in.")
        except APIError as exc:
            show_message("error", str(exc))
