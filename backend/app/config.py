"""
Configuration management for the EduGrade AI application.

This file defines a Pydantic Settings class to manage environment-based
configuration. It loads settings from a .env file and provides them
to the rest of the application.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings.

    All settings are loaded from environment variables or a .env file.
    """
    # Supabase/PostgreSQL settings
    DATABASE_URL: str

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

    # CORS settings for the FastAPI backend
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8501"

    class Config:
        """
        Pydantic settings configuration.
        """
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    This function is cached to ensure that the settings are only loaded once.

    Returns:
        Settings: The application settings.
    """
    return Settings()
