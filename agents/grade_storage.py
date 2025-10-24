"""
Grade Storage Agent for EduGrade AI
Handles secure storage of grades with SHA-256 cryptographic hashing
Creates tamper-proof grade records with timestamps
"""

import hashlib
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from dataclasses import dataclass, asdict
import os

logger = logging.getLogger(__name__)

@dataclass
class GradeRecord:
    """Immutable grade record with cryptographic verification"""
    student_id: str
    exam_id: str
    question_id: str
    answer_text: str
    score: float
    max_score: float
    percentage: float
    feedback: str
    timestamp: str
    previous_hash: str
    current_hash: str
    metadata: Dict[str, Any]

class GradeStorageAgent:
    """Agent responsible for secure grade storage and verification"""
    
    def __init__(self, db_path: str = "grades.db", storage_dir: str = "./grades"):
        """
        Initialize the Grade Storage Agent
        
        Args:
            db_path: Path to SQLite database
            storage_dir: Directory for file-based storage
        """
        self.db_path = db_path
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Chain of grade records for verification
        self.grade_chain = []
        self._load_existing_chain()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create grades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    exam_id TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    answer_text TEXT NOT NULL,
                    score REAL NOT NULL,
                    max_score REAL NOT NULL,
                    percentage REAL NOT NULL,
                    feedback TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    previous_hash TEXT NOT NULL,
                    current_hash TEXT NOT NULL UNIQUE,
                    metadata TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_student_exam 
                ON grades(student_id, exam_id)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_hash 
                ON grades(current_hash)
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def _load_existing_chain(self):
        """Load existing grade records to maintain chain integrity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT student_id, exam_id, question_id, answer_text, score, max_score,
                       percentage, feedback, timestamp, previous_hash, current_hash, metadata
                FROM grades
                ORDER BY created_at ASC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                grade_record = GradeRecord(
                    student_id=row[0],
                    exam_id=row[1],
                    question_id=row[2],
                    answer_text=row[3],
                    score=row[4],
                    max_score=row[5],
                    percentage=row[6],
                    feedback=row[7],
                    timestamp=row[8],
                    previous_hash=row[9],
                    current_hash=row[10],
                    metadata=json.loads(row[11])
                )
                self.grade_chain.append(grade_record)
            
            logger.info(f"Loaded {len(self.grade_chain)} existing grade records")
            
        except Exception as e:
            logger.warning(f"Failed to load existing chain: {e}")
            self.grade_chain = []
    
    def store_grade(self, 
                   student_id: str,
                   exam_id: str,
                   question_id: str,
                   answer_text: str,
                   score: float,
                   max_score: float,
                   percentage: float,
                   feedback: str,
                   metadata: Dict[str, Any] = None) -> GradeRecord:
        """
        Store a grade record with cryptographic verification
        
        Args:
            student_id: Unique student identifier
            exam_id: Unique exam identifier
            question_id: Unique question identifier
            answer_text: The student's answer text
            score: Achieved score
            max_score: Maximum possible score
            percentage: Score percentage
            feedback: Teacher feedback
            metadata: Additional metadata
            
        Returns:
            GradeRecord object with cryptographic hashes
        """
        try:
            # Prepare metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'stored_at': datetime.now(timezone.utc).isoformat(),
                'version': '1.0',
                'agent': 'grade_storage_agent'
            })
            
            # Get previous hash (last record in chain)
            previous_hash = self._get_last_hash()
            
            # Create timestamp
            timestamp = datetime.now(timezone.utc).isoformat()
            
            # Create grade record
            grade_record = GradeRecord(
                student_id=student_id,
                exam_id=exam_id,
                question_id=question_id,
                answer_text=answer_text,
                score=score,
                max_score=max_score,
                percentage=percentage,
                feedback=feedback,
                timestamp=timestamp,
                previous_hash=previous_hash,
                current_hash="",  # Will be calculated
                metadata=metadata
            )
            
            # Calculate hash
            grade_record.current_hash = self._calculate_hash(grade_record)
            
            # Store in database
            self._store_in_database(grade_record)
            
            # Add to chain
            self.grade_chain.append(grade_record)
            
            # Save to file system
            self._save_to_file(grade_record)
            
            logger.info(f"Grade stored successfully for student {student_id}, question {question_id}")
            return grade_record
            
        except Exception as e:
            logger.error(f"Failed to store grade: {e}")
            raise
    
    def _get_last_hash(self) -> str:
        """Get hash of the last record in the chain"""
        if not self.grade_chain:
            return "0" * 64  # Genesis hash
        
        return self.grade_chain[-1].current_hash
    
    def _calculate_hash(self, grade_record: GradeRecord) -> str:
        """Calculate SHA-256 hash for grade record"""
        # Create data string for hashing
        data_string = f"{grade_record.student_id}{grade_record.exam_id}{grade_record.question_id}"
        data_string += f"{grade_record.answer_text}{grade_record.score}{grade_record.max_score}"
        data_string += f"{grade_record.percentage}{grade_record.feedback}{grade_record.timestamp}"
        data_string += f"{grade_record.previous_hash}{json.dumps(grade_record.metadata, sort_keys=True)}"
        
        # Calculate SHA-256 hash
        hash_object = hashlib.sha256(data_string.encode('utf-8'))
        return hash_object.hexdigest()
    
    def _store_in_database(self, grade_record: GradeRecord):
        """Store grade record in SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO grades (student_id, exam_id, question_id, answer_text, score, max_score,
                                  percentage, feedback, timestamp, previous_hash, current_hash, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                grade_record.student_id,
                grade_record.exam_id,
                grade_record.question_id,
                grade_record.answer_text,
                grade_record.score,
                grade_record.max_score,
                grade_record.percentage,
                grade_record.feedback,
                grade_record.timestamp,
                grade_record.previous_hash,
                grade_record.current_hash,
                json.dumps(grade_record.metadata)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store in database: {e}")
            raise
    
    def _save_to_file(self, grade_record: GradeRecord):
        """Save grade record to file system for backup"""
        try:
            # Create directory structure
            student_dir = self.storage_dir / grade_record.student_id
            exam_dir = student_dir / grade_record.exam_id
            exam_dir.mkdir(parents=True, exist_ok=True)
            
            # Save individual record
            record_file = exam_dir / f"{grade_record.question_id}_{grade_record.timestamp}.json"
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(grade_record), f, indent=2, ensure_ascii=False)
            
            # Update chain file
            chain_file = self.storage_dir / "grade_chain.json"
            chain_data = [asdict(record) for record in self.grade_chain]
            
            with open(chain_file, 'w', encoding='utf-8') as f:
                json.dump(chain_data, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.warning(f"Failed to save to file: {e}")
    
    def verify_chain_integrity(self) -> Dict[str, Any]:
        """
        Verify the integrity of the grade chain
        
        Returns:
            Dictionary with verification results
        """
        verification_result = {
            'is_valid': True,
            'total_records': len(self.grade_chain),
            'invalid_records': [],
            'chain_breaks': []
        }
        
        try:
            for i, record in enumerate(self.grade_chain):
                # Verify current record hash
                expected_hash = self._calculate_hash(record)
                if record.current_hash != expected_hash:
                    verification_result['invalid_records'].append({
                        'index': i,
                        'student_id': record.student_id,
                        'question_id': record.question_id,
                        'expected_hash': expected_hash,
                        'actual_hash': record.current_hash
                    })
                    verification_result['is_valid'] = False
                
                # Verify chain continuity
                if i > 0:
                    if record.previous_hash != self.grade_chain[i-1].current_hash:
                        verification_result['chain_breaks'].append({
                            'index': i,
                            'student_id': record.student_id,
                            'question_id': record.question_id,
                            'expected_previous_hash': self.grade_chain[i-1].current_hash,
                            'actual_previous_hash': record.previous_hash
                        })
                        verification_result['is_valid'] = False
            
            logger.info(f"Chain verification completed. Valid: {verification_result['is_valid']}")
            
        except Exception as e:
            logger.error(f"Chain verification failed: {e}")
            verification_result['is_valid'] = False
            verification_result['error'] = str(e)
        
        return verification_result
    
    def get_student_grades(self, student_id: str, exam_id: str = None) -> List[GradeRecord]:
        """
        Retrieve grades for a specific student
        
        Args:
            student_id: Student identifier
            exam_id: Optional exam identifier to filter
            
        Returns:
            List of grade records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if exam_id:
                cursor.execute('''
                    SELECT student_id, exam_id, question_id, answer_text, score, max_score,
                           percentage, feedback, timestamp, previous_hash, current_hash, metadata
                    FROM grades
                    WHERE student_id = ? AND exam_id = ?
                    ORDER BY timestamp ASC
                ''', (student_id, exam_id))
            else:
                cursor.execute('''
                    SELECT student_id, exam_id, question_id, answer_text, score, max_score,
                           percentage, feedback, timestamp, previous_hash, current_hash, metadata
                    FROM grades
                    WHERE student_id = ?
                    ORDER BY timestamp ASC
                ''', (student_id,))
            
            rows = cursor.fetchall()
            conn.close()
            
            grades = []
            for row in rows:
                grade_record = GradeRecord(
                    student_id=row[0],
                    exam_id=row[1],
                    question_id=row[2],
                    answer_text=row[3],
                    score=row[4],
                    max_score=row[5],
                    percentage=row[6],
                    feedback=row[7],
                    timestamp=row[8],
                    previous_hash=row[9],
                    current_hash=row[10],
                    metadata=json.loads(row[11])
                )
                grades.append(grade_record)
            
            return grades
            
        except Exception as e:
            logger.error(f"Failed to retrieve student grades: {e}")
            return []
    
    def get_exam_analytics(self, exam_id: str) -> Dict[str, Any]:
        """
        Get analytics for a specific exam
        
        Args:
            exam_id: Exam identifier
            
        Returns:
            Dictionary with exam analytics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get basic statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_answers,
                    AVG(percentage) as avg_percentage,
                    MIN(percentage) as min_percentage,
                    MAX(percentage) as max_percentage,
                    COUNT(DISTINCT student_id) as unique_students
                FROM grades
                WHERE exam_id = ?
            ''', (exam_id,))
            
            stats = cursor.fetchone()
            
            # Get grade distribution
            cursor.execute('''
                SELECT 
                    CASE 
                        WHEN percentage >= 90 THEN 'A'
                        WHEN percentage >= 80 THEN 'B'
                        WHEN percentage >= 70 THEN 'C'
                        WHEN percentage >= 60 THEN 'D'
                        ELSE 'F'
                    END as grade,
                    COUNT(*) as count
                FROM grades
                WHERE exam_id = ?
                GROUP BY grade
                ORDER BY grade
            ''', (exam_id,))
            
            grade_distribution = dict(cursor.fetchall())
            
            conn.close()
            
            return {
                'exam_id': exam_id,
                'total_answers': stats[0],
                'unique_students': stats[4],
                'average_percentage': round(stats[1], 2) if stats[1] else 0,
                'min_percentage': round(stats[2], 2) if stats[2] else 0,
                'max_percentage': round(stats[3], 2) if stats[3] else 0,
                'grade_distribution': grade_distribution
            }
            
        except Exception as e:
            logger.error(f"Failed to get exam analytics: {e}")
            return {}
    
    def export_grades(self, output_path: str, exam_id: str = None):
        """Export grades to JSON file"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if exam_id:
                cursor.execute('''
                    SELECT * FROM grades WHERE exam_id = ? ORDER BY student_id, question_id
                ''', (exam_id,))
            else:
                cursor.execute('''
                    SELECT * FROM grades ORDER BY student_id, exam_id, question_id
                ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            # Convert to list of dictionaries
            grades_data = []
            for row in rows:
                grade_dict = {
                    'id': row[0],
                    'student_id': row[1],
                    'exam_id': row[2],
                    'question_id': row[3],
                    'answer_text': row[4],
                    'score': row[5],
                    'max_score': row[6],
                    'percentage': row[7],
                    'feedback': row[8],
                    'timestamp': row[9],
                    'previous_hash': row[10],
                    'current_hash': row[11],
                    'metadata': json.loads(row[12]),
                    'created_at': row[13]
                }
                grades_data.append(grade_dict)
            
            # Save to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(grades_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Grades exported to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export grades: {e}")
            raise

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize agent
    agent = GradeStorageAgent()
    
    # Test storing a grade
    # grade_record = agent.store_grade(
    #     student_id="STU001",
    #     exam_id="EXAM001",
    #     question_id="Q001",
    #     answer_text="The answer is photosynthesis",
    #     score=8.5,
    #     max_score=10.0,
    #     percentage=85.0,
    #     feedback="Good understanding of the concept",
    #     metadata={"teacher": "Dr. Smith", "subject": "Biology"}
    # )
    # print(f"Grade stored with hash: {grade_record.current_hash}")
    
    # Verify chain integrity
    # verification = agent.verify_chain_integrity()
    # print(f"Chain integrity: {verification['is_valid']}")
