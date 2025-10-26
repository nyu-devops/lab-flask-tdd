# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
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
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch, MagicMock

# from unittest.mock import MagicMock, patch
from urllib.parse import quote_plus
from wsgi import app

# from service import create_app
from service.common import status
from service.models import Pet, Gender, db, DataValidationError
from tests.factories import PetFactory

# Disable all but critical errors during normal test run
# uncomment for debugging failing tests
# logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/pets"

# app = create_app()


######################################################################
#  T E S T   P E T   S E R V I C E
######################################################################
class TestPetService(TestCase):
    """Pet Server Tests"""

    # pylint: disable=duplicate-code
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Pet).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        db.session.remove()

    ############################################################
    # Utility function to bulk create pets
    ############################################################
    def _create_pets(self, count: int = 1) -> list:
        """Factory method to create pets in bulk"""
        pets = []
        for _ in range(count):
            test_pet = PetFactory()
            response = self.client.post(BASE_URL, json=test_pet.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test pet",
            )
            new_pet = response.get_json()
            test_pet.id = new_pet["id"]
            pets.append(test_pet)
        return pets

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """It should call the Home Page"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Pet Demo REST API Service")

    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], 200)
        self.assertEqual(data["message"], "Healthy")

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_pet_list(self):
        """It should Get a list of Pets"""
        self._create_pets(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ----------------------------------------------------------
    # TEST READ
    # ----------------------------------------------------------
    def test_get_pet(self):
        """It should Get a single Pet"""
        # get the id of a pet
        test_pet = self._create_pets(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_pet.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_pet.name)

    def test_get_pet_not_found(self):
        """It should not Get a Pet thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    # ----------------------------------------------------------
    # TEST CREATE
    # ----------------------------------------------------------
    def test_create_pet(self):
        """It should Create a new Pet"""
        test_pet = PetFactory()
        logging.debug("Test Pet: %s", test_pet.serialize())
        response = self.client.post(BASE_URL, json=test_pet.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_pet = response.get_json()
        self.assertEqual(new_pet["name"], test_pet.name)
        self.assertEqual(new_pet["category"], test_pet.category)
        self.assertEqual(new_pet["available"], test_pet.available)
        self.assertEqual(new_pet["gender"], test_pet.gender.name)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_pet = response.get_json()
        self.assertEqual(new_pet["name"], test_pet.name)
        self.assertEqual(new_pet["category"], test_pet.category)
        self.assertEqual(new_pet["available"], test_pet.available)
        self.assertEqual(new_pet["gender"], test_pet.gender.name)

    # ----------------------------------------------------------
    # TEST UPDATE
    # ----------------------------------------------------------
    def test_update_pet(self):
        """It should Update an existing Pet"""
        # create a pet to update
        test_pet = PetFactory()
        response = self.client.post(BASE_URL, json=test_pet.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the pet
        new_pet = response.get_json()
        logging.debug(new_pet)
        new_pet["category"] = "unknown"
        response = self.client.put(f"{BASE_URL}/{new_pet['id']}", json=new_pet)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_pet = response.get_json()
        self.assertEqual(updated_pet["category"], "unknown")

    # ----------------------------------------------------------
    # TEST DELETE
    # ----------------------------------------------------------
    def test_delete_pet(self):
        """It should Delete a Pet"""
        test_pet = self._create_pets(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_pet.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_pet.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existing_pet(self):
        """It should Delete a Pet even if it doesn't exist"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_query_by_name(self):
        """It should Query Pets by name"""
        pets = self._create_pets(5)
        test_name = pets[0].name
        name_count = len([pet for pet in pets if pet.name == test_name])
        response = self.client.get(
            BASE_URL, query_string=f"name={quote_plus(test_name)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["name"], test_name)

    def test_query_pet_list_by_category(self):
        """It should Query Pets by Category"""
        pets = self._create_pets(10)
        test_category = pets[0].category
        category_pets = [pet for pet in pets if pet.category == test_category]
        response = self.client.get(
            BASE_URL, query_string=f"category={quote_plus(test_category)}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), len(category_pets))
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["category"], test_category)

    def test_query_by_availability(self):
        """It should Query Pets by availability"""
        pets = self._create_pets(10)
        available_pets = [pet for pet in pets if pet.available is True]
        unavailable_pets = [pet for pet in pets if pet.available is False]
        available_count = len(available_pets)
        unavailable_count = len(unavailable_pets)
        logging.debug("Available Pets [%d] %s", available_count, available_pets)
        logging.debug("Unavailable Pets [%d] %s", unavailable_count, unavailable_pets)

        # test for available
        response = self.client.get(BASE_URL, query_string="available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["available"], True)

        # test for unavailable
        response = self.client.get(BASE_URL, query_string="available=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), unavailable_count)
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["available"], False)

    def test_query_by_gender(self):
        """It should Query Pets by gender"""
        pets = self._create_pets(10)
        female_pets = [pet for pet in pets if pet.gender == Gender.FEMALE]
        female_count = len(female_pets)
        logging.debug("Female Pets [%d] %s", female_count, female_pets)

        # test for available
        response = self.client.get(BASE_URL, query_string="gender=female")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), female_count)
        # check the data just to be sure
        for pet in data:
            self.assertEqual(pet["gender"], Gender.FEMALE.name)

    # ----------------------------------------------------------
    # TEST ACTIONS
    # ----------------------------------------------------------
    def test_purchase_a_pet(self):
        """It should Purchase a Pet"""
        # Create a pet that is available for purchase
        pet = PetFactory()
        pet.available = True
        response = self.client.post(BASE_URL, json=pet.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        pet.id = data["id"]
        self.assertEqual(data["available"], True)

        # Call purchase on the created id and check the results
        response = self.client.put(f"{BASE_URL}/{pet.id}/purchase")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{pet.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["available"], False)

    def test_purchase_not_available(self):
        """It should not Purchase a Pet that is not available"""
        pets = self._create_pets(10)
        unavailable_pets = [pet for pet in pets if pet.available is False]
        pet = unavailable_pets[0]
        response = self.client.put(f"{BASE_URL}/{pet.id}/purchase")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a pet id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_pet_no_data(self):
        """It should not Create a Pet with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pet_no_content_type(self):
        """It should not Create a Pet with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_pet_wrong_content_type(self):
        """It should not Create a Pet with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_pet_bad_available(self):
        """It should not Create a Pet with bad available data"""
        test_pet = PetFactory()
        logging.debug(test_pet)
        # change available to a string
        test_pet.available = "true"
        response = self.client.post(BASE_URL, json=test_pet.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pet_bad_gender(self):
        """It should not Create a Pet with bad gender data"""
        pet = PetFactory()
        logging.debug(pet)
        # change gender to a bad string
        test_pet = pet.serialize()
        test_pet["gender"] = "XXX"  # invalid gender
        response = self.client.post(BASE_URL, json=test_pet)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ######################################################################
    #  T E S T   M O C K S
    ######################################################################

    @patch("service.routes.Pet.find_by_name")
    def test_bad_request(self, bad_request_mock):
        """It should return a Bad Request error from Find By Name"""
        bad_request_mock.side_effect = DataValidationError()
        response = self.client.get(BASE_URL, query_string="name=fido")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("service.routes.Pet.find_by_name")
    def test_mock_search_data(self, pet_find_mock):
        """It should showing how to mock data"""
        pet_find_mock.return_value = [MagicMock(serialize=lambda: {"name": "fido"})]
        response = self.client.get(BASE_URL, query_string="name=fido")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
