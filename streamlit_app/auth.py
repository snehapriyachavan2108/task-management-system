import streamlit as st

from api import APIError, login_user, register_user


def is_logged_in():
    return bool(st.session_state.get("access_token"))


def require_login():
    if not is_logged_in():
        st.warning("Please log in to continue.")
        st.stop()


def logout():
    st.session_state.pop("access_token", None)
    st.session_state.pop("user", None)
    st.session_state.pop("tasks", None)


def login(username, password):
    try:
        response = login_user(username, password)
    except APIError as exc:
        raise APIError(str(exc)) from exc

    token = response.get("token")
    if not token:
        raise APIError("Authentication failed.")

    st.session_state.access_token = token
    st.session_state.user = {"username": username}
    return token


def register(payload):
    try:
        return register_user(payload)
    except APIError as exc:
        raise APIError(str(exc)) from exc
