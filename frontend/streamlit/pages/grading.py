"""
Streamlit page for displaying grading results.

This page allows users to enter a submission ID and view the grading
results for that submission.
"""

import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000/api/v1")

def app():
    """
    Renders the grading results page.
    """
    st.title("Grading Results")

    submission_id = st.text_input("Enter Submission ID to view results")

    if st.button("Get Results"):
        if submission_id:
            with st.spinner("Fetching results..."):
                try:
                    response = requests.get(f"{API_URL}/submissions/{submission_id}")
                    if response.status_code == 200:
                        submission_data = response.json()
                        st.write(f"**Student:** {submission_data['student_name']} ({submission_data['student_id']})")
                        st.write(f"**Status:** {submission_data['status']}")

                        grade_response = requests.get(f"{API_URL}/grades/{submission_id}")
                        if grade_response.status_code == 200:
                            grades = grade_response.json()
                            for grade in grades:
                                with st.expander(f"Question {grade['question_number']} - Score: {grade['score']}/{grade['max_score']}"):
                                    st.text_area("Extracted Text", grade['extracted_text'], height=150)
                                    st.info(f"**Feedback:** {grade['feedback']}")
                                    st.warning(f"**Reasoning:** {grade['reasoning']}")

                                    # Teacher override section
                                    st.subheader("Teacher Override")
                                    new_score = st.number_input("New Score", value=grade['score'], key=f"score_{grade['id']}")
                                    reason = st.text_input("Reason for Override", key=f"reason_{grade['id']}")
                                    if st.button("Override Grade", key=f"override_{grade['id']}"):
                                        override_data = {"new_score": new_score, "reason": reason}
                                        override_response = requests.put(f"{API_URL}/grades/{grade['id']}/override", json=override_data)
                                        if override_response.status_code == 200:
                                            st.success("Grade overridden successfully!")
                                        else:
                                            st.error(f"Failed to override grade: {override_response.text}")
                        else:
                            st.error(f"Could not fetch grades for this submission. Error: {grade_response.text}")
                    else:
                        st.error(f"Could not find submission with ID {submission_id}. Error: {response.text}")
                except requests.exceptions.ConnectionError as e:
                    st.error(f"Could not connect to the API. Error: {e}")
        else:
            st.warning("Please enter a Submission ID.")
