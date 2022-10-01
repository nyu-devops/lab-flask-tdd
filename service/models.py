# Copyright 2016, 2021 John Rofrano. All Rights Reserved.
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
from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


def init_db(app):
    """Initialize the SQLAlchemy app"""
    Pet.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Gender(Enum):
    """Enumeration of valid Pet Genders"""

    MALE = 0
    FEMALE = 1
    UNKNOWN = 3


class Pet(db.Model):
    """
    Class that represents a Pet

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)
    gender = db.Column(
        db.Enum(Gender), nullable=False, server_default=(Gender.UNKNOWN.name)
    )
    birthday = db.Column(db.Date(), nullable=False, default=date.today())

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return f"<Pet {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Pet to the database
        """
        logger.info("Creating %s", self.name)
        # id must be none to generate next primary key
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Pet to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Pet from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self) -> dict:
        """Serializes a Pet into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "available": self.available,
            "gender": self.gender.name,  # convert enum to string
            "birthday": self.birthday.isoformat()
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Pet from a dictionary
        Args:
            data (dict): A dictionary containing the Pet data
        """
        try:
            self.name = data["name"]
            self.category = data["category"]
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
            self.gender = getattr(Gender, data["gender"])  # create enum from string
            self.birthday = date.fromisoformat(data["birthday"])
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError("Invalid pet: missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid pet: body of request contained bad or no data " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Pets in the database"""
        logger.info("Processing all Pets")
        return cls.query.all()

    @classmethod
    def find(cls, pet_id: int):
        """Finds a Pet by it's ID

        :param pet_id: the id of the Pet to find
        :type pet_id: int

        :return: an instance with the pet_id, or None if not found
        :rtype: Pet

        """
        logger.info("Processing lookup for id %s ...", pet_id)
        return cls.query.get(pet_id)

    @classmethod
    def find_or_404(cls, pet_id: int):
        """Find a Pet by it's id

        :param pet_id: the id of the Pet to find
        :type pet_id: int

        :return: an instance with the pet_id, or 404_NOT_FOUND if not found
        :rtype: Pet

        """
        logger.info("Processing lookup or 404 for id %s ...", pet_id)
        return cls.query.get_or_404(pet_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Pets with the given name

        :param name: the name of the Pets you want to match
        :type name: str

        :return: a collection of Pets with that name
        :rtype: list

        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Pets in a category

        :param category: the category of the Pets you want to match
        :type category: str

        :return: a collection of Pets in that category
        :rtype: list

        """
        logger.info("Processing category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Returns all Pets by their availability

        :param available: True for pets that are available
        :type available: str

        :return: a collection of Pets that are available
        :rtype: list

        """
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)

    @classmethod
    def find_by_gender(cls, gender: Gender = Gender.UNKNOWN) -> list:
        """Returns all Pets by their Gender

        :param gender: values are ['MALE', 'FEMALE', 'UNKNOWN']
        :type available: enum

        :return: a collection of Pets that are available
        :rtype: list

        """
        logger.info("Processing gender query for %s ...", gender.name)
        return cls.query.filter(cls.gender == gender)
