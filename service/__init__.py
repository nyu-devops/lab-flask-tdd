# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Dependencies require we import the routes AFTER the Flask app is created
# pylint: disable=wrong-import-position, wrong-import-order, cyclic-import
from service import routes, models        # noqa: F401, E402
from service.common import error_handlers, cli_commands  # noqa: F401, E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  P E T   S T O R E   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our sqlalchemy tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
