"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from app.models import Pet

class PetFactory(factory.Factory):
    """ Creates fake pets that you don't have to feed """
    class Meta:
        model = Pet
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('first_name')
    category = FuzzyChoice(choices=['dog', 'cat', 'bird', 'fish'])
    available = FuzzyChoice(choices=[True, False])

if __name__ == '__main__':
    for _ in range(10):
        pet = PetFactory()
        print(pet.serialize())
