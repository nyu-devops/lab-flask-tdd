# Copyright 2016 John Rofrano. All Rights Reserved.
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
""" Models for Pet Demo Service """

import threading

class Pet(object):
    """
    Class that represents a Pet

    This version uses an in-memory collection of pets for testing
    """
    __lock = threading.Lock()
    __data = []
    __index = 0

    def __init__(self, pet_id=0, name='', category=''):
        """ Initialize a Pet """
        self.id = pet_id
        self.name = name
        self.category = category

    def save(self):
        """
        Saves a Pet to the data store
        """
        if self.id == 0:
            self.id = self.__next_index()
            Pet.__data.append(self)
        else:
            for i in range(len(Pet.__data)):
                if Pet.__data[i].id == self.id:
                    Pet.__data[i] = self
                    break

    def delete(self):
        """ Removes a Pet from the data store """
        Pet.__data.remove(self)

    def serialize(self):
        """ Serializes a Pet into a dictionary """
        return {"id": self.id, "name": self.name, "category": self.category}

    def deserialize(self, data):
        """
        Deserializes a Pet from a dictionary

        Args:
            data (dict): A dictionary containing the Pet data
        """
        if not isinstance(data, dict):
            raise ValueError('Invalid pet: body of request contained bad or no data')
        if data.has_key('id'):
            self.id = data['id']
        try:
            self.name = data['name']
            self.category = data['category']
        except KeyError as err:
            raise ValueError('Invalid pet: missing ' + err.args[0])
        return

    @staticmethod
    def __next_index():
        """ Generates the next index in a continual sequence """
        with Pet.__lock:
            Pet.__index += 1
        return Pet.__index

    @staticmethod
    def all():
        """ Returns all of the Pets in the database """
        return [pet for pet in Pet.__data]

    @staticmethod
    def remove_all():
        """ Removes all of the Pets from the database """
        del Pet.__data[:]
        Pet.__index = 0
        return Pet.__data

    @staticmethod
    def find(pet_id):
        """ Finds a Pet by it's ID """
        if not Pet.__data:
            return None
        pets = [pet for pet in Pet.__data if pet.id == pet_id]
        if pets:
            return pets[0]
        return None

    @staticmethod
    def find_by_category(category):
        """ Returns all of the Pets in a category

        Args:
            category (string): the category of the Pets you want to match
        """
        return [pet for pet in Pet.__data if pet.category == category]

    @staticmethod
    def find_by_name(name):
        """ Returns all Pets with the given name

        Args:
            name (string): the name of the Pets you want to match
        """
        return [pet for pet in Pet.__data if pet.name == name]
