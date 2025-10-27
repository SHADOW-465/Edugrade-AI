"""
Streamlit page for configuring the application settings.

This page allows users to configure the application settings, such as the
API URL.
"""

import streamlit as st

def app():
    """
    Renders the settings page.
    """
    st.title("Settings")

    st.write("Configure the application settings below.")

    api_url = st.text_input("API URL", st.session_state.get("api_url", "http://localhost:8000/api/v1"))
    st.session_state["api_url"] = api_url

    if st.button("Save Settings"):
        st.success("Settings saved!")
