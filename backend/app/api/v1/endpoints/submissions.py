"""
API endpoints for managing submissions.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from .... import models
from ....core.database import SessionLocal
from ....services import grading_service
from ....config import get_settings
import shutil
import os

router = APIRouter()
settings = get_settings()

def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=models.schemas.SubmissionResponse)
async def create_submission(
    exam_id: int,
    student_name: str,
    student_id: str,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    Create a new submission.
    """
    # Save the uploaded file
    file_path = os.path.join(settings.UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create a submission record in the database
    submission = models.database.Submission(
        exam_id=exam_id,
        student_name=student_name,
        student_id=student_id,
        image_path=file_path,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # Start the grading workflow in the background
    background_tasks.add_task(grading_service.grade_submission, submission.id, db)

    # This is a placeholder for the response
    return {
        "id": submission.id,
        "exam_id": submission.exam_id,
        "student_name": submission.student_name,
        "student_id": submission.student_id,
        "status": submission.status,
        "progress": 0,
        "grades": [],
        "uploaded_at": submission.uploaded_at,
        "processed_at": submission.processed_at
    }

@router.get("/{submission_id}", response_model=models.schemas.SubmissionResponse)
def read_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single submission by ID.
    """
    db_submission = db.query(models.database.Submission).filter(models.database.Submission.id == submission_id).first()
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    # This is a placeholder for the response
    return {
        "id": db_submission.id,
        "exam_id": db_submission.exam_id,
        "student_name": db_submission.student_name,
        "student_id": db_submission.student_id,
        "status": db_submission.status,
        "progress": 0,
        "grades": [],
        "uploaded_at": db_submission.uploaded_at,
        "processed_at": db_submission.processed_at
    }

@router.get("/{submission_id}/status")
def get_submission_status(submission_id: int, db: Session = Depends(get_db)):
    """
    Get the status of a submission.
    """
    db_submission = db.query(models.database.Submission).filter(models.database.Submission.id == submission_id).first()
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"status": db_submission.status, "progress_percentage": 0, "current_step": ""}
