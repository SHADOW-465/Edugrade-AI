<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# i just want you to give me a descriptive detailed development guide which i can use to input as a prompt into cursor to build out the entire application. i want to build it such that it is compatible with streamlit implementation as well as a react or next.js frontend and this code acting as a backend, so that i can implement it as production grade as well as for quick UI for the hackathon.

Here's a **comprehensive, detailed development prompt** you can directly input into Cursor to build your entire EduGrade AI application with both Streamlit (for hackathon) and REST API backend (for React/Next.js production frontend):

***

# **Cursor Development Prompt: EduGrade AI - Multi-Agentic Answer Sheet Grading System**

## **Project Overview**

Build a production-grade, modular automated answer sheet grading system called "EduGrade AI" that:

- Accepts scanned/uploaded handwritten answer sheets
- Automatically preprocesses, segments, and extracts text via OCR
- Grades answers using AI with personalized feedback
- Provides a teacher dashboard for review and override
- Supports both Streamlit UI (for rapid hackathon demo) and RESTful API backend (for React/Next.js production frontend)

***

## **Architecture Requirements**

### **Backend: FastAPI + LangGraph Multi-Agent System**

- **Framework**: FastAPI with async support
- **Multi-Agent Orchestration**: LangGraph for modular agent pipeline
- **Agents**:

1. Preprocessing Agent (OpenCV)
2. Segmentation Agent (YOLOv8)
3. OCR Agent (DeepSeek-OCR + TrOCR ensemble)
4. Grading Agent (GPT-4o/Gemini with rubric-based evaluation)
5. Feedback Agent (Personalized student feedback)
6. Storage Agent (PostgreSQL + cryptographic hashing)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based (optional for production)
- **API Documentation**: Auto-generated via FastAPI/Swagger


### **Frontend Options**

1. **Streamlit Dashboard**: Quick UI for hackathon demos
2. **REST API Endpoints**: For React/Next.js production frontend

***

## **Detailed Technical Specifications**

### **1. Project Structure**

Create the following modular, production-grade file structure:

```
edugrade-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI application entry
│   │   ├── config.py                    # Configuration management
│   │   ├── dependencies.py              # Shared dependencies
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py              # JWT auth, password hashing
│   │   │   ├── database.py              # Database connection
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
│   │   │   └── storage_agent.py         # Database + hash storage
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
│   │   │   │   │   ├── grades.py        # Grade retrieval/override
│   │   │   │   │   ├── analytics.py     # Dashboard analytics
│   │   │   │   │   └── health.py        # Health check endpoints
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── database.py              # SQLAlchemy models
│   │   │   └── schemas.py               # Pydantic request/response schemas
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── exam_service.py          # Exam business logic
│   │   │   ├── grading_service.py       # Grading orchestration
│   │   │   ├── ocr_service.py           # OCR wrapper service
│   │   │   ├── llm_service.py           # LLM API integration
│   │   │   └── storage_service.py       # File/DB operations
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── image_utils.py           # Image processing helpers
│   │       ├── prompt_templates.py      # LLM prompt templates
│   │       ├── validators.py            # Input validation
│   │       └── hash_utils.py            # Cryptographic hashing
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                  # Pytest fixtures
│   │   ├── test_agents.py
│   │   ├── test_api.py
│   │   ├── test_services.py
│   │   └── test_graph.py
│   │
│   ├── alembic/                         # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── streamlit/
│   │   ├── app.py                       # Streamlit dashboard
│   │   ├── pages/
│   │   │   ├── upload.py                # Sheet upload page
│   │   │   ├── grading.py               # Grading results page
│   │   │   ├── analytics.py             # Analytics dashboard
│   │   │   └── settings.py              # Configuration page
│   │   └── components/
│   │       ├── grade_card.py            # Reusable grade display
│   │       └── feedback_panel.py        # Feedback display component
│   │
│   └── nextjs/                          # (Future: React/Next.js frontend)
│       └── README.md
│
├── data/
│   ├── uploads/                         # Temporary upload storage
│   ├── processed/                       # Processed images
│   ├── models/                          # YOLO weights
│   │   └── yolov8n.pt
│   └── sample_data/
│       ├── answer_sheets/
│       └── answer_keys/
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```


***

## **2. Core Implementation Requirements**

### **A. Configuration Management (`backend/app/config.py`)**

