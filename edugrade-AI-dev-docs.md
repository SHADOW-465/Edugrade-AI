<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# i just want you to give me a descriptive detailed development guide which i can use to input as a prompt into cursor to build out the entire application. i want to build it such that it is compatible with streamlit implementation as well as a react or next.js frontend and this code acting as a backend, so that i can implement it as production grade as well as for quick UI for the hackathon.

Here's a **comprehensive, detailed development prompt** you can directly input into Cursor to build your entire EduGrade AI application with both Streamlit (for hackathon) and REST API backend (for React/Next.js production frontend):

***

# **Cursor Development Prompt: EduGrade AI - Multi-Agentic Answer Sheet Grading System**


Project Overview

Build a production-grade, modular automated answer sheet grading system called "EduGrade AI" that:
Accepts scanned/uploaded handwritten answer sheets
Automatically preprocesses, segments, and extracts text via OCR
Grades answers using AI with personalized feedback
Provides a teacher dashboard for review and override
Supports both Streamlit UI (for rapid hackathon demo) and RESTful API backend (for React/Next.js production frontend)

Architecture Requirements


Backend: FastAPI + LangGraph Multi-Agent System

Framework: FastAPI with async support for long-running tasks.
Multi-Agent Orchestration: LangGraph for modular agent pipeline.
Agents:
Preprocessing Agent (OpenCV)
Segmentation Agent (YOLOv8)
OCR Agent (DeepSeek-OCR + TrOCR ensemble)
Grading Agent (Gemini with rubric-based evaluation)
Feedback Agent (Personalized student feedback)
Fact-Check Agent (Perplexity API) (Imported from mark_ai_st)
Database: Convex (as the primary real-time DB) and SQLite (as a persistent failsafe queue).
Resiliency: A FailsafeService will wrap all database operations. A background apscheduler will sync the queue to Convex when the DB is online.
API Documentation: Auto-generated via FastAPI/Swagger

Frontend Options

Streamlit Dashboard: A complete, multi-role (Teacher, Parent, Admin) UI for all app functions.
REST API Endpoints: For React/Next.js production frontend.

Detailed Technical Specifications


1. Project Structure

Create the following modular, production-grade file structure:



edugrade-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI app, lifespan manager, scheduler
│   │   ├── config.py                    # Configuration management
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py              # JWT auth, password hashing
│   │   │   ├── logging.py               # Logging configuration
│   │   │   └── exceptions.py            # Custom exception handlers
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py            # Abstract base agent class
│   │   │   ├── preprocessing_agent.py   # OpenCV preprocessing
│   │   │   ├── segmentation_agent.py    # YOLOv8 document segmentation
│   │   │   ├── ocr_agent.py             # DeepSeek-OCR + TrOCR ensemble
│   │   │   ├── grading_agent.py         # LLM-based grading
│   │   │   ├── feedback_agent.py        # Personalized feedback generation
│   │   │   └── factcheck_agent.py       # Perplexity fact-checking
│   │   │
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── workflow.py              # LangGraph workflow orchestration
│   │   │   └── state.py                 # Shared state definitions
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── exams.py         # Exam management endpoints
│   │   │   │   │   ├── submissions.py   # Answer sheet upload/grading
│   │   │   │   │   ├── approvals.py     # Teacher approval workflow
│   │   │   │   │   ├── analytics.py     # Dashboard analytics
│   │   │   │   │   └── health.py        # Health check endpoints
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py               # Pydantic request/response schemas
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── grading_service.py       # Invokes LangGraph, handles results
│   │   │   ├── convex_service.py        # Python client for Convex
│   │   │   ├── local_queue_service.py   # SQLite queue for failsafe
│   │   │   └── failsafe_service.py      # Wraps Convex/SQLite logic
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── image_utils.py           # Image processing helpers
│   │       └── prompt_templates.py      # LLM prompt templates
│   │
│   ├── convex/                          # Convex project
│   │   ├── schema.ts                    # Convex database schema
│   │   ├── submissions.ts               # Convex mutations/queries
│   │   └── exams.ts                     # Convex mutations/queries
│   │
│   ├── tests/
│   │   ├── (tests to be updated for new services)
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── streamlit_dashboard.py         # Main multi-role UI
│   ├── requirements.txt               # Frontend deps
│   └── (nextjs folder removed for clarity)
│
├── data/
│   ├── uploads/
│   ├── processed/
│   └── models/
│
├── docker-compose.yml
├── Dockerfile
├── failsafe_queue.db                  # Local SQLite failsafe DB
└── README.md



2. Core Implementation Requirements


A. Configuration Management (backend/app/config.py)


Python


"""
Create a Pydantic Settings class for environment-based configuration.
- Load from .env file
- Support for API keys (GEMINI, PERPLEXITY)
- CONVEX_URL (from Convex dashboard)
- File storage paths
"""



