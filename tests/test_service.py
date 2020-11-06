# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
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
Pet API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status  # HTTP Status Codes
# from unittest.mock import MagicMock, patch
from service.models import Pet, DataValidationError, db
from .pet_factory import PetFactory
from service import app
from service.routes import init_db

# Disable all but ciritcal erros suirng unittest
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv("DATABASE_URI", "postgres://postgres:postgres@localhost:5432/testdb")

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPetService(unittest.TestCase):
    """ Pet Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        app.testing = True
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ Run once after all tests """
        db.dispose()

    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_pets(self, count):
        """ Factory method to create pets in bulk """
        pets = []
        for _ in range(count):
            test_pet = PetFactory()
            resp = self.app.post(
                "/pets", json=test_pet.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test pet"
            )
            new_pet = resp.get_json()
            test_pet.id = new_pet["id"]
            pets.append(test_pet)
        return pets

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Pet Demo REST API Service")

    def test_get_pet_list(self):
        """ Get a list of Pets """
        self._create_pets(5)
        resp = self.app.get("/pets")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_pet(self):
        """ Get a single Pet """
        # get the id of a pet
        test_pet = self._create_pets(1)[0]
        resp = self.app.get(
            "/pets/{}".format(test_pet.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], test_pet.name)

    def test_get_pet_not_found(self):
        """ Get a Pet thats not found """
        resp = self.app.get("/pets/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_pet(self):
        """ Create a new Pet """
        test_pet = PetFactory()
        resp = self.app.post(
            "/pets", json=test_pet.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_pet = resp.get_json()
        self.assertEqual(new_pet["name"], test_pet.name, "Names do not match")
        self.assertEqual(
            new_pet["category"], test_pet.category, "Categories do not match"
        )
        self.assertEqual(
            new_pet["available"], test_pet.available, "Availability does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_pet = resp.get_json()
        self.assertEqual(new_pet["name"], test_pet.name, "Names do not match")
        self.assertEqual(
            new_pet["category"], test_pet.category, "Categories do not match"
        )
        self.assertEqual(
            new_pet["available"], test_pet.available, "Availability does not match"
        )

    def test_update_pet(self):
        """ Update an existing Pet """
        # create a pet to update
        test_pet = PetFactory()
        resp = self.app.post(
            "/pets", json=test_pet.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_pet = resp.get_json()
        new_pet["category"] = "unknown"
        resp = self.app.put(
            "/pets/{}".format(new_pet["id"]),
            json=new_pet,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_pet = resp.get_json()
        self.assertEqual(updated_pet["category"], "unknown")

    def test_delete_pet(self):
        """ Delete a Pet """
        test_pet = self._create_pets(1)[0]
        resp = self.app.delete(
            "/pets/{}".format(test_pet.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/pets/{}".format(test_pet.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_pet_list_by_category(self):
        """ Query Pets by Category """
        pets = self._create_pets(10)
        test_category = pets[0].category
        category_pets = [pet for pet in pets if pet.category == test_category]
        resp = self.app.get("/pets", query_string="category={}".format(test_category))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_pets))
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["category"], test_category)

    # @patch('service.routes.Pet.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    
    # @patch('service.routes.Pet.find_by_name')
    # def test_mock_search_data(self, pet_find_mock):
    #     """ Test showing how to mock data """
    #     pet_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/pets', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
