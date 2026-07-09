import streamlit as st

from api import APIError, create_task
from auth import require_login
from utils import show_message

require_login()

st.title("Add Task")

with st.form("add_task"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    completed = st.checkbox("Completed")
    submitted = st.form_submit_button("Create Task")

    if submitted:
        if not title or not description:
            show_message("error", "Title and description are required.")
        else:
            try:
                create_task(
                    st.session_state.access_token,
                    {"title": title, "description": description, "completed": completed},
                )
                show_message("success", "Task created successfully.")
                st.rerun()
            except APIError as exc:
                show_message("error", str(exc))
