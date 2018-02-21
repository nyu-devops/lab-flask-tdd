# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for Pet Demo Service

All of the models are stored in this module

Models
------
Pet - A Pet used in the Pet Store

Attributes:
-----------
name (string) - the name of the pet
category (string) - the category the pet belongs to (i.e., dog, cat)
available (boolean) - True for pets that are available for adoption

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Pet(db.Model):
    """
    Class that represents a Pet

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    category = db.Column(db.String(63))
    available = db.Column(db.Boolean())

    def __repr__(self):
        return '<Pet %r>' % (self.name)

    def save(self):
        """
        Saves a Pet to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Pet from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Pet into a dictionary """
        return {"id": self.id,
                "name": self.name,
                "category": self.category,
                "available": self.available}

    def deserialize(self, data):
        """
        Deserializes a Pet from a dictionary

        Args:
            data (dict): A dictionary containing the Pet data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid pet: body of request contained bad or no data')
        try:
            self.name = data['name']
            self.category = data['category']
            self.available = data['available']
        except KeyError as error:
            raise DataValidationError('Invalid pet: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid pet: body of request contained' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Pet.logger.info('Initializing database')
        Pet.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """ Returns all of the Pets in the database """
        Pet.logger.info('Processing all Pets')
        return Pet.query.all()

    @staticmethod
    def find(pet_id):
        """ Finds a Pet by it's ID """
        Pet.logger.info('Processing lookup for id %s ...', pet_id)
        return Pet.query.get(pet_id)

    @staticmethod
    def find_or_404(pet_id):
        """ Find a Pet by it's id """
        Pet.logger.info('Processing lookup or 404 for id %s ...', pet_id)
        return Pet.query.get_or_404(pet_id)

    @staticmethod
    def find_by_name(name):
        """ Returns all Pets with the given name

        Args:
            name (string): the name of the Pets you want to match
        """
        Pet.logger.info('Processing name query for %s ...', name)
        return Pet.query.filter(Pet.name == name)

    @staticmethod
    def find_by_category(category):
        """ Returns all of the Pets in a category

        Args:
            category (string): the category of the Pets you want to match
        """
        Pet.logger.info('Processing category query for %s ...', category)
        return Pet.query.filter(Pet.category == category)

    @staticmethod
    def find_by_availability(available=True):
        """ Query that finds Pets by their availability """
        """ Returns all Pets by their availability

        Args:
            available (boolean): True for pets that are available
        """
        Pet.logger.info('Processing available query for %s ...', available)
        return Pet.query.filter(Pet.available == available)
