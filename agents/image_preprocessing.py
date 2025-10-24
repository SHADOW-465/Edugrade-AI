"""
Image Preprocessing Agent for EduGrade AI
Handles image alignment, rotation correction, and answer sheet detection using OpenCV and YOLOv8
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from pathlib import Path
import logging
from ultralytics import YOLO
from PIL import Image
import os

logger = logging.getLogger(__name__)

class ImagePreprocessingAgent:
    """Agent responsible for preprocessing answer sheet images"""
    
    def __init__(self, yolo_model_path: str = None, confidence_threshold: float = 0.5):
        """
        Initialize the Image Preprocessing Agent
        
        Args:
            yolo_model_path: Path to YOLOv8 model for answer sheet detection
            confidence_threshold: Minimum confidence for detection
        """
        self.confidence_threshold = confidence_threshold
        self.yolo_model = None
        
        if yolo_model_path and os.path.exists(yolo_model_path):
            try:
                self.yolo_model = YOLO(yolo_model_path)
                logger.info(f"YOLO model loaded from {yolo_model_path}")
            except Exception as e:
                logger.warning(f"Failed to load YOLO model: {e}")
                logger.info("Using OpenCV-based detection as fallback")
        else:
            logger.info("No YOLO model provided, using OpenCV-based detection")
    
    def preprocess_image(self, image_path: str) -> Dict:
        """
        Main preprocessing pipeline for answer sheet images
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Dictionary containing processed image data and metadata
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            original_image = image.copy()
            
            # Step 1: Image enhancement and noise reduction
            enhanced_image = self._enhance_image(image)
            
            # Step 2: Rotation correction
            corrected_image = self._correct_rotation(enhanced_image)
            
            # Step 3: Answer sheet detection and segmentation
            answer_boxes = self._detect_answer_boxes(corrected_image)
            
            # Step 4: Extract individual answer regions
            answer_patches = self._extract_answer_patches(corrected_image, answer_boxes)
            
            return {
                'original_image': original_image,
                'processed_image': corrected_image,
                'answer_boxes': answer_boxes,
                'answer_patches': answer_patches,
                'metadata': {
                    'image_path': image_path,
                    'original_shape': original_image.shape,
                    'processed_shape': corrected_image.shape,
                    'num_answers': len(answer_patches),
                    'preprocessing_success': True
                }
            }
            
        except Exception as e:
            logger.error(f"Error in image preprocessing: {e}")
            return {
                'error': str(e),
                'preprocessing_success': False
            }
    
    def _enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Enhance image quality for better processing"""
        # Convert to grayscale for processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Morphological operations to clean up the image
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
    
    def _correct_rotation(self, image: np.ndarray) -> np.ndarray:
        """Correct image rotation using contour detection"""
        # Find contours
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return image
        
        # Find the largest contour (likely the answer sheet)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the minimum area rectangle
        rect = cv2.minAreaRect(largest_contour)
        angle = rect[2]
        
        # Correct angle if it's significantly off
        if abs(angle) > 1:
            # Rotate the image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, rotation_matrix, (w, h), 
                                   flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            return rotated
        
        return image
    
    def _detect_answer_boxes(self, image: np.ndarray) -> List[Dict]:
        """Detect answer boxes using YOLO or OpenCV-based methods"""
        if self.yolo_model:
            return self._detect_with_yolo(image)
        else:
            return self._detect_with_opencv(image)
    
    def _detect_with_yolo(self, image: np.ndarray) -> List[Dict]:
        """Detect answer boxes using YOLOv8"""
        try:
            results = self.yolo_model(image, conf=self.confidence_threshold)
            
            answer_boxes = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = box.conf[0].cpu().numpy()
                        
                        answer_boxes.append({
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'confidence': float(confidence),
                            'class': 'answer_box'
                        })
            
            return answer_boxes
            
        except Exception as e:
            logger.warning(f"YOLO detection failed: {e}, falling back to OpenCV")
            return self._detect_with_opencv(image)
    
    def _detect_with_opencv(self, image: np.ndarray) -> List[Dict]:
        """Detect answer boxes using OpenCV contour detection"""
        # Find contours
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        answer_boxes = []
        min_area = 1000  # Minimum area for answer boxes
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by aspect ratio (answer boxes are typically rectangular)
                aspect_ratio = w / h
                if 0.5 < aspect_ratio < 3.0:
                    answer_boxes.append({
                        'bbox': [x, y, x + w, y + h],
                        'confidence': 0.8,  # Default confidence for OpenCV detection
                        'class': 'answer_box'
                    })
        
        # Sort by position (top to bottom, left to right)
        answer_boxes.sort(key=lambda x: (x['bbox'][1], x['bbox'][0]))
        
        return answer_boxes
    
    def _extract_answer_patches(self, image: np.ndarray, answer_boxes: List[Dict]) -> List[np.ndarray]:
        """Extract individual answer patches from detected boxes"""
        patches = []
        
        for i, box in enumerate(answer_boxes):
            x1, y1, x2, y2 = box['bbox']
            
            # Add padding around the box
            padding = 10
            h, w = image.shape[:2]
            
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(w, x2 + padding)
            y2 = min(h, y2 + padding)
            
            # Extract patch
            patch = image[y1:y2, x1:x2]
            
            if patch.size > 0:
                patches.append(patch)
                logger.debug(f"Extracted answer patch {i+1}: {patch.shape}")
        
        return patches
    
    def save_processed_data(self, processed_data: Dict, output_dir: str) -> Dict:
        """Save processed image data to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = {}
        
        try:
            # Save processed image
            processed_image_path = output_path / "processed_image.jpg"
            cv2.imwrite(str(processed_image_path), processed_data['processed_image'])
            saved_files['processed_image'] = str(processed_image_path)
            
            # Save answer patches
            patches_dir = output_path / "answer_patches"
            patches_dir.mkdir(exist_ok=True)
            
            for i, patch in enumerate(processed_data['answer_patches']):
                patch_path = patches_dir / f"answer_{i+1:03d}.jpg"
                cv2.imwrite(str(patch_path), patch)
                saved_files[f'answer_patch_{i+1}'] = str(patch_path)
            
            # Save metadata
            metadata_path = output_path / "metadata.json"
            import json
            with open(metadata_path, 'w') as f:
                json.dump(processed_data['metadata'], f, indent=2)
            saved_files['metadata'] = str(metadata_path)
            
            logger.info(f"Processed data saved to {output_dir}")
            
        except Exception as e:
            logger.error(f"Error saving processed data: {e}")
            saved_files['error'] = str(e)
        
        return saved_files

# Example usage and testing
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize agent
    agent = ImagePreprocessingAgent()
    
    # Test with sample image (replace with actual image path)
    # result = agent.preprocess_image("sample_answer_sheet.jpg")
    # print(f"Processing result: {result['metadata']}")
