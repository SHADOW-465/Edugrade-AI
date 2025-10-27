"""
Firestore data models for EduGrade AI.
"""

from datetime import datetime
from typing import Dict, List, Optional
from app.core.firebase_db import db


class Exam:
    collection = db.collection("exams")

    @staticmethod
    def create(data: Dict):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = None
        doc_ref = Exam.collection.add(data)
        return doc_ref[1].id

    @staticmethod
    def get(exam_id: str):
        doc = Exam.collection.document(exam_id).get()
        return doc.to_dict() if doc.exists else None

    @staticmethod
    def list_all():
        return [doc.to_dict() for doc in Exam.collection.stream()]

    @staticmethod
    def update(exam_id: str, data: Dict):
        data["updated_at"] = datetime.utcnow()
        Exam.collection.document(exam_id).update(data)
        return True


class Submission:
    collection = db.collection("submissions")

    @staticmethod
    def create(data: Dict):
        data["uploaded_at"] = datetime.utcnow()
        data["status"] = "pending"
        doc_ref = Submission.collection.add(data)
        return doc_ref[1].id

    @staticmethod
    def get(submission_id: str):
        doc = Submission.collection.document(submission_id).get()
        return doc.to_dict() if doc.exists else None

    @staticmethod
    def update(submission_id: str, data: Dict):
        data["processed_at"] = datetime.utcnow()
        Submission.collection.document(submission_id).update(data)
        return True
