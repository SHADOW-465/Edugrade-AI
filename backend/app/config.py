"""
Configuration management for the EduGrade AI application (Firebase version).
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings for Firebase-based EduGrade AI.
    """
    # Firebase
    FIREBASE_CREDENTIALS: str = "app/firebase_service_key.json"

    # API keys for external services
    OPENAI_API_KEY: str
    PERPLEXITY_API_KEY: str

    # File storage paths
    UPLOADS_DIR: str = "data/uploads"
    PROCESSED_DIR: str = "data/processed"
    MODELS_DIR: str = "data/models"

    # Model configurations
    YOLO_MODEL: str = "yolov8n.pt"
    TESSERACT_PATH: str = "/usr/bin/tesseract"

    # CORS settings for frontend
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8501"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """Load and cache settings."""
    return Settings()