```python
"""
Create a Pydantic Settings class for environment-based configuration.
- Load from .env file
- Support for API keys (OpenAI, Perplexity, etc.)
- Database connection string
- File storage paths
- Model configurations
- CORS settings
"""
```

**Requirements**:

- Use `pydantic-settings` for validation
- Support development and production environments
- Implement `@lru_cache` for singleton pattern
- Include validation for required fields


### **B. Database Models (`backend/app/models/database.py`)**

```python
"""
Create SQLAlchemy ORM models for:

1. Exam Table:
   - id, name, subject, total_questions
   - answer_key (JSON field storing model answers and rubrics)
   - created_at, updated_at
   - Relationship: one-to-many with Submission

2. Submission Table:
   - id, exam_id (FK), student_name, student_id
   - image_path, status (enum: pending, processing, completed, failed)
   - uploaded_at, processed_at
   - Relationship: one-to-many with Grade

3. Grade Table:
   - id, submission_id (FK), question_number
   - extracted_text (OCR output)
   - score, max_score
   - feedback (personalized feedback text)
   - reasoning (LLM grading explanation)
   - points_covered (JSON array)
   - points_missed (JSON array)
   - hash_signature (SHA-256 hash for tamper-proof)
   - teacher_override (boolean), override_reason
   - created_at, updated_at

4. User Table (Optional):
   - id, email, hashed_password, role (teacher/admin)
   - created_at
"""
```

**Requirements**:

- Use declarative base from SQLAlchemy
- Add proper indexes for performance
- Include timestamps with automatic updates
- Implement cascade deletes appropriately


### **C. Pydantic Schemas (`backend/app/models/schemas.py`)**

```python
"""
Create Pydantic models for API request/response validation:

Request Schemas:
- ExamCreate: name, subject, answer_key (list of questions with rubrics)
- SubmissionCreate: exam_id, student_name, file upload
- GradeOverride: grade_id, new_score, reason

Response Schemas:
- ExamResponse: Include all fields + submission count
- SubmissionResponse: Include status, progress, grades list
- GradeResponse: score, feedback, reasoning, hash_signature
- AnalyticsResponse: class average, distribution, common errors

Nested Schemas:
- QuestionRubric: question_number, model_answer, rubric_text, max_marks
- GradeDetail: question_number, score, feedback, breakdown
"""
```


***

## **3. Agent Implementation**

### **A. Base Agent Class (`backend/app/agents/base_agent.py`)**

```python
"""
Create an abstract base class for all agents with:
- process() method (abstract)
- Logging integration
- Error handling wrapper
- Performance metrics collection
"""
```


### **B. Preprocessing Agent (`backend/app/agents/preprocessing_agent.py`)**

```python
"""
Implement OpenCV-based image preprocessing:

Functions:
1. deskew_image(image: np.ndarray) -> np.ndarray
   - Detect angle using minAreaRect
   - Apply rotation transformation

2. denoise_image(image: np.ndarray) -> np.ndarray
   - Apply fastNlMeansDenoising

3. binarize_image(image: np.ndarray) -> np.ndarray
   - Convert to grayscale
   - Apply adaptive thresholding

4. process(image_path: str) -> np.ndarray
   - Full preprocessing pipeline
   - Return cleaned, aligned image

Error Handling:
- Handle corrupted images
- Validate image dimensions
- Log preprocessing steps
"""
```


### **C. Segmentation Agent (`backend/app/agents/segmentation_agent.py`)**

```python
"""
Implement YOLOv8-based document segmentation:

Functions:
1. __init__(model_path: str)
   - Load YOLOv8 model
   - Set confidence threshold

2. detect_answer_boxes(image: np.ndarray) -> List[BoundingBox]
   - Run YOLO inference
   - Filter by confidence
   - Sort boxes by position (top-to-bottom, left-to-right)

3. crop_answers(image: np.ndarray, boxes: List[BoundingBox]) -> List[np.ndarray]
   - Extract answer regions
   - Apply padding if needed

4. process(image: np.ndarray) -> List[Dict]
   - Return list of cropped answer images with metadata
   - Include question_number, bbox coordinates

Features:
- Support for custom-trained YOLO models
- Fallback to grid-based segmentation if detection fails
- Visual debugging option (draw boxes on image)
"""
```


### **D. OCR Agent (`backend/app/agents/ocr_agent.py`)**

