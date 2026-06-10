# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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
Test Factory to make fake objects for testing
"""

from datetime import date

from factory.base import Factory
from factory.declarations import LazyFunction, Sequence
from factory.fuzzy import FuzzyChoice, FuzzyDate
from .pet_name_provider import PetNameFaker
from service.models import Pet, Gender


class PetFactory(Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Pet

    id = Sequence(lambda n: n)
    name = LazyFunction(lambda: PetNameFaker().pet_name())
    category = FuzzyChoice(choices=["dog", "cat", "bird", "fish"])
    available = FuzzyChoice(choices=[True, False])
    gender = FuzzyChoice(choices=[Gender.MALE, Gender.FEMALE, Gender.UNKNOWN])
    birthday = FuzzyDate(date(2008, 1, 1))
