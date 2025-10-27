# EduGrade AI

EduGrade AI is a multi-agentic answer sheet grading system that automates the process of grading handwritten answer sheets. It uses a combination of computer vision, OCR, and large language models to provide accurate grades and personalized feedback.

## Features

- **Automated Grading**: Automatically grades handwritten answer sheets.
- **Personalized Feedback**: Provides personalized feedback for each student.
- **Teacher Dashboard**: A dashboard for teachers to review and override grades.
- **Supabase Integration**: Uses Supabase for the database.
- **Streamlit Frontend**: A Streamlit frontend for rapid prototyping and hackathons.
- **Next.js Frontend (in progress)**: A Next.js frontend for production use.

## Setup Guide

### Prerequisites

- Python 3.9+
- Docker
- Node.js (for Next.js frontend)
- A Supabase account

### 1. Clone the repository

```bash
git clone <repository-url>
cd edugrade-ai
```

### 2. Set up Supabase

1. Go to [Supabase](https://supabase.io/) and create a new project.
2. In your Supabase project, go to `Settings` > `Database`.
3. Find the `Connection string` and copy it.

### 3. Configure environment variables

Create a `.env` file in the root of the project and add the following environment variables:

```
DATABASE_URL=<your-supabase-connection-string>
OPENAI_API_KEY=<your-openai-api-key>
PERPLEXITY_API_KEY=<your-perplexity-api-key>
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

## How to use

1. **Create an exam**: Use the API to create an exam with an answer key.
2. **Upload an answer sheet**: Use the Streamlit dashboard to upload an answer sheet.
3. **View the results**: View the grading results in the Streamlit dashboard.

## Testing

To run the tests, you can use `pytest`:

```bash
pytest backend/tests
```