```python
"""
Implement ensemble OCR using DeepSeek-OCR and TrOCR:

Functions:
1. __init__()
   - Initialize TrOCR processor and model
   - Initialize DeepSeek-OCR client (if using API)

2. extract_trocr(image: np.ndarray) -> Tuple[str, float]
   - Process with TrOCR
   - Return (text, confidence_score)

3. extract_deepseek(image: np.ndarray) -> Tuple[str, float]
   - Process with DeepSeek-OCR
   - Return (text, confidence_score)

4. ensemble_extract(image: np.ndarray) -> Dict
   - Run both OCR models
   - Select best result based on:
     * Confidence scores
     * Text length
     * Character validity
   - Return: {text, confidence, source_model, alternatives}

5. process(answer_images: List[np.ndarray]) -> List[Dict]
   - Batch process all answers
   - Return structured OCR results

Optimization:
- Batch processing for efficiency
- GPU utilization if available
- Caching for repeated images
"""
```


### **E. Grading Agent (`backend/app/agents/grading_agent.py`)**

```python
"""
Implement LLM-based grading:

Functions:
1. __init__(api_key: str, model: str)
   - Initialize OpenAI/Anthropic client
   - Load prompt templates

2. grade_answer(
       student_answer: str,
       model_answer: str,
       rubric: str,
       max_marks: int
   ) -> Dict
   
   Prompt Structure:
   - Role: Expert exam evaluator
   - Context: Model answer, rubric, max marks
   - Task: Evaluate with partial marking
   - Output: JSON with:
     * score (float)
     * points_covered (list)
     * points_missed (list)
     * feedback (string)
     * reasoning (step-by-step explanation)
   
   Temperature: 0.3 (for consistency)
   Response Format: Strict JSON

3. batch_grade(answers: List[Dict]) -> List[Dict]
   - Process multiple answers
   - Handle API rate limits
   - Retry logic for failures

4. fact_check(answer: str, topic: str) -> Dict
   - Optional Perplexity Sonar API integration
   - Return factual accuracy assessment

Error Handling:
- API timeout handling
- Fallback to alternative models
- Validate JSON responses
"""
```


### **F. Feedback Agent (`backend/app/agents/feedback_agent.py`)**

```python
"""
Generate personalized student feedback:

Functions:
1. generate_feedback(
       student_name: str,
       grade_results: List[Dict],
       overall_score: float,
       max_score: float
   ) -> str
   
   Prompt Template:
   - Encouraging tone
   - Specific topic recommendations
   - Actionable study advice
   - Highlight strengths and weaknesses
   
2. generate_class_insights(all_grades: List[Dict]) -> Dict
   - Common errors analysis
   - Topic-wise performance
   - Difficulty assessment
   
3. process(grading_results: Dict) -> Dict
   - Add personalized feedback to each grade
   - Generate summary insights
"""
```


### **G. Storage Agent (`backend/app/agents/storage_agent.py`)**

```python
"""
Handle database storage and cryptographic hashing:

Functions:
1. compute_hash(grade_data: Dict) -> str
   - Create SHA-256 hash of grade data
   - Include: submission_id, question, score, timestamp
   - Return hex digest

2. store_grades(grades: List[Dict], submission_id: int) -> bool
   - Insert grades into database
   - Compute and store hash for each grade
   - Handle transaction rollback on error

3. verify_integrity(grade_id: int) -> bool
   - Retrieve grade and stored hash
   - Recompute hash from current data
   - Return True if match (not tampered)

4. process(grading_results: Dict) -> Dict
   - Store all results
   - Return storage confirmation with hashes
"""
```


***

## **4. LangGraph Workflow (`backend/app/graph/workflow.py`)**

