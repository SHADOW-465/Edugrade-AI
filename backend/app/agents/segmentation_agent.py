"""
Answer sheet segmentation agent for the EduGrade AI application.

This agent is responsible for identifying and cropping the individual answer
boxes from the preprocessed answer sheet images.
"""

from .base_agent import BaseAgent
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Dict, Any

class SegmentationAgent(BaseAgent):
    """
    Agent for segmenting answer sheet images.

    This agent uses a YOLOv8 model to detect the answer boxes in the image
    and then crops them out.
    """
    def __init__(self, model_path: str):
        """
        Initializes the segmentation agent.

        Args:
            model_path: The path to the YOLOv8 model file.
        """
        super().__init__("segmentation_agent")
        self.model = YOLO(model_path)

    def detect_answer_boxes(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detects the answer boxes in an image.

        Args:
            image: The image to detect the answer boxes in.

        Returns:
            A list of dictionaries, where each dictionary contains the
            bounding box coordinates and the confidence score for an answer box.
        """
        results = self.model(image)
        boxes = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                boxes.append({
                    "box": [int(x1), int(y1), int(x2), int(y2)],
                    "confidence": float(box.conf)
                })

        # Sort boxes top-to-bottom, then left-to-right
        boxes.sort(key=lambda b: (b['box'][1], b['box'][0]))
        return boxes

    def crop_answers(self, image: np.ndarray, boxes: List[Dict[str, Any]]) -> List[np.ndarray]:
        """
        Crops the answer boxes from an image.

        Args:
            image: The image to crop the answer boxes from.
            boxes: A list of dictionaries containing the bounding box
                   coordinates for the answer boxes.

        Returns:
            A list of the cropped answer box images.
        """
        cropped_images = []
        for box_info in boxes:
            x1, y1, x2, y2 = box_info['box']
            cropped_images.append(image[y1:y2, x1:x2])
        return cropped_images

    def process(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Processes an image.

        Args:
            image: The image to process.

        Returns:
            A dictionary containing the detected answer boxes, the cropped
            answer images, and the status of the operation.
        """
        try:
            detected_boxes = self.detect_answer_boxes(image)
            if not detected_boxes:
                # Fallback to grid-based segmentation if detection fails
                self.logger.warning("No answer boxes detected, falling back to grid-based segmentation.")
                # Implement grid-based segmentation logic here if needed
                return {
                    "answer_boxes": [],
                    "status": "fallback",
                    "message": "No answer boxes detected."
                }

            cropped_answers = self.crop_answers(image, detected_boxes)
            return {
                "answer_boxes": detected_boxes,
                "cropped_answers": cropped_answers,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error segmenting image: {e}")
            return {
                "answer_boxes": [],
                "cropped_answers": [],
                "status": "error",
                "error_message": str(e)
            }