B. Convex Setup

Initialize Convex: Run npx convex init in the backend/ directory.
Define Schema: Create backend/convex/schema.ts to define exams and submissions tables. The submissions table must include fields for status, results, and approval info.
Define Functions: Create backend/convex/submissions.ts and backend/convex/exams.ts to hold all backend database logic (mutations and queries) like createSubmission, getSubmission, storeGradingResults, approveSubmission, getPendingApprovals, etc.

C. Database Models (backend/convex/schema.ts)


TypeScript


/*
Implement the Convex schema:

1. exams Table:
   - title, subject, grade_level, teacher_id
   - answer_key (v.any() for JSON)
   - status (v.string())
   - Index: by_teacher_id

2. submissions Table:
   - id (v.string(), our unique ID)
   - exam_id, student_id, student_name, teacher_id
   - file_paths (v.array(v.string()))
   - status (v.string(): e.g., "processing", "pending_review", "approved")
   - processing_stage (v.optional(v.string()))
   - created_at (v.number())
   - results (v.optional(v.any()))
   - total_score, max_score, percentage (v.optional(v.number()))
   - approved, approved_by, approved_at (v.optional(...))
   - Indexes: by_submission_id, by_teacher_id, by_student_id
*/



D. Pydantic Schemas (backend/app/models/schemas.py)


Python


"""
Create Pydantic models for API request/response validation:

Request Schemas:
- ExamCreate: (from mark_ai_st)
- ApprovalRequest: (from mark_ai_st)

Response Schemas:
- ExamResponse: (from mark_ai_st)
- SubmissionResponse: (from mark_ai_st)
- ApprovalResponse: (from mark_ai_st)
- SubmissionReview: (from mark_ai_st)
"""



3. Agent Implementation


A. Base Agent Class (backend/app/agents/base_agent.py)


Python


"""
Create an abstract base class for all agents with:
- process() method (abstract)
- Logging integration
- Must be compatible with LangGraph state
"""



