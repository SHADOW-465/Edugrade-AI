"""
Adaptive OCR using tier-appropriate models and ensemble strategies.
"""

from typing import Any, Dict, Tuple
from PIL import Image
import torch
from .base_agent import BaseAgent


class OCRAgent(BaseAgent):
    """Tier-aware OCR extraction."""

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text using tier-appropriate OCR."""

        try:
            submission_id = state.get("submission_id")
            grade_tier = state.get("grade_tier")
            self._log_start(submission_id)

            regions = state["segmented_regions"]
            ocr_results = []

            for region in regions:
                if grade_tier == "K-5":
                    text, conf = await self._ocr_primary(region["image"])
                elif grade_tier == "6-8":
                    text, conf = await self._ocr_middle(region["image"])
                elif grade_tier == "9-12":
                    text, conf = await self._ocr_secondary(region["image"])
                else:  # College+
                    text, conf = await self._ocr_college(region["image"])

                ocr_results.append({
                    "question_number": region["question_number"],
                    "extracted_text": text,
                    "confidence": conf,
                    "coordinates": region["coordinates"]
                })

            state["ocr_results"] = ocr_results
            state["processing_stage"] = "ocr_completed"

            return state

        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            state["error"] = str(e)
            return state

    async def _ocr_primary(self, image: 'np.ndarray') -> Tuple[str, float]:
        """K-5: TrOCR-small (lightweight)."""
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel

        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")

        pil_image = Image.fromarray(image.astype('uint8'))
        pixel_values = processor(pil_image, return_tensors="pt").pixel_values

        with torch.no_grad():
            generated_ids = model.generate(pixel_values, max_length=128)

        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        confidence = min(1.0, len(text) / 40)

        return text, confidence

    async def _ocr_middle(self, image: 'np.ndarray') -> Tuple[str, float]:
        """6-8: TrOCR-base + diagram detection."""
        # Use TrOCR base model
        # Also detect diagrams and handle separately
        text, conf = await self._ocr_with_model(image, "microsoft/trocr-base-handwritten")

        # Check for diagram elements
        diagram_detected = await self._detect_diagram_region(image)
        if diagram_detected:
            text += "[DIAGRAM DETECTED]"

        return text, conf

    async def _ocr_secondary(self, image: 'np.ndarray') -> Tuple[str, float]:
        """9-12: Ensemble OCR + Math notation parsing."""
        # TrOCR + PaddleOCR ensemble
        text1, conf1 = await self._ocr_with_model(image, "microsoft/trocr-large-handwritten")
        text2, conf2 = await self._ocr_paddleocr(image)

        # Ensemble result
        text = self._ensemble_ocr_results([text1, text2])

        # Parse mathematical notation
        math_text = await self._parse_math_notation(text)

        return math_text, max(conf1, conf2)

    async def _ocr_college(self, image: 'np.ndarray') -> Tuple[str, float]:
        """College+: Full ensemble + LaTeX parsing + code detection."""

        # Multiple OCR passes
        ocr_results = []
        ocr_results.append(await self._ocr_with_model(image, "microsoft/trocr-large-handwritten"))
        ocr_results.append(await self._ocr_paddleocr(image))

        # Weighted ensemble
        text = await self._weighted_ocr_ensemble(ocr_results)

        # Parse LaTeX/math
        text = await self._parse_latex(text)

        # Detect code blocks
        if self._is_code_block(image):
            text += "\n[CODE BLOCK DETECTED]\n"

        confidence = max([r[1] for r in ocr_results])

        return text, confidence

    async def _ocr_with_model(self, image: 'np.ndarray', model_name: str) -> Tuple[str, float]:
        """OCR with a given model."""
        return "text", 0.9

    async def _detect_diagram_region(self, image: 'np.ndarray') -> bool:
        """Detect diagram region."""
        return False

    async def _ocr_paddleocr(self, image: 'np.ndarray') -> Tuple[str, float]:
        """OCR with PaddleOCR."""
        return "text", 0.9

    def _ensemble_ocr_results(self, results: list) -> str:
        """Ensemble OCR results."""
        return "text"

    async def _parse_math_notation(self, text: str) -> str:
        """Parse math notation."""
        return text

    async def _weighted_ocr_ensemble(self, results: list) -> str:
        """Weighted ensemble of OCR results."""
        return "text"

    async def _parse_latex(self, text: str) -> str:
        """Parse LaTeX."""
        return text

    def _is_code_block(self, image: 'np.ndarray') -> bool:
        """Check if the image is a code block."""
        return False
