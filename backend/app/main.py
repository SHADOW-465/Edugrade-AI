"""
Main application file for the EduGrade AI FastAPI backend.

This initializes the FastAPI app, sets up CORS middleware,
and includes the API routers for exams, submissions, grades, and analytics.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import exams, submissions, approvals, analytics
from app.config import get_settings

# Get application settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(title="EduGrade AI", version="2.0.0")

# CORS setup
origins = settings.CORS_ORIGINS.split(",") if hasattr(settings, "CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(exams.router, prefix="/api/v1/exams", tags=["Exams"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["Submissions"])
app.include_router(approvals.router, prefix="/api/v1/approvals", tags=["Approvals"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    """
    print("✅ EduGrade AI backend started successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application stops.
    """
    print("🛑 EduGrade AI backend shutting down...")


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "EduGrade AI backend running successfully"}
