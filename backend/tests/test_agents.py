import pytest
from backend.app.agents.preprocessing_agent import PreprocessingAgent
import numpy as np
import cv2
import os

@pytest.fixture
def preprocessing_agent():
    return PreprocessingAgent()

@pytest.fixture
def sample_image():
    # Create a dummy image for testing
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.putText(image, "Test", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Save the image to a temporary file
    test_image_path = "test_image.png"
    cv2.imwrite(test_image_path, image)

    yield test_image_path

    # Clean up the temporary file
    os.remove(test_image_path)

def test_preprocessing_agent(preprocessing_agent, sample_image):
    result = preprocessing_agent.process(sample_image, sample_image)
    assert result["status"] == "success"
    assert result["preprocessed_image"] is not None
    assert isinstance(result["preprocessed_image"], np.ndarray)

def test_align_image(preprocessing_agent, sample_image):
    image = cv2.imread(sample_image)
    result = preprocessing_agent.align_image(image, image)
    assert "aligned_image" in result
    assert "transformation_parameters" in result
    assert "alignment_accuracy" in result
