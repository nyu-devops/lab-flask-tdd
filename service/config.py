"""
Global Configuration for Application
"""
import os
import logging

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
)

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_POOL_SIZE = 2

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")
LOGGING_LEVEL = logging.INFO
