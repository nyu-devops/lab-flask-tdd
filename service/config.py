"""
Global Configuration for Application
"""
import os
import json
import logging

# Get configuration from environment
DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url']

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_POOL_SIZE = 2

# Secret for session management
SECRET_KEY = os.getenv("SECRET_KEY", "sup3r-s3cr3t")
LOGGING_LEVEL = logging.INFO
