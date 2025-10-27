"""
Main application file for the EduGrade AI FastAPI backend (Firebase version).

This initializes the FastAPI app, sets up CORS middleware,
and includes the API routers for exams, submissions, grades, and analytics.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import exams, submissions
from app.core.firebase_db import db  # ✅ Firestore connection
from app.config import get_settings

# Get application settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(title="EduGrade AI", version="2.0.0")

# ✅ CORS setup
origins = settings.CORS_ORIGINS.split(",") if hasattr(settings, "CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include only Firebase-based routers (for now)
app.include_router(exams.router, prefix="/api/v1/exams", tags=["Exams"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["Submissions"])

# Optional future routes (uncomment once you add them)
# from app.api.v1.endpoints import grades, analytics
# app.include_router(grades.router, prefix="/api/v1/grades", tags=["Grades"])
# app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts.
    This initializes Firebase and checks connection.
    """
    print("✅ EduGrade AI backend started successfully.")
    print("🔥 Firebase connection active:", db)

@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application stops.
    Useful for cleanup tasks.
    """
    print("🛑 EduGrade AI backend shutting down...")

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "EduGrade AI Firebase backend running successfully"}
