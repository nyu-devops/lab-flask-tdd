# Test cases can be run with:
# nosetests
# coverage report -m

""" Test cases for Pet Model """

import unittest
from models import Pet, DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPets(unittest.TestCase):
    """ Test Cases for Pets """

    def setUp(self):
        Pet.remove_all()

    def test_create_a_pet(self):
        """ Create a pet and assert that it exists """
        pet = Pet(0, "fido", "dog")
        self.assertTrue(pet != None)
        self.assertEqual(pet.id, 0)
        self.assertEqual(pet.name, "fido")
        self.assertEqual(pet.category, "dog")

    def test_add_a_pet(self):
        """ Create a pet and add it to the database """
        pets = Pet.all()
        self.assertEqual(pets, [])
        pet = Pet(0, "fido", "dog")
        self.assertTrue(pet != None)
        self.assertEqual(pet.id, 0)
        pet.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(pet.id, 1)
        pets = Pet.all()
        self.assertEqual(len(pets), 1)

    def test_update_a_pet(self):
        """ Update a Pet """
        pet = Pet(0, "fido", "dog")
        pet.save()
        self.assertEqual(pet.id, 1)
        # Change it an save it
        pet.category = "k9"
        pet.save()
        self.assertEqual(pet.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        pets = Pet.all()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].category, "k9")

    def test_delete_a_pet(self):
        """ Delete a Pet """
        pet = Pet(0, "fido", "dog")
        pet.save()
        self.assertEqual(len(Pet.all()), 1)
        # delete the pet and make sure it isn't in the database
        pet.delete()
        self.assertEqual(len(Pet.all()), 0)

    def test_serialize_a_pet(self):
        """ Test serialization of a Pet """
        pet = Pet(0, "fido", "dog")
        data = pet.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], 0)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "fido")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "dog")

    def test_deserialize_a_pet(self):
        """ Test deserialization of a Pet """
        data = {"id": 1, "name": "kitty", "category": "cat"}
        pet = Pet()
        pet.deserialize(data)
        self.assertNotEqual(pet, None)
        self.assertEqual(pet.id, 1)
        self.assertEqual(pet.name, "kitty")
        self.assertEqual(pet.category, "cat")

    def test_deserialize_with_no_name(self):
        """ Deserialize a Pet without a name """
        pet = Pet()
        data = {"id":0, "category": "cat"}
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_deserialize_with_no_data(self):
        """ Deserialize a Pet with no data """
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, None)

    def test_deserialize_with_bad_data(self):
        """ Deserailize a Pet with bad data """
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, "data")

    def test_find_pet(self):
        """ Find a Pet by ID """
        Pet(0, "fido", "dog").save()
        Pet(0, "kitty", "cat").save()
        pet = Pet.find(2)
        self.assertIsNot(pet, None)
        self.assertEqual(pet.id, 2)
        self.assertEqual(pet.name, "kitty")

    def test_find_with_no_pets(self):
        """ Find a Pet with no Pets """
        pet = Pet.find(1)
        self.assertIs(pet, None)

    def test_pet_not_found(self):
        """ Test for a Pet that doesn't exist """
        Pet(0, "fido", "dog").save()
        pet = Pet.find(2)
        self.assertIs(pet, None)

    def test_find_by_category(self):
        """ Find Pets by Category """
        Pet(0, "fido", "dog").save()
        Pet(0, "kitty", "cat").save()
        pets = Pet.find_by_category("cat")
        self.assertNotEqual(len(pets), 0)
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")

    def test_find_by_name(self):
        """ Find a Pet by Name """
        Pet(0, "fido", "dog").save()
        Pet(0, "kitty", "cat").save()
        pets = Pet.find_by_name("kitty")
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestPets)
    # unittest.TextTestRunner(verbosity=2).run(suite)
