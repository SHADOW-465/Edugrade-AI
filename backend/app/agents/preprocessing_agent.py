"""
Image preprocessing agent for the EduGrade AI application.

This agent is responsible for cleaning and preparing the uploaded answer
sheet images for further processing.
"""

from .base_agent import BaseAgent
import cv2
import numpy as np
from typing import Dict, Any

class PreprocessingAgent(BaseAgent):
    """
    Agent for preprocessing answer sheet images.

    This agent performs deskewing, denoising, and binarization of the images.
    """
    def __init__(self):
        """
        Initializes the preprocessing agent.
        """
        super().__init__("preprocessing_agent")

    def deskew_image(self, image: np.ndarray) -> np.ndarray:
        """
        Deskews an image.

        Args:
            image: The image to deskew.

        Returns:
            The deskewed image.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    def denoise_image(self, image: np.ndarray) -> np.ndarray:
        """
        Denoises an image.

        Args:
            image: The image to denoise.

        Returns:
            The denoised image.
        """
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

    def binarize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Binarizes an image.

        Args:
            image: The image to binarize.

        Returns:
            The binarized image.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

    def process(self, image_path: str) -> Dict[str, Any]:
        """
        Processes an image.

        Args:
            image_path: The path to the image to process.

        Returns:
            A dictionary containing the preprocessed image and the status of
            the operation.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image from path: {image_path}")

            deskewed_image = self.deskew_image(image)
            denoised_image = self.denoise_image(deskewed_image)
            binarized_image = self.binarize_image(denoised_image)

            return {
                "preprocessed_image": binarized_image,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {e}")
            return {
                "preprocessed_image": None,
                "status": "error",
                "error_message": str(e)
            }
