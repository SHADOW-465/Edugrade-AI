"""
Database connection setup for the EduGrade AI application.

This file creates the SQLAlchemy engine, session maker, and declarative base
that are used to interact with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import get_settings

# Get application settings
settings = get_settings()

# Create the SQLAlchemy engine for connecting to the database
engine = create_engine(settings.DATABASE_URL)

# Create a session maker for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base for defining database models
Base = declarative_base()