B-F. All Agents (backend/app/agents/*.py)


Python


"""
Refactor all agents (Preprocessing, Segmentation, OCR, Grading, FactCheck, Feedback) to:
1. Inherit from BaseAgent.
2. Implement an `async def process(self, state: GradingState) -> GradingState` method.
3. Read all necessary inputs from the `state` dictionary.
4. Write all outputs back into the `state` dictionary.
5. Return the modified `state` object.
"""



G. Failsafe & Storage Service (Replaces StorageAgent)

The StorageAgent is removed. Its logic is now split:
1. backend/app/services/convex_service.py:
Uses convex-client-python.
Implements the same interface as the old FirebaseService (e.g., async def create_submission, async def get_submission, async def store_grading_results).
Wraps all self.client.call() in a try...except block that raises a custom DatabaseError.
Uses asyncio.to_thread or loop.run_in_executor to run the synchronous Convex calls in an async-compatible way.
2. backend/app/services/local_queue_service.py:
Manages a local failsafe_queue.db file using sqlite3.
Provides methods: add_to_queue, get_pending_actions, delete_action, increment_attempt.
This queue is persistent across server restarts.
3. backend/app/services/failsafe_service.py:
Wraps both ConvexService and LocalQueueService.
Maintains a self.db_healthy boolean.
Write Logic: Tries to call convex_service. If it raises DatabaseError, it sets db_healthy = False and writes the action to the local_queue_service instead.
Read Logic: Tries to call convex_service. If it fails, it can optionally try to read from the local_queue_service for recently-created items.
Sync Logic: Implements sync_queue_to_db() for the scheduler to call.

4. LangGraph Workflow (backend/app/graph/workflow.py)


Python


"""
Create LangGraph orchestration for the grading pipeline:

State Definition (backend/app/graph/state.py):
class GradingState(TypedDict):
    submission_id: str
    exam_id: str
    file_paths: List[str]
    answer_key: Dict[str, Any]
    status: str
    # Agent outputs
    preprocessed_images: Optional[List[Dict]]
    segmented_regions: Optional[List[Dict]]
    grades: Optional[List[Dict]]
    grades_fact_checked: Optional[List[Dict]]
    feedback: Optional[str]
    error: Optional[str]

Nodes:
1. preprocess_node
2. segment_node
3. grade_node
4. fact_check_node
5. feedback_node
6. (NO storage_node - saving is handled by the calling service)

Graph Construction:
- Entry point: preprocess_node
- Linear flow: preprocess → segment → grade → fact_check → feedback → END
- Error edges: (To be implemented)
"""



5. FastAPI Endpoints


A. Main Application (backend/app/main.py)


Python


"""
Create FastAPI application with:
- `lifespan` manager:
    - On startup: Initializes the `FailsafeService`, `LocalQueueService`, and starts the `apscheduler`.
    - The `apscheduler` must call `failsafe_service.check_db_health` (e.g., every 60s) and `failsafe_service.sync_queue_to_db` (e.g., every 120s).
    - On shutdown: Shuts down the scheduler.
- `DatabaseError` Exception Handler:
    - Catches any `DatabaseError` raised from the services.
    - Returns a `HTTP 503 Service Unavailable` with a JSON payload:
      `{"detail": "Database is temporarily unavailable. Your request has been queued."}`
- API Routers:
    - Include routers for exams, submissions, and approvals.
"""



B. API Endpoints (backend/app/api/v1/endpoints/*.py)


Python


"""
Refactor ALL API endpoint files (exams.py, submissions.py, approvals.py):
1.  **Dependency Injection:** Create a `get_failsafe_service() -> FailsafeService` dependency that returns the global `app.state.failsafe_service` instance from `main.py`.
2.  **Change Function Signatures:** All API functions that need the database must now depend on `failsafe: FailsafeService = Depends(get_failsafe_service)`.
3.  **Call Failsafe:** All calls to `firebase.create_...` are replaced with `await failsafe.create_...`.
"""



C. Submission Endpoints (backend/app/api/v1/endpoints/submissions.py)


Python


"""
This is the most critical API change.

POST /api/v1/submissions/
- Must accept `background_tasks: BackgroundTasks` as a parameter.
- **DO NOT** run the grading pipeline here.
- Logic:
    1. Save the uploaded files.
    2. Create the `submission_data` dictionary.
    3. Call `await failsafe.create_submission(submission_data)`.
    4. **Add the background task:** `background_tasks.add_task(grading_service.grade_submission, submission_id)`.
    5. Return the `SubmissionResponse` immediately.
"""



6. Streamlit Dashboard (frontend/streamlit_dashboard.py)


Python


"""
(This file is largely complete from mark_ai_st).

Key Change:
- Modify the `EduGradeAPI._make_request` function.
- In the `except requests.exceptions.RequestException as e:` block:
    - Check if `e.response is not None and e.response.status_code == 503`.
    - If True, display a friendly `st.warning("🚨 Database is temporarily unavailable. Your request has been queued and will be processed shortly.", icon="🕒")`.
    - Otherwise, show the normal `st.error(f"API Error: {str(e)}")`.
"""



7. Services Layer


A. Grading Service (backend/app/services/grading_service.py)


Python


"""
This service is the "glue" that runs the background task.

Functions:
1.  async def grade_submission(submission_id: str):
    - This is the function called by `BackgroundTasks`.
    - Instantiate the `FailsafeService`.
    - Fetch submission data and answer key using `failsafe.get_submission` and `failsafe.get_answer_key`.
    - Initialize the `GradingState` dictionary.
    - Invoke the LangGraph workflow: `final_state = await workflow.ainvoke(initial_state)`.
    - Call `await save_results_to_db(failsafe, submission_id, final_state)`.
    - Implement `try...except` to catch all errors and update submission status to "error" using `failsafe.update_submission_status`.

2.  async def save_results_to_db(failsafe: FailsafeService, ...):
    - This helper function should be wrapped with `@retry(retry=retry_if_exception_type(DatabaseError), ...)` from the `tenacity` library.
    - It calls `failsafe.store_grading_results(...)` and `failsafe.update_submission_status(...)`.
    - This ensures that even if the DB connection flaps, the app will retry saving the *final* results.
"""



8. Requirements Files

backend/requirements.txt:

Plaintext


# Core Framework
fastapi
uvicorn[standard]
python-multipart
pydantic
pydantic-settings

# Multi-Agent & LLM
langgraph
langchain
langchain-openai
openai
google-generativeai

# Computer Vision & OCR
opencv-python
ultralytics
transformers
torch
torchvision
Pillow
pdf2image

# Database & Failsafe
convex-client-python
apscheduler
tenacity
sqlite3

# Utilities
python-dotenv
numpy
pandas
requests


frontend/requirements.txt:

Plaintext


streamlit
requests
pandas
plotly
pillow



Success Criteria

[ ] Backend runs, and failsafe_queue.db file is created.
[ ] /health endpoint shows "database_status: Healthy".
[ ] Submitting a file returns an immediate response while the AI agents run in the background.
[ ] (Test) Shutting down the cloud DB (or disconnecting internet) causes the /health endpoint to show "UNHEALTHY (Failsafe Mode Active)".
[ ] (Test) Submitting a file while the DB is "UNHEALTHY" still returns an immediate response, and a new entry appears in the pending_actions table in failsafe_queue.db.
[ ] (Test) Restoring the DB connection causes the apscheduler to automatically sync the queued items, and the pending_actions table becomes empty.
[ ] The Streamlit app shows the correct "queued" or "unavailable" message instead of crashing.
