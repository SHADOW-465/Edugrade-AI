"""
SQLAlchemy ORM models for the EduGrade AI application.

This file defines the database tables as Python classes using SQLAlchemy's
declarative base.
"""

import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class StatusEnum(str, enum.Enum):
    """
    Enum for the status of a submission.
    """
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Exam(Base):
    """
    Represents an exam in the database.
    """
    __tablename__ = "exams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String)
    total_questions = Column(Integer)
    answer_key = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submissions = relationship("Submission", back_populates="exam", cascade="all, delete-orphan")


class Submission(Base):
    """
    Represents a student's submission for an exam.
    """
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"))
    student_name = Column(String)
    student_id = Column(String)
    image_path = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    exam = relationship("Exam", back_populates="submissions")
    grades = relationship("Grade", back_populates="submission", cascade="all, delete-orphan")


class Grade(Base):
    """
    Represents a grade for a single question in a submission.
    """
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    question_number = Column(Integer)
    extracted_text = Column(String)
    score = Column(Float)
    max_score = Column(Float)
    feedback = Column(String)
    reasoning = Column(String)
    points_covered = Column(JSON)
    points_missed = Column(JSON)
    hash_signature = Column(String, unique=True)
    teacher_override = Column(Boolean, default=False)
    override_reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submission = relationship("Submission", back_populates="grades")


class User(Base):
    """
    Represents a user of the application (e.g., a teacher or admin).
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
