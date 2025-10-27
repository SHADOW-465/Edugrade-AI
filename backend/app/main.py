"""
Main application file for the EduGrade AI FastAPI backend.

This file initializes the FastAPI application, sets up CORS middleware,
and includes the API routers for the different endpoints. It also
creates the database tables on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import exams, submissions, grades, analytics
from .core.database import engine, Base
from .config import get_settings

# Get application settings
settings = get_settings()

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="EduGrade AI", version="1.0.0")

# Set up CORS middleware to allow cross-origin requests
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for different parts of the application
app.include_router(exams.router, prefix="/api/v1/exams", tags=["Exams"])
app.include_router(submissions.router, prefix="/api/v1/submissions", tags=["Submissions"])
app.include_router(grades.router, prefix="/api/v1/grades", tags=["Grades"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.on_event("startup")
async def startup_event():
    """
    Event handler for the application startup.
    This is a good place to load models or other resources.
    """
    pass

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for the application shutdown.
    This is a good place to clean up resources.
    """
    pass

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify that the application is running.
    """
    return {"status": "ok"}
