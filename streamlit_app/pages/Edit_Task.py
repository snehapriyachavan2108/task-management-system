import streamlit as st

from api import APIError, delete_task, get_tasks, update_task
from auth import require_login
from utils import show_message, status_label, status_value

require_login()

st.title("Edit Task")

try:
    tasks = get_tasks(st.session_state.access_token)
except APIError as exc:
    show_message("error", str(exc))
    st.stop()

if tasks:
    task_options = {f"{task.get('id')} - {task.get('title')}": task for task in tasks}
    selected_key = st.selectbox("Select task", list(task_options.keys()))
    selected_task = task_options[selected_key]

    with st.form("edit_task"):
        title = st.text_input("Title", value=selected_task.get("title", ""))
        description = st.text_area("Description", value=selected_task.get("description", ""))
        completed = st.checkbox("Completed", value=selected_task.get("completed", False))
        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Save Changes")
        deleted = col2.form_submit_button("Delete Task")

        if submitted:
            try:
                update_task(
                    st.session_state.access_token,
                    selected_task.get("id"),
                    {"title": title, "description": description, "completed": completed},
                )
                show_message("success", "Task updated successfully.")
                st.rerun()
            except APIError as exc:
                show_message("error", str(exc))

        if deleted:
            try:
                delete_task(st.session_state.access_token, selected_task.get("id"))
                show_message("success", "Task deleted successfully.")
                st.rerun()
            except APIError as exc:
                show_message("error", str(exc))
else:
    st.info("No tasks available to edit.")