```python
"""
Create LangGraph orchestration for the grading pipeline:

State Definition (backend/app/graph/state.py):
class GradingState(TypedDict):
    submission_id: int
    exam_id: int
    image_path: str
    answer_key: List[Dict]
    preprocessed_image: Optional[np.ndarray]
    answer_boxes: Optional[List[Dict]]
    ocr_results: Optional[List[Dict]]
    grades: Optional[List[Dict]]
    feedback: Optional[str]
    status: str
    error: Optional[str]

Nodes:
1. preprocess_node(state: GradingState) -> GradingState
   - Call PreprocessingAgent.process()
   - Update state with preprocessed_image
   - Set status to "preprocessed"

2. segment_node(state: GradingState) -> GradingState
   - Call SegmentationAgent.process()
   - Update state with answer_boxes
   - Set status to "segmented"

3. ocr_node(state: GradingState) -> GradingState
   - Call OCRAgent.process()
   - Update state with ocr_results
   - Set status to "ocr_completed"

4. grade_node(state: GradingState) -> GradingState
   - For each OCR result and corresponding answer key:
     * Call GradingAgent.grade_answer()
   - Update state with grades
   - Set status to "graded"

5. feedback_node(state: GradingState) -> GradingState
   - Call FeedbackAgent.generate_feedback()
   - Update state with personalized feedback
   - Set status to "feedback_generated"

6. storage_node(state: GradingState) -> GradingState
   - Call StorageAgent.store_grades()
   - Update submission status in database
   - Set status to "completed"

7. error_handler_node(state: GradingState) -> GradingState
   - Log error
   - Update submission status to "failed"
   - Send notification (optional)

Graph Construction:
- Entry point: preprocess_node
- Linear flow: preprocess → segment → ocr → grade → feedback → storage
- Error edges: Each node → error_handler_node on exception
- Conditional edges: Skip segmentation if single-answer sheet

Compilation:
- Use StateGraph(GradingState)
- Set checkpointer for workflow resumption
- Enable persistence for long-running tasks
"""
```


***

## **5. FastAPI Endpoints**

### **A. Main Application (`backend/app/main.py`)**

```python
"""
Create FastAPI application with:
- CORS middleware (configurable origins)
- Request ID middleware for tracking
- Exception handlers
- Startup/shutdown events (DB connection, model loading)
- API versioning (prefix: /api/v1)
- Auto-generated OpenAPI docs at /docs

Startup Tasks:
1. Initialize database connection
2. Load YOLO model weights
3. Warm up LLM connections
4. Create upload directories

Shutdown Tasks:
1. Close database connections
2. Cleanup temporary files
"""
```


### **B. Exam Endpoints (`backend/app/api/v1/endpoints/exams.py`)**

```python
"""
Implement exam management endpoints:

POST /api/v1/exams/
- Create new exam with answer key
- Request: ExamCreate schema
- Response: ExamResponse schema

GET /api/v1/exams/
- List all exams (paginated)
- Query params: skip, limit, subject filter

GET /api/v1/exams/{exam_id}
- Get exam details
- Include submission statistics

PUT /api/v1/exams/{exam_id}
- Update exam (answer key, rubrics)

DELETE /api/v1/exams/{exam_id}
- Soft delete exam
"""
```


### **C. Submission Endpoints (`backend/app/api/v1/endpoints/submissions.py`)**

```python
"""
Implement answer sheet submission and grading:

POST /api/v1/submissions/
- Upload answer sheet
- Request: multipart/form-data with file + exam_id + student_name
- Response: submission_id, status
- Trigger: Start async grading workflow

GET /api/v1/submissions/{submission_id}
- Get submission status and results
- Response: SubmissionResponse with grades

GET /api/v1/submissions/{submission_id}/status
- Poll for grading progress
- Response: {status, progress_percentage, current_step}

POST /api/v1/submissions/batch
- Bulk upload multiple answer sheets
- Process in background queue

Implementation:
- Use BackgroundTasks for async processing
- Store files with secure naming (UUID)
- Validate file types and sizes
- Implement retry logic
"""
```


### **D. Grade Endpoints (`backend/app/api/v1/endpoints/grades.py`)**

```python
"""
Grade management and teacher override:

GET /api/v1/grades/{submission_id}
- Get all grades for a submission
- Include feedback and reasoning

PUT /api/v1/grades/{grade_id}/override
- Teacher manual override
- Request: {new_score, reason}
- Update grade and log override

GET /api/v1/grades/{grade_id}/verify
- Verify grade integrity (hash check)
- Response: {verified: bool, hash_match: bool}

DELETE /api/v1/grades/{grade_id}
- Soft delete grade (keep hash for audit)
"""
```


### **E. Analytics Endpoints (`backend/app/api/v1/endpoints/analytics.py`)**

```python
"""
Dashboard analytics and insights:

GET /api/v1/analytics/exam/{exam_id}
- Overall exam statistics
- Response: {
    average_score,
    score_distribution,
    question_wise_performance,
    common_errors
  }

GET /api/v1/analytics/student/{student_id}
- Student performance over time
- Subject-wise breakdown

GET /api/v1/analytics/class
- Class-level insights
- Top performers, struggling students

GET /api/v1/analytics/question/{question_number}
- Question difficulty analysis
- Common mistakes for specific question
"""
```


