# EduGrade AI - Multi-Agentic Answer Sheet Evaluator

An automated exam grading system for handwritten answer sheets using multi-agent AI architecture.

## Features

- **Image Preprocessing Agent**: OpenCV + YOLOv8 for answer sheet detection and segmentation
- **OCR Extraction Agent**: Google Vision API + TrOCR for multi-language text extraction
- **Evaluation Agent**: Google Gemini + Perplexity Sonar API for semantic grading
- **Grade Storage Agent**: SHA-256 cryptographic hashing for tamper-proof storage
- **Teacher Dashboard**: Streamlit/Gradio interface for review and override capabilities

## Project Structure

```
Edugrade-AI/
├── agents/                 # Multi-agent system components
│   ├── image_preprocessing.py
│   ├── ocr_extraction.py
│   ├── evaluation.py
│   └── grade_storage.py
├── api/                   # FastAPI backend
│   ├── main.py
│   ├── endpoints/
│   └── models/
├── dashboard/             # Teacher dashboard
│   ├── streamlit_app.py
│   └── gradio_app.py
├── database/              # Database models and migrations
│   ├── models.py
│   └── migrations/
├── utils/                 # Utility functions
│   ├── image_utils.py
│   ├── text_utils.py
│   └── crypto_utils.py
├── tests/                 # Unit tests
├── docker/                # Docker configuration
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Docker (optional)
- Google Cloud Vision API key
- Google Gemini API key
- Perplexity API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Edugrade-AI
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API keys:
# - GOOGLE_GEMINI_API_KEY=your_gemini_api_key
# - GOOGLE_VISION_API_KEY=your_vision_api_key
# - PERPLEXITY_API_KEY=your_perplexity_api_key
```

5. Initialize database:
```bash
python -m database.init_db
```

6. Run the application:
```bash
# Start FastAPI backend
uvicorn api.main:app --reload

# Start teacher dashboard (in another terminal)
streamlit run dashboard/streamlit_app.py
```

### Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## API Endpoints

- `POST /upload` - Upload answer sheet image
- `GET /grades/{student_id}` - Get student grades
- `POST /override` - Teacher grade override
- `GET /analytics` - Class performance analytics

## Configuration

Edit `config/settings.py` to configure:
- API endpoints
- Model parameters
- Database settings
- File storage paths

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=api --cov=dashboard
```

## License

MIT License
