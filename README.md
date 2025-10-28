# EduGrade AI

EduGrade AI is a multi-agent automated grading platform for handwritten answer sheets. It uses a combination of computer vision, AI LLMs (Google Gemini), advanced OCR (DeepSeek-OCR, TrOCR), and blockchain credentialing (DevDock) to provide accurate grades and personalized feedback.

## Features

- **Template-Based Alignment**: Uses template-based geometric registration for robust alignment of answer sheets.
- **Automated Grading**: Automatically grades handwritten answer sheets using Google Gemini.
- **Personalized Feedback**: Provides personalized feedback for each student.
- **Fact-Checking**: Uses Perplexity for real-time fact-checking.
- **Blockchain Credentialing**: Stores immutable grades on the DevDock blockchain.
- **Teacher Dashboard**: A dashboard for teachers to review and override grades.
- **Firebase Integration**: Uses Firebase for the database.
- **Streamlit Frontend**: A Streamlit frontend for rapid prototyping and hackathons.
- **Next.js Frontend (in progress)**: A Next.js frontend for production use.

## System Architecture

The system is composed of the following agents:

- **Preprocessing Agent**: Performs template-based alignment, deskewing, denoising, and binarization of the images.
- **Segmentation Agent**: Detects the answer boxes in the image and crops them out.
- **OCR Agent**: An ensemble of DeepSeek-OCR, TrOCR, and Gemini Vision for accurate OCR.
- **Grading Agent**: Uses Google Gemini for rubric-based semantic scoring.
- **Fact-Checking Agent**: Uses Perplexity for real-time fact-checking.
- **Feedback Agent**: Provides personalized feedback for each student.

## API Endpoints

- `POST /exams/`: Create an exam (answer key, rubric, template)
- `POST /submissions/`: Upload an answer sheet
- `GET /submissions/{id}/aligned`: Get the aligned, registered sheet image
- `GET /submissions/{id}/transforms`: Get the transformation parameters and accuracy
- `GET /submissions/{id}/grades`: Get the grading results (per question)
- `PUT /grades/{grade_id}/override`: Teacher override of a score/feedback
- `GET /analytics/{exam_id}`: Get aggregated analytics
- `POST /devdock/verify`: Verify a credential on the DevDock blockchain
- `GET /health`: Health check

## Setup Guide

### Prerequisites

- Python 3.9+
- Docker
- Node.js (for Next.js frontend)
- A Firebase account
- A Google Gemini API key
- A Perplexity API key
- A DevDock API key

### 1. Clone the repository

```bash
git clone <repository-url>
cd edugrade-ai
```

### 2. Set up Firebase

1. Go to [Firebase](https://firebase.google.com/) and create a new project.
2. In your Firebase project, go to `Project settings` > `Service accounts`.
3. Click on `Generate new private key` and download the JSON file.
4. Save the JSON file as `firebase-credentials.json` in the `backend/app/core` directory.

### 3. Configure environment variables

Create a `.env` file in the root of the project and add the following environment variables:

```
GEMINI_API_KEY=<your-google-gemini-api-key>
PERPLEXITY_API_KEY=<your-perplexity-api-key>
DEVDOCK_API_KEY=<your-devdock-api-key>
```

### 4. Run the application

You can run the application using Docker Compose:

```bash
docker-compose up --build
```

This will start the backend server, the Streamlit frontend, and the Next.js frontend.

- **Backend API**: `http://localhost:8000`
- **Streamlit Dashboard**: `http://localhost:8501`
- **Next.js App**: `http://localhost:3000`

## Testing

To run the tests, you can use `pytest`:

```bash
pytest backend/tests
```