***

## **6. Streamlit Dashboard (`frontend/streamlit/app.py`)**

```python
"""
Create interactive Streamlit dashboard with:

Pages (using st.Page):
1. Home/Upload Page:
   - Exam selection dropdown
   - File uploader (supports: jpg, png, pdf)
   - Scan via camera option
   - Submit button → triggers API call to /api/v1/submissions/
   - Real-time progress bar polling /status endpoint

2. Grading Results Page:
   - Display submission list (filterable by status, date)
   - Click submission → show detailed grades
   - For each question:
     * Score badge (colored by performance)
     * Extracted answer (expandable)
     * Feedback panel
     * Points covered/missed
     * Teacher override button
   - Download results as PDF/CSV

3. Analytics Dashboard:
   - Summary metrics (cards with st.metric)
   - Score distribution histogram (plotly/altair)
   - Question-wise performance chart
   - Common errors word cloud
   - Filter by exam, date range, student

4. Exam Management:
   - Create new exam form
   - Upload answer key (JSON or manual entry)
   - Rubric editor with markdown support
   - View/edit existing exams

5. Settings:
   - API endpoint configuration
   - Model selection (GPT-4o, Gemini, etc.)
   - Grading strictness slider
   - Export preferences

Features:
- Session state for user authentication
- File caching for performance
- Responsive design
- Error handling with st.error()
- Success notifications with st.success()

API Integration:
- Use requests library
- Handle connection errors gracefully
- Show loading spinners with st.spinner()
"""
```


***

## **7. Services Layer**

### **A. Grading Service (`backend/app/services/grading_service.py`)**

```python
"""
Orchestrate the complete grading workflow:

Functions:
1. async def grade_submission(submission_id: int) -> Dict:
   - Retrieve submission and exam data from DB
   - Initialize workflow with state
   - Execute LangGraph workflow
   - Update database with results
   - Return final grades

2. async def regrade_submission(submission_id: int, questions: List[int]) -> Dict:
   - Re-run grading for specific questions
   - Keep other grades unchanged

3. def get_grading_status(submission_id: int) -> Dict:
   - Check workflow state
   - Return progress information

Implementation:
- Use asyncio for concurrent processing
- Implement queuing for batch processing
- Add logging at each step
- Handle partial failures gracefully
"""
```


***

## **8. Utilities**

### **A. Prompt Templates (`backend/app/utils/prompt_templates.py`)**

```python
"""
Define all LLM prompts as templates:

GRADING_PROMPT = '''
You are an expert {subject} teacher evaluating a student's exam answer.

**Student's Answer:**
{student_answer}

**Model Answer:**
{model_answer}

**Grading Rubric:**
{rubric}

**Maximum Marks:** {max_marks}

**Instructions:**
1. Compare the student's answer against the model answer and rubric
2. Award full marks for complete answers, partial marks for partial correctness
3. Identify all key points covered and missed
4. Provide constructive, specific feedback

**Output Format (strict JSON):**
{{
  "score": <number between 0 and {max_marks}>,
  "points_covered": ["point 1", "point 2", ...],
  "points_missed": ["missing point 1", ...],
  "feedback": "Detailed constructive feedback",
  "reasoning": "Step-by-step grading explanation"
}}
'''

FEEDBACK_PROMPT = '''
Generate encouraging, personalized feedback for {student_name}.

**Performance Summary:**
- Overall Score: {total_score}/{max_total_score}
- Questions: {num_questions}

**Detailed Results:**
{question_breakdown}

**Instructions:**
Write 3-4 sentences that:
1. Acknowledge strengths
2. Identify specific areas for improvement
3. Suggest actionable study strategies
4. Motivate the student

Be specific about topics and concepts, not generic.
'''

FACT_CHECK_PROMPT = '''
Verify the factual accuracy of this answer in the context of {topic}:

{answer}

Return JSON: {{"accurate": bool, "errors": ["error 1", ...], "corrections": ["correction 1", ...]}}
'''
"""
```


### **B. Image Utils (`backend/app/utils/image_utils.py`)**

