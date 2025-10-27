"""
Pydantic schemas for the EduGrade AI application.

This file defines the Pydantic models that are used for API request and
response validation.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .database import StatusEnum


class QuestionRubric(BaseModel):
    """
    Schema for the rubric of a single question.
    """
    question_number: int
    model_answer: str
    rubric_text: str
    max_marks: int


class ExamBase(BaseModel):
    """
    Base schema for an exam.
    """
    name: str
    subject: str
    answer_key: List[QuestionRubric]


class ExamCreate(ExamBase):
    """
    Schema for creating a new exam.
    """
    pass


class ExamResponse(ExamBase):
    """
    Schema for the response when an exam is retrieved.
    """
    id: int
    submission_count: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SubmissionBase(BaseModel):
    """
    Base schema for a submission.
    """
    exam_id: int
    student_name: str
    student_id: str


class SubmissionCreate(SubmissionBase):
    """
    Schema for creating a new submission.
    """
    pass


class GradeDetail(BaseModel):
    """
    Schema for the detailed breakdown of a grade.
    """
    question_number: int
    score: float
    feedback: str
    breakdown: dict


class SubmissionResponse(SubmissionBase):
    """
    Schema for the response when a submission is retrieved.
    """
    id: int
    status: StatusEnum
    progress: int
    grades: List[GradeDetail]
    uploaded_at: datetime
    processed_at: Optional[datetime]

    class Config:
        orm_mode = True


class GradeOverride(BaseModel):
    """
    Schema for overriding a grade.
    """
    grade_id: int
    new_score: float
    reason: str


class GradeResponse(BaseModel):
    """
    Schema for the response when a grade is retrieved.
    """
    id: int
    score: float
    feedback: str
    reasoning: str
    hash_signature: str

    class Config:
        orm_mode = True


class AnalyticsResponse(BaseModel):
    """
    Schema for the response when analytics are retrieved.
    """
    class_average: float
    distribution: dict
    common_errors: List[str]
