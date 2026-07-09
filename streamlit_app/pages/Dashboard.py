import streamlit as st

from api import APIError, get_tasks
from auth import require_login, logout
from utils import show_message, status_label

require_login()

st.title("Dashboard")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Logout"):
        logout()
        st.switch_page("pages/Login.py")
with col1:
    st.write("Welcome back")

search = st.text_input("Search tasks")
status_filter = st.selectbox("Filter by status", ["All", "Completed", "Pending"])

try:
    tasks = get_tasks(st.session_state.access_token)
except APIError as exc:
    show_message("error", str(exc))
    st.stop()

filtered = []
for task in tasks:
    title_match = search.lower() in task.get("title", "").lower()
    desc_match = search.lower() in task.get("description", "").lower()
    status_match = status_filter == "All" or status_label(task.get("completed", False)) == status_filter
    if (not search or title_match or desc_match) and status_match:
        filtered.append(task)

if filtered:
    st.dataframe(
        [
            {
                "ID": task.get("id"),
                "Title": task.get("title"),
                "Description": task.get("description"),
                "Status": status_label(task.get("completed", False)),
            }
            for task in filtered
        ],
        use_container_width=True,
    )
else:
    st.info("No tasks found.")
