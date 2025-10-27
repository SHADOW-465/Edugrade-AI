"""
Main application file for the EduGrade AI Streamlit frontend.

This file initializes the Streamlit application, sets up the page
configuration, and handles the navigation between the different pages.
"""

import streamlit as st
from pages import upload, grading, analytics, settings

# Set page configuration
st.set_page_config(
    page_title="EduGrade AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload", "Grading", "Analytics", "Settings"])

# Page routing
if page == "Upload":
    upload.app()
elif page == "Grading":
    grading.app()
elif page == "Analytics":
    analytics.app()
elif page == "Settings":
    settings.app()
