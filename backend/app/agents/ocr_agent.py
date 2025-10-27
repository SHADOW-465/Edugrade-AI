"""
OCR agent for the EduGrade AI application.

This agent is responsible for extracting text from the cropped answer
images using an ensemble of OCR models.
"""

from .base_agent import BaseAgent
import numpy as np
from typing import List, Dict, Any, Tuple
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import requests # Assuming DeepSeek-OCR is accessed via API

class OCRAgent(BaseAgent):
    """
    Agent for extracting text from images using OCR.

    This agent uses an ensemble of TrOCR and DeepSeek-OCR to extract text
    from the cropped answer images.
    """
    def __init__(self, deepseek_api_key: str):
        """
        Initializes the OCR agent.

        Args:
            deepseek_api_key: The API key for the DeepSeek-OCR service.
        """
        super().__init__("ocr_agent")
        self.processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
        self.model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
        self.deepseek_api_key = deepseek_api_key

    def extract_trocr(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Extracts text from an image using TrOCR.

        Args:
            image: The image to extract text from.

        Returns:
            A tuple containing the extracted text and a confidence score.
        """
        pil_image = Image.fromarray(image).convert("RGB")
        pixel_values = self.processor(images=pil_image, return_tensors="pt").pixel_values
        generated_ids = self.model.generate(pixel_values)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        # TrOCR does not provide a direct confidence score, so we'll have to use a placeholder.
        return generated_text, 0.9

    def extract_deepseek(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Extracts text from an image using DeepSeek-OCR.

        Args:
            image: The image to extract text from.

        Returns:
            A tuple containing the extracted text and a confidence score.
        """
        # This is a placeholder for DeepSeek-OCR API call
        # You would replace this with the actual API call
        # For now, let's simulate a response
        return "deepseek text", 0.95

    def ensemble_extract(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extracts text from an image using an ensemble of OCR models.

        Args:
            image: The image to extract text from.

        Returns:
            A dictionary containing the extracted text, the confidence score,
            the source model, and the alternative results.
        """
        trocr_text, trocr_confidence = self.extract_trocr(image)
        deepseek_text, deepseek_confidence = self.extract_deepseek(image)

        # Simple ensemble: choose the one with higher confidence
        if trocr_confidence > deepseek_confidence:
            best_text = trocr_text
            best_confidence = trocr_confidence
            source_model = "TrOCR"
        else:
            best_text = deepseek_text
            best_confidence = deepseek_confidence
            source_model = "DeepSeek-OCR"

        return {
            "text": best_text,
            "confidence": best_confidence,
            "source_model": source_model,
            "alternatives": {
                "trocr": trocr_text,
                "deepseek": deepseek_text
            }
        }

    def process(self, answer_images: List[np.ndarray]) -> Dict[str, Any]:
        """
        Processes a list of answer images.

        Args:
            answer_images: A list of the answer images to process.

        Returns:
            A dictionary containing the OCR results and the status of the
            operation.
        """
        ocr_results = []
        try:
            for image in answer_images:
                result = self.ensemble_extract(image)
                ocr_results.append(result)
            return {
                "ocr_results": ocr_results,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error during OCR processing: {e}")
            return {
                "ocr_results": [],
                "status": "error",
                "error_message": str(e)
            }
