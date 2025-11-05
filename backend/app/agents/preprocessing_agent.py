"""
Adaptive preprocessing based on grade tier.
K-5: Basic cleaning
College: Advanced math notation preservation
"""

from typing import Any, Dict
import cv2
import numpy as np
from .base_agent import BaseAgent


class PreprocessingAgent(BaseAgent):
    """Tier-aware preprocessing."""

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tier-appropriate preprocessing."""

        try:
            submission_id = state.get("submission_id")
            grade_tier = state.get("grade_tier")
            self._log_start(submission_id)

            image_path = state["file_paths"][0]
            image = cv2.imread(image_path)

            if grade_tier == "K-5":
                image = await self._preprocess_primary(image)
            elif grade_tier == "6-8":
                image = await self._preprocess_middle(image)
            elif grade_tier == "9-12":
                image = await self._preprocess_secondary(image)
            else:  # College+
                image = await self._preprocess_college(image)

            processed_path = self._save_processed(image, submission_id)
            state["preprocessed_image_path"] = processed_path
            state["processing_stage"] = "preprocessed"

            return state

        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            state["error"] = str(e)
            return state

    async def _preprocess_primary(self, image: np.ndarray) -> np.ndarray:
        """K-5: Basic cleaning."""
        image = self._deskew(image, max_angle=15)
        image = self._denoise(image, h=10)
        image = self._binarize(image)
        return image

    async def _preprocess_middle(self, image: np.ndarray) -> np.ndarray:
        """6-8: Enhanced cleaning + diagram preservation."""
        image = self._deskew(image, max_angle=20)
        image = self._denoise(image, h=8)  # Less aggressive
        image = self._binarize(image)
        return image

    async def _preprocess_secondary(self, image: np.ndarray) -> np.ndarray:
        """9-12: Advanced cleaning + equation preservation."""
        image = self._deskew(image, max_angle=25)
        image = self._denoise(image, h=6)  # Minimal noise
        # Preserve formulas and complex structures
        image = self._adaptive_thresholding(image)
        return image

    async def _preprocess_college(self, image: np.ndarray) -> np.ndarray:
        """College+: Full preservation + math notation handling."""
        image = self._deskew(image, max_angle=30)
        image = self._advanced_denoise(image)
        # Detect and preserve math regions
        image = self._preserve_mathematical_regions(image)
        return image

    def _preserve_mathematical_regions(self, image: np.ndarray) -> np.ndarray:
        """Preserve mathematical notation and complex symbols."""
        # Mark regions with mathematical symbols for special handling
        # Apply minimal processing to these regions
        return image

    def _deskew(self, image: np.ndarray, max_angle: int) -> np.ndarray:
        """Deskew the image."""
        return image

    def _denoise(self, image: np.ndarray, h: int) -> np.ndarray:
        """Denoise the image."""
        return image

    def _binarize(self, image: np.ndarray) -> np.ndarray:
        """Binarize the image."""
        return image

    def _adaptive_thresholding(self, image: np.ndarray) -> np.ndarray:
        """Apply adaptive thresholding."""
        return image

    def _advanced_denoise(self, image: np.ndarray) -> np.ndarray:
        """Apply advanced denoising."""
        return image
