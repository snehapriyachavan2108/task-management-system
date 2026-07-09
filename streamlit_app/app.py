# import streamlit as st

# from auth import is_logged_in, logout
# from config import APP_SUBTITLE, APP_TITLE

# st.set_page_config(page_title=APP_TITLE, page_icon="✅", layout="wide")

# st.sidebar.title(APP_TITLE)
# st.sidebar.write(APP_SUBTITLE)

# if is_logged_in():
#     st.sidebar.button("Logout", on_click=logout)

# st.sidebar.markdown("---")
# st.sidebar.write("Navigate using the pages on the left.")

# st.title(APP_TITLE)
# st.write(APP_SUBTITLE)

# if not is_logged_in():
#     st.info("Use the Login page to access your tasks.")
# else:
#     st.success("You are logged in and can manage tasks.")

import streamlit as st

from auth import is_logged_in, logout
from config import APP_SUBTITLE, APP_TITLE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="✅",
    layout="wide"
)

# ---------------- Sidebar ----------------

st.sidebar.title("📋 " + APP_TITLE)
st.sidebar.write(APP_SUBTITLE)

if is_logged_in():
    st.sidebar.success("Logged in")
    st.sidebar.button("🚪 Logout", on_click=logout)
else:
    st.sidebar.warning("Not Logged In")

st.sidebar.markdown("---")
st.sidebar.caption("Navigate using the pages on the left.")

# ---------------- Home Page ----------------

st.title("📋 TaskFlow")
st.subheader("Simple, Secure & Smart Task Management System")

st.write("""
Manage your daily tasks efficiently using a secure FastAPI backend
and a clean Streamlit interface.
""")

st.markdown("---")

if not is_logged_in():
    st.info("👈 Please Login or Register from the sidebar to start managing your tasks.")
else:
    st.success("🎉 Welcome back! You are logged in and can manage your tasks.")
