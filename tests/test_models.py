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
Test cases for Pet Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_pets.py:TestPetModel

"""
import os
import logging
import unittest
from datetime import date
from werkzeug.exceptions import NotFound
from service.models import Pet, Gender, DataValidationError, db
from service import app
from .factories import PetFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P E T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestPetModel(unittest.TestCase):
    """Test Cases for Pet Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Pet.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Pet).delete() # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_pet(self):
        """Create a pet and assert that it exists"""
        pet = Pet(name="Fido", category="dog", available=True, gender=Gender.MALE)
        self.assertEqual(str(pet), "<Pet 'Fido' id=[None]>")
        self.assertTrue(pet is not None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, "Fido")
        self.assertEqual(pet.category, "dog")
        self.assertEqual(pet.available, True)
        self.assertEqual(pet.gender, Gender.MALE)
        pet = Pet(name="Fido", category="dog", available=False, gender=Gender.FEMALE)
        self.assertEqual(pet.available, False)
        self.assertEqual(pet.gender, Gender.FEMALE)

    def test_add_a_pet(self):
        """Create a pet and add it to the database"""
        pets = Pet.all()
        self.assertEqual(pets, [])
        pet = Pet(name="Fido", category="dog", available=True, gender=Gender.MALE)
        self.assertTrue(pet is not None)
        self.assertEqual(pet.id, None)
        pet.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(pet.id)
        pets = Pet.all()
        self.assertEqual(len(pets), 1)

    def test_read_a_pet(self):
        """Read a Pet"""
        pet = PetFactory()
        logging.debug(pet)
        pet.id = None
        pet.create()
        self.assertIsNotNone(pet.id)
        # Fetch it back 
        found_pet = Pet.find(pet.id)
        self.assertEqual(found_pet.id, pet.id)
        self.assertEqual(found_pet.name, pet.name)
        self.assertEqual(found_pet.category, pet.category)

    def test_update_a_pet(self):
        """Update a Pet"""
        pet = PetFactory()
        logging.debug(pet)
        pet.id = None
        pet.create()
        logging.debug(pet)
        self.assertIsNotNone(pet.id)
        # Change it an save it
        pet.category = "k9"
        original_id = pet.id
        pet.update()
        self.assertEqual(pet.id, original_id)
        self.assertEqual(pet.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        pets = Pet.all()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].id, original_id)
        self.assertEqual(pets[0].category, "k9")

    def test_update_no_id(self):
        """Update a Pet with no id"""
        pet = PetFactory()
        logging.debug(pet)
        pet.id = None
        self.assertRaises(DataValidationError, pet.update)

    def test_delete_a_pet(self):
        """Delete a Pet"""
        pet = PetFactory()
        pet.create()
        self.assertEqual(len(Pet.all()), 1)
        # delete the pet and make sure it isn't in the database
        pet.delete()
        self.assertEqual(len(Pet.all()), 0)

    def test_list_all_pets(self):
        """List Pets in the database"""
        pets = Pet.all()
        self.assertEqual(pets, [])
        # Create 5 Pets
        for i in range(5):
            pet = PetFactory()
            pet.create()
        # See if we get back 5 pets
        pets = Pet.all()
        self.assertEqual(len(pets), 5)

    def test_serialize_a_pet(self):
        """Test serialization of a Pet"""
        pet = PetFactory()
        data = pet.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], pet.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], pet.name)
        self.assertIn("category", data)
        self.assertEqual(data["category"], pet.category)
        self.assertIn("available", data)
        self.assertEqual(data["available"], pet.available)
        self.assertIn("gender", data)
        self.assertEqual(data["gender"], pet.gender.name)
        self.assertIn("birthday", data)
        self.assertEqual(date.fromisoformat(data["birthday"]), pet.birthday)

    def test_deserialize_a_pet(self):
        """Test de-serialization of a Pet"""
        data = PetFactory().serialize()
        pet = Pet()
        pet.deserialize(data)
        self.assertNotEqual(pet, None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, data["name"])
        self.assertEqual(pet.category, data["category"])
        self.assertEqual(pet.available, data["available"])
        self.assertEqual(pet.gender.name, data["gender"])
        self.assertEqual(pet.birthday, date.fromisoformat(data["birthday"]))

    def test_deserialize_missing_data(self):
        """Test de-serialization of a Pet with missing data"""
        data = {"id": 1, "name": "Kitty", "category": "cat"}
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test de-serialization of bad data"""
        data = "this is not a dictionary"
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_deserialize_bad_available(self):
        """Test de-serialization of bad available attribute"""
        test_pet = PetFactory()
        data = test_pet.serialize()
        data["available"] = "true"
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_deserialize_bad_gender(self):
        """Test de-serialization of bad gender attribute"""
        test_pet = PetFactory()
        data = test_pet.serialize()
        data["gender"] = "male"  # wrong case
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_find_pet(self):
        """Find a Pet by ID"""
        pets = PetFactory.create_batch(3)
        for pet in pets:
            pet.create()
        logging.debug(pets)
        # make sure they got saved
        self.assertEqual(len(Pet.all()), 3)
        # find the 2nd pet in the list
        pet = Pet.find(pets[1].id)
        self.assertIsNot(pet, None)
        self.assertEqual(pet.id, pets[1].id)
        self.assertEqual(pet.name, pets[1].name)
        self.assertEqual(pet.available, pets[1].available)

    def test_find_by_category(self):
        """Find Pets by Category"""
        Pet(name="Fido", category="dog", available=True).create()
        Pet(name="Kitty", category="cat", available=False).create()
        pets = Pet.find_by_category("cat")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "Kitty")
        self.assertEqual(pets[0].available, False)

    def test_find_by_name(self):
        """Find a Pet by Name"""
        Pet(name="Fido", category="dog", available=True).create()
        Pet(name="Kitty", category="cat", available=False).create()
        pets = Pet.find_by_name("Kitty")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "Kitty")
        self.assertEqual(pets[0].available, False)

    def test_find_by_availability(self):
        """Find Pets by Availability"""
        Pet(name="Fido", category="dog", available=True).create()
        Pet(name="Kitty", category="cat", available=False).create()
        Pet(name="Fifi", category="dog", available=True).create()
        pets = Pet.find_by_availability(False)
        pet_list = list(pets)
        self.assertEqual(len(pet_list), 1)
        self.assertEqual(pets[0].name, "Kitty")
        self.assertEqual(pets[0].category, "cat")
        pets = Pet.find_by_availability(True)
        pet_list = list(pets)
        self.assertEqual(len(pet_list), 2)

    def test_find_by_gender(self):
        """Find Pets by Gender"""
        Pet(name="Fido", category="dog", available=True, gender=Gender.MALE).create()
        Pet(
            name="Kitty", category="cat", available=False, gender=Gender.FEMALE
        ).create()
        Pet(name="Fifi", category="dog", available=True, gender=Gender.MALE).create()
        pets = Pet.find_by_gender(Gender.FEMALE)
        pet_list = list(pets)
        self.assertEqual(len(pet_list), 1)
        self.assertEqual(pets[0].name, "Kitty")
        self.assertEqual(pets[0].category, "cat")
        pets = Pet.find_by_gender(Gender.MALE)
        pet_list = list(pets)
        self.assertEqual(len(pet_list), 2)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        pets = PetFactory.create_batch(3)
        for pet in pets:
            pet.create()

        pet = Pet.find_or_404(pets[1].id)
        self.assertIsNot(pet, None)
        self.assertEqual(pet.id, pets[1].id)
        self.assertEqual(pet.name, pets[1].name)
        self.assertEqual(pet.available, pets[1].available)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Pet.find_or_404, 0)