```python
"""
Helper functions for image operations:

1. validate_image(file_bytes: bytes) -> bool
   - Check file is valid image format
   - Verify dimensions are reasonable

2. resize_if_needed(image: np.ndarray, max_size: int) -> np.ndarray
   - Resize large images for processing efficiency

3. numpy_to_pil(image: np.ndarray) -> Image:
   - Convert between formats

4. add_debug_overlay(image: np.ndarray, boxes: List) -> np.ndarray
   - Draw bounding boxes for visualization

5. pdf_to_images(pdf_path: str) -> List[np.ndarray]:
   - Convert multi-page PDF to images (using pdf2image)
"""
```


***

## **9. Testing Requirements**

### **A. Unit Tests (`backend/tests/test_agents.py`)**

```python
"""
Test each agent independently:

1. test_preprocessing_agent():
   - Test with skewed image → verify straightened
   - Test with noisy image → verify cleaned
   - Test with various formats

2. test_segmentation_agent():
   - Test with standard answer sheet
   - Test with custom layouts
   - Verify box count and order

3. test_ocr_agent():
   - Test with printed text
   - Test with handwritten text (various qualities)
   - Test ensemble logic

4. test_grading_agent():
   - Mock LLM responses
   - Verify rubric application
   - Test partial marking logic

5. test_feedback_agent():
   - Verify personalization
   - Check tone and quality
"""
```


### **B. Integration Tests (`backend/tests/test_api.py`)**

```python
"""
Test API endpoints end-to-end:

1. test_create_exam():
   - POST to /api/v1/exams/
   - Verify response and database entry

2. test_submit_and_grade():
   - Upload answer sheet
   - Poll status until complete
   - Verify grades returned

3. test_teacher_override():
   - Submit override
   - Verify grade updated
   - Check hash recomputed

Use pytest fixtures for:
- Database session
- Test data (sample images, answer keys)
- API client
"""
```


***

## **10. Deployment Configuration**

### **A. Docker Configuration**

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Download models on build
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/edugrade
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=edugrade
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  streamlit:
    build: ./frontend/streamlit
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api

volumes:
  postgres_data:
```


***

## **11. Requirements Files**

**backend/requirements.txt:**

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0

# Multi-Agent & LLM
langgraph==0.2.0
langchain==0.1.0
langchain-openai==0.0.5
openai==1.3.0

# Computer Vision & OCR
opencv-python==4.8.1.78
ultralytics==8.1.0
transformers==4.35.0
torch==2.1.0
torchvision==0.16.0
Pillow==10.1.0
pdf2image==1.16.3

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Utilities
python-dotenv==1.0.0
numpy==1.24.3
pandas==2.1.3
requests==2.31.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Monitoring & Logging
loguru==0.7.2
prometheus-client==0.19.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

**frontend/streamlit/requirements.txt:**

```txt
streamlit==1.28.0
requests==2.31.0
pandas==2.1.3
plotly==5.18.0
altair==5.2.0
Pillow==10.1.0
```


***

## **12. Additional Features to Implement**

1. **Rate Limiting**: Use SlowAPI to prevent abuse
2. **Caching**: Redis for OCR results and LLM responses
3. **Queue System**: Celery for background job processing
4. **Monitoring**: Prometheus metrics + Grafana dashboard
5. **Logging**: Structured logging with request tracing
6. **CI/CD**: GitHub Actions for automated testing and deployment
7. **Security**: Input sanitization, file upload validation, SQL injection prevention
8. **Scalability**: Horizontal scaling with load balancer support

***

## **13. Development Workflow**

1. **Phase 1**: Core backend (FastAPI + Database models)
2. **Phase 2**: Implement all agents independently
3. **Phase 3**: Build LangGraph workflow
4. **Phase 4**: Create API endpoints
5. **Phase 5**: Build Streamlit dashboard
6. **Phase 6**: Testing and debugging
7. **Phase 7**: Docker containerization
8. **Phase 8**: Production deployment

***

## **Success Criteria**

- [ ] Backend API fully functional with all endpoints
- [ ] All agents working independently and in workflow
- [ ] Streamlit dashboard responsive and feature-complete
- [ ] API compatible with future React/Next.js frontend
- [ ] Comprehensive error handling
- [ ] Production-ready with Docker
- [ ] Automated tests passing
- [ ] Documentation complete

***

**Now use this prompt to build the complete EduGrade AI system with modular, production-grade architecture that supports both rapid hackathon demos (Streamlit) and scalable production deployments (REST API + React/Next.js).**

