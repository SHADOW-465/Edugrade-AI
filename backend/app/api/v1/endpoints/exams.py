"""
API endpoints for managing exams.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .... import models
from ....core.database import SessionLocal

router = APIRouter()

def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=models.schemas.ExamResponse)
def create_exam(exam: models.schemas.ExamCreate, db: Session = Depends(get_db)):
    """
    Create a new exam.
    """
    db_exam = models.database.Exam(**exam.dict())
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    # This is a placeholder for submission_count
    db_exam.submission_count = 0
    return db_exam

@router.get("/", response_model=List[models.schemas.ExamResponse])
def read_exams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all exams.
    """
    exams = db.query(models.database.Exam).offset(skip).limit(limit).all()
    # This is a placeholder for submission_count
    for exam in exams:
        exam.submission_count = 0
    return exams

@router.get("/{exam_id}", response_model=models.schemas.ExamResponse)
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single exam by ID.
    """
    db_exam = db.query(models.database.Exam).filter(models.database.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    # This is a placeholder for submission_count
    db_exam.submission_count = 0
    return db_exam

@router.put("/{exam_id}", response_model=models.schemas.ExamResponse)
def update_exam(exam_id: int, exam: models.schemas.ExamCreate, db: Session = Depends(get_db)):
    """
    Update an existing exam.
    """
    db_exam = db.query(models.database.Exam).filter(models.database.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    for var, value in vars(exam).items():
        setattr(db_exam, var, value) if value else None
    db.commit()
    db.refresh(db_exam)
    # This is a placeholder for submission_count
    db_exam.submission_count = 0
    return db_exam

@router.delete("/{exam_id}", response_model=models.schemas.ExamResponse)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    """
    Delete an exam.
    """
    db_exam = db.query(models.database.Exam).filter(models.database.Exam.id == exam_id).first()
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    db.delete(db_exam)
    db.commit()
    # This is a placeholder for submission_count
    db_exam.submission_count = 0
    return db_exam
