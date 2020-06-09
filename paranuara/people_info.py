from .models import People, Food, Company
from functools import lru_cache
import logging


def get_employees_from_company(index):
    if Company.objects(index=index).first() is None:
        raise ValueError(f"Company with index {index} don't exisit")
    return People.objects(company_id=index).only('index',
                                                 'name').exclude('_id')


def common_friends_alive_brown_eyes(index1, index2):
    person1 = People.objects(index=index1).first()
    if person1 is None:
        raise ValueError(f"person with index {index1} don't exist")

    person2 = People.objects(index=index2).first()
    if person2 is None:
        raise ValueError(f"person with index {index2} don't exist")

    common = person1.common_friends(person2)
    alive_brown_eye_friends = \
        People.objects(index__in=common, eyeColor='brown',
                       has_died=False).only('name', 'age', 'address',
                                            'phone').exclude('_id')
    return {'person1': person1.short_dict(), 'person2': person2.short_dict(),
            'common_friends': alive_brown_eye_friends}


@lru_cache
def _fruits():
    return [x['name'] for x in Food.objects(category='fruit')]


@lru_cache
def _vegetables():
    return [x['name'] for x in Food.objects(category='vegetable')]


def get_favourite_food(index):
    person = People.objects(index=index).first()
    if person is None:
        raise ValueError(f"person with index {index} don't exist")
    fruits, vegs = [], []
    for item in person.favouriteFood:
        if item in _fruits():
            fruits.append(item)
        elif item in _vegetables():
            vegs.append(item)
        else:
            logging.error(f"Unclassified food {item} from person: {index}")

    return {'username': person.name, 'age': person.age, 'fruits': fruits,
            'vegetables': vegs}
