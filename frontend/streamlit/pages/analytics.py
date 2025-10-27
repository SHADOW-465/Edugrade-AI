"""
Streamlit page for displaying analytics.

This page allows users to select an exam and view analytics for that exam,
such as the class average, score distribution, and common errors.
"""

import streamlit as st
import requests
import os
import plotly.express as px
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def app():
    """
    Renders the analytics page.
    """
    st.title("Analytics Dashboard")

    # Fetch exams from the backend
    try:
        response = requests.get(f"{API_URL}/exams/")
        exams = response.json()
        exam_options = {exam['name']: exam['id'] for exam in exams}
    except requests.exceptions.ConnectionError as e:
        st.error(f"Could not connect to the API. Error: {e}")
        return

    selected_exam_name = st.selectbox("Select Exam to View Analytics", list(exam_options.keys()))

    if st.button("Load Analytics"):
        if selected_exam_name:
            exam_id = exam_options[selected_exam_name]
            with st.spinner("Loading analytics..."):
                try:
                    response = requests.get(f"{API_URL}/analytics/exam/{exam_id}")
                    if response.status_code == 200:
                        analytics_data = response.json()

                        st.metric(label="Class Average", value=f"{analytics_data['class_average']:.2f}%")

                        st.subheader("Score Distribution")
                        dist_df = pd.DataFrame(analytics_data['distribution'].items(), columns=['Score Range', 'Number of Students'])
                        fig = px.bar(dist_df, x='Score Range', y='Number of Students', title="Score Distribution")
                        st.plotly_chart(fig)

                        st.subheader("Common Errors")
                        for error in analytics_data['common_errors']:
                            st.write(f"- {error}")
                    else:
                        st.error(f"Could not load analytics for this exam. Error: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the API. Error: {e}")
