"""
Storage agent for the EduGrade AI application.

This agent is responsible for storing the grading results in the database
and for computing a cryptographic hash to ensure the integrity of the grades.
"""

from .base_agent import BaseAgent
from typing import List, Dict, Any
import hashlib
import json
from sqlalchemy.orm import Session
from ..models import database as db_models
from datetime import datetime

class StorageAgent(BaseAgent):
    """
    Agent for storing grading results.

    This agent stores the grading results in the database and computes a
    cryptographic hash to ensure the integrity of the grades.
    """
    def __init__(self, db_session: Session):
        """
        Initializes the storage agent.

        Args:
            db_session: The database session to use.
        """
        super().__init__("storage_agent")
        self.db = db_session

    def compute_hash(self, grade_data: Dict[str, Any]) -> str:
        """
        Computes a SHA-256 hash of the grade data.

        Args:
            grade_data: A dictionary containing the grade data.

        Returns:
            The SHA-256 hash of the grade data.
        """
        # Create a canonical JSON string to ensure consistent hashing
        canonical_string = json.dumps(grade_data, sort_keys=True)
        return hashlib.sha256(canonical_string.encode()).hexdigest()

    def store_grades(self, grades: List[Dict[str, Any]], submission_id: int) -> bool:
        """
        Stores the grades for a submission in the database.

        Args:
            grades: A list of dictionaries, where each dictionary contains
                    the grade data for a question.
            submission_id: The ID of the submission.

        Returns:
            True if the grades were stored successfully, False otherwise.
        """
        try:
            for grade_data in grades:
                grade_data_to_hash = {
                    "submission_id": submission_id,
                    "question_number": grade_data["question_number"],
                    "score": grade_data["score"],
                    "timestamp": datetime.utcnow().isoformat() # to ensure uniqueness
                }
                hash_signature = self.compute_hash(grade_data_to_hash)

                db_grade = db_models.Grade(
                    submission_id=submission_id,
                    question_number=grade_data["question_number"],
                    extracted_text=grade_data["extracted_text"],
                    score=grade_data["score"],
                    max_score=grade_data["max_score"],
                    feedback=grade_data["feedback"],
                    reasoning=grade_data["reasoning"],
                    points_covered=grade_data["points_covered"],
                    points_missed=grade_data["points_missed"],
                    hash_signature=hash_signature,
                )
                self.db.add(db_grade)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Error storing grades for submission {submission_id}: {e}")
            return False

    def verify_integrity(self, grade_id: int) -> bool:
        """
        Verifies the integrity of a grade.

        Args:
            grade_id: The ID of the grade to verify.

        Returns:
            True if the grade is valid, False otherwise.
        """
        db_grade = self.db.query(db_models.Grade).filter(db_models.Grade.id == grade_id).first()
        if not db_grade:
            return False

        grade_data_to_hash = {
            "submission_id": db_grade.submission_id,
            "question_number": db_grade.question_number,
            "score": db_grade.score,
            # This is a simplification. In a real system, you'd need to store the timestamp
            # or have a consistent way to recreate the exact data that was hashed.
            "timestamp": db_grade.created_at.isoformat()
        }
        recomputed_hash = self.compute_hash(grade_data_to_hash)
        return recomputed_hash == db_grade.hash_signature

    def process(self, grading_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the grading results to store them in the database.

        Args:
            grading_results: A dictionary containing the grading results.

        Returns:
            A dictionary containing the status of the storage operation.
        """
        success = self.store_grades(grading_results["grades"], grading_results["submission_id"])
        if success:
            return {
                "storage_status": "success",
                "message": f"Grades for submission {grading_results['submission_id']} stored successfully."
            }
        else:
            return {
                "storage_status": "error",
                "message": f"Failed to store grades for submission {grading_results['submission_id']}."
            }
