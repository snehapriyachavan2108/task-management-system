import streamlit as st


def show_message(kind, message):
    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    elif kind == "warning":
        st.warning(message)
    else:
        st.info(message)


def status_label(completed):
    return "Completed" if completed else "Pending"


def status_value(label):
    return label == "Completed"


def get_user_name():
    user = st.session_state.get("user") or {}
    return user.get("username") or "there"
