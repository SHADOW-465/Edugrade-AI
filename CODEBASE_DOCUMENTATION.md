# EduGrade AI: Codebase Documentation

## 1. Project Overview

EduGrade AI is a multi-agentic, AI-powered system designed to automate the grading of handwritten answer sheets. It streamlines the grading process by leveraging computer vision for image processing and large language models for intelligent evaluation. The system is built to be modular, scalable, and adaptable for different deployment scenarios, from hackathon prototypes to production-grade applications.

## 2. Architecture

The application is built on a microservices-oriented architecture with a distinct separation between the backend and frontend.

-   **Backend**: A powerful FastAPI application that exposes a RESTful API for all grading-related operations. It uses a multi-agent system orchestrated by LangGraph to handle the complex grading workflow.
-   **Frontend**: The system is designed to be compatible with multiple frontend clients. The primary frontend is a Streamlit dashboard for rapid prototyping and internal use, with the flexibility to integrate with a more robust, production-ready frontend built with a framework like React or Next.js.
-   **Database**: Supabase (PostgreSQL) is used for data persistence, managed through the SQLAlchemy ORM.
-   **Agents**: A collection of specialized agents, each responsible for a specific task in the grading pipeline.

## 3. Backend

The backend is a FastAPI application that serves as the core of the EduGrade AI system.

### 3.1. Project Structure

The backend code is organized into a modular structure to promote separation of concerns and maintainability.

-   `app/`: The main application package.
    -   `main.py`: The FastAPI application entry point, where the app is initialized and middleware is configured.
    -   `api/`: Contains the API endpoints, versioned for better maintenance.
    -   `agents/`: Houses the individual agents responsible for specific tasks in the grading workflow.
    -   `core/`: Core components like database connections, security, and configuration.
    -   `graph/`: The LangGraph workflow definition, orchestrating the agents.
    -   `models/`: SQLAlchemy database models and Pydantic schemas.
    -   `services/`: Business logic and service layer.
    -   `utils/`: Utility functions and helper scripts.
-   `tests/`: Unit and integration tests for the backend.

### 3.2. API Endpoints

The API is versioned under `/api/v1` and provides the following resources:

-   `/exams`: Manage exams, including creating, retrieving, and updating exam details and answer keys.
-   `/submissions`: Handle the submission of answer sheets, initiate the grading process, and retrieve grading status and results.
-   `/grades`: Manage individual grades, including teacher overrides and integrity verification.
-   `/analytics`: Provide analytics and insights into student and class performance.

### 3.3. Agents

The grading process is handled by a series of agents, each with a specific responsibility:

-   `PreprocessingAgent`: Cleans and prepares the uploaded answer sheet images for processing.
-   `SegmentationAgent`: Segments the answer sheet to identify individual answer boxes.
-   `OCRAgent`: Extracts handwritten text from the segmented answer boxes.
-   `GradingAgent`: Grades the extracted text using an LLM (Gemini) based on the provided rubric.
-   `FeedbackAgent`: Generates personalized feedback for students based on their performance.
-   `StorageAgent`: Stores the grading results in the database with a cryptographic hash for integrity.

## 4. Frontend

The frontend is designed to be decoupled from the backend, communicating via the REST API.

-   **Streamlit**: A Streamlit dashboard provides a user-friendly interface for uploading answer sheets, viewing grading results, and analyzing performance.
-   **React/Next.js**: The API is designed to support a more complex, production-ready frontend built with a modern JavaScript framework.

## 5. Getting Started

To run the application, you will need to have Docker and Docker Compose installed.

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd edugrade-ai
    ```
2.  **Configure environment variables**:
    Create a `.env` file from the `env.example` file and populate it with your Supabase credentials and Gemini API key.
3.  **Run the application**:
    ```bash
    docker-compose up -d
    ```
4.  **Access the application**:
    -   The backend API will be available at `http://localhost:8000`.
    -   The Streamlit dashboard will be accessible at `http://localhost:8501`.
