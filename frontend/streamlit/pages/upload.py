"""
Streamlit page for uploading answer sheets.

This page allows users to select an exam, enter student details, and upload
an answer sheet image for grading.
"""

import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def app():
    """
    Renders the upload page.
    """
    st.title("Upload Answer Sheet")

    # Fetch exams from the backend
    try:
        response = requests.get(f"{API_URL}/exams/")
        exams = response.json()
        exam_options = {exam['name']: exam['id'] for exam in exams}
    except requests.exceptions.ConnectionError as e:
        st.error(f"Could not connect to the API. Please make sure the backend is running. Error: {e}")
        return

    selected_exam_name = st.selectbox("Select Exam", list(exam_options.keys()))
    student_name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    uploaded_file = st.file_uploader("Choose an answer sheet image", type=["jpg", "png", "jpeg"])

    if st.button("Submit for Grading"):
        if uploaded_file is not None and selected_exam_name and student_name and student_id:
            with st.spinner("Uploading and processing..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {
                    "exam_id": exam_options[selected_exam_name],
                    "student_name": student_name,
                    "student_id": student_id,
                }

                try:
                    response = requests.post(f"{API_URL}/submissions/", files=files, data=data)
                    if response.status_code == 200:
                        st.success("Successfully submitted for grading!")
                        st.json(response.json())
                    else:
                        st.error(f"Error submitting for grading: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the API. Error: {e}")
        else:
            st.warning("Please fill out all fields and upload a file.")
