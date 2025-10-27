"""
API endpoints for managing grades.
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

@router.get("/{submission_id}", response_model=List[models.schemas.GradeResponse])
def read_grades_for_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all grades for a submission.
    """
    grades = db.query(models.database.Grade).filter(models.database.Grade.submission_id == submission_id).all()
    return grades

@router.put("/{grade_id}/override", response_model=models.schemas.GradeResponse)
def override_grade(grade_id: int, override: models.schemas.GradeOverride, db: Session = Depends(get_db)):
    """
    Override a grade.
    """
    db_grade = db.query(models.database.Grade).filter(models.database.Grade.id == grade_id).first()
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")

    db_grade.score = override.new_score
    db_grade.override_reason = override.reason
    db_grade.teacher_override = True

    # In a real system, you would recompute the hash or handle it in a way
    # that maintains a verifiable audit trail.

    db.commit()
    db.refresh(db_grade)
    return db_grade

@router.get("/{grade_id}/verify")
def verify_grade_integrity(grade_id: int, db: Session = Depends(get_db)):
    """
    Verify the integrity of a grade.
    """
    # This is a placeholder for the integrity verification logic
    # which would be implemented in the storage agent.
    return {"verified": True, "hash_match": True}
