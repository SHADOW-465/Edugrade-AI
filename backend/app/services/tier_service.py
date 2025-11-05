"""
Automatically detect student grade level from answer sheet content.
Used to configure entire grading pipeline.
"""

from enum import Enum
from typing import Dict, Tuple
from PIL import Image
import numpy as np

class GradeTier(Enum):
    """Grade level classification."""
    PRIMARY = "K-5"           # Kindergarten to 5th
    MIDDLE = "6-8"            # Middle school
    SECONDARY = "9-12"        # High school
    COLLEGE = "College+"      # College and above

class TierService:
    """Detect and configure grade tier."""

    @staticmethod
    async def detect_tier_from_image(image: np.ndarray) -> Tuple[GradeTier, float]:
        """
        Analyze image to detect grade tier.

        Heuristics:
        - Image complexity (detailed drawings/diagrams = higher tier)
        - Text complexity (mathematical notation = higher tier)
        - Handwriting maturity (cursive quality = higher tier)
        - Layout sophistication (multi-column = higher tier)

        Returns: (GradeTier, confidence: 0-1)
        """

        # Extract features
        text_complexity = await TierService._analyze_text_complexity(image)
        handwriting_quality = await TierService._analyze_handwriting_quality(image)
        diagram_presence = await TierService._detect_diagrams(image)
        notation_complexity = await TierService._detect_notation(image)

        # Decision logic
        if notation_complexity > 0.7:  # Mathematical notation detected
            return (GradeTier.COLLEGE, 0.9)
        elif notation_complexity > 0.4:  # Some formulas
            return (GradeTier.SECONDARY, 0.85)
        elif handwriting_quality > 0.8 and diagram_presence > 0.5:
            return (GradeTier.MIDDLE, 0.8)
        elif diagram_presence > 0.3:
            return (GradeTier.MIDDLE, 0.75)
        else:
            return (GradeTier.PRIMARY, 0.85)

    @staticmethod
    async def _analyze_text_complexity(image: np.ndarray) -> float:
        """Analyze text for complexity indicators."""
        # A real implementation would use a model to analyze the text.
        # For now, we'll use a simple heuristic based on the image size.
        return image.size / 1000000.0

    @staticmethod
    async def _analyze_handwriting_quality(image: np.ndarray) -> float:
        """Assess handwriting maturity."""
        # A real implementation would use a model to analyze the handwriting.
        # For now, we'll use a simple heuristic based on the number of unique colors.
        return len(np.unique(image.reshape(-1, image.shape[2]))) / 1000.0

    @staticmethod
    async def _detect_diagrams(image: np.ndarray) -> float:
        """Detect presence and complexity of diagrams."""
        # A real implementation would use a model to detect diagrams.
        # For now, we'll use a simple heuristic based on the image's standard deviation.
        return np.std(image) / 100.0

    @staticmethod
    async def _detect_notation(image: np.ndarray) -> float:
        """Detect mathematical/scientific notation."""
        # A real implementation would use a model to detect notation.
        # For now, we'll use a simple heuristic based on the image's mean.
        return np.mean(image) / 255.0

    @staticmethod
    def get_tier_config(tier: GradeTier) -> Dict:
        """Return processing configuration for tier."""

        configs = {
            GradeTier.PRIMARY: {
                "ocr_model": "trocr-small",
                "yolo_model": "yolov8n.pt",
                "llm_model": "gemini-2.0-flash",
                "llm_temperature": 0.3,
                "grading_strategy": "exact_match",
                "max_attempts_per_question": 1,
                "supports_diagrams": False,
                "supports_equations": False,
                "feedback_style": "encouraging"
            },
            GradeTier.MIDDLE: {
                "ocr_model": "trocr-base",
                "yolo_model": "yolov8m.pt",
                "llm_model": "gemini-2.0-flash",
                "llm_temperature": 0.5,
                "grading_strategy": "semantic",
                "max_attempts_per_question": 2,
                "supports_diagrams": True,
                "supports_equations": False,
                "feedback_style": "constructive"
            },
            GradeTier.SECONDARY: {
                "ocr_model": "trocr-large",
                "yolo_model": "yolov8m.pt",
                "llm_model": "gemini-pro",
                "llm_temperature": 0.6,
                "grading_strategy": "advanced_rubric",
                "max_attempts_per_question": 3,
                "supports_diagrams": True,
                "supports_equations": True,
                "feedback_style": "academic_critique"
            },
            GradeTier.COLLEGE: {
                "ocr_model": "ensemble",  # TrOCR + PaddleOCR + custom
                "yolo_model": "yolov8l.pt",
                "llm_model": "gemini-pro",
                "llm_temperature": 0.7,
                "grading_strategy": "advanced_reasoning",
                "max_attempts_per_question": 5,
                "supports_diagrams": True,
                "supports_equations": True,
                "supports_code": True,
                "supports_research": True,
                "plagiarism_check": True,
                "feedback_style": "scholarly"
            }
        }

        return configs.get(tier, configs[GradeTier.PRIMARY])
