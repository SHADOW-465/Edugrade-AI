"""
Adaptive state that changes based on grade tier.
"""

from typing import TypedDict, List, Dict, Any, Optional


class GradingState(TypedDict):
    # Metadata
    submission_id: str
    exam_id: str
    student_name: str
    student_id: str
    student_grade_level: str
    grade_tier: str  # K-5, 6-8, 9-12, College
    grade_tier_confidence: float
    file_paths: List[str]
    answer_key: Dict[str, Any]

    # Processing
    status: str
    processing_stage: str

    # Agent outputs
    preprocessed_image_path: Optional[str]
    segmented_regions: Optional[List[Dict]]
    answer_boxes: Optional[List[Dict]]
    ocr_results: Optional[List[Dict]]
    grades: Optional[List[Dict]]
    feedback: Optional[str]

    # College-specific
    plagiarism_checked: Optional[bool]
    plagiarism_score: Optional[float]

    # Errors
    error: Optional[str]
    created_at: float
    teacher_id: str
