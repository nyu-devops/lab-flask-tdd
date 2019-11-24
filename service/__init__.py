"""
Package: app

Package for the application models and services
This module also sets up the logging to be used with gunicorn
"""
import logging
from flask import Flask

# Create Flask application
app = Flask(__name__)
# We'll just use SQLite here so we don't need an external database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/development.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "sup3r-s3cr3t"  # change for production
app.config["LOGGING_LEVEL"] = logging.INFO

# Import the routes After the Flask app is created
from service import service, models

# Set up logging for production
print("Setting up logging for {}...".format(__name__))
app.logger.propagate = False
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("Logging established")

app.logger.info(70 * "*")
app.logger.info("  P E T   S T O R E   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")

# make our sqlalchemy tables
service.init_db()

app.logger.info("Service inititalized!")
