import unittest
import json

from paranuara.app import app
from paranuara.db import (initialize_db, db, FOOD_COLLECTION,
                          PEOPLE_COLLECTION, COMPANY_COLLECTION)
from .test_data import people, food, company


TEST_MONGO = 'mongomock://localhost/mongotest'


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        app.config['MONGODB_SETTINGS'] = \
            {'host': TEST_MONGO}
        app.config['TESTING'] = True

        initialize_db(app)
        cls.app = app.test_client()
        cls.db = db.get_db()
        cls.people = cls.db[PEOPLE_COLLECTION]
        cls.people.insert_many(people)
        cls.food = cls.db[FOOD_COLLECTION]
        cls.food.insert_many(food)
        cls.company = cls.db[COMPANY_COLLECTION]
        cls.company.insert_many(company)

    def test_alive(self):
        resp = self.app.get('/alive')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data, b'Alive')

    def test_nonexistent_endpoint(self):
        resp = self.app.get('/test')
        expected = {"code": 404, "name": "Not Found"}
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(json.loads(resp.data), expected)

    def test_company_have_employees(self):
        resp = self.app.get('/company/1/employees')
        expected = [{"index": 1, "name": "Decker Mckenzie"},
                    {"index": 4, "name": "Mindy Beasley"}]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), expected)

    def test_company_dont_exist(self):
        resp = self.app.get('/company/9999/employees')
        expected = {'Internal Error': "Company with index 9999 don't exisit"}
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data), expected)

    def test_favourite_food_with_valid_person(self):
        resp = self.app.get('/people/1/favourite_food')
        expected = {"username": "Decker Mckenzie", "age": 60, "fruits": [],
                    "vegetables": ["cucumber", "beetroot", "carrot", "celery"]}
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), expected)

    def test_favourite_food_with_non_existing_person(self):
        resp = self.app.get('/people/10/favourite_food')
        expected = {'Internal Error': "person with index 10 don't exist"}
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data), expected)

    def test_common_friends_nonexisting_person(self):
        resp = self.app.get('/people/10/common_friends_with/1')
        expected = {'Internal Error': "person with index 10 don't exist"}
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data), expected)

    def test_common_friends_nonexisting_person2(self):
        resp = self.app.get('/people/2/common_friends_with/11')
        expected = {'Internal Error': "person with index 11 don't exist"}
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data), expected)

    def test_common_friends_valid_people(self):
        resp = self.app.get('/people/3/common_friends_with/4')
        expected = {
                    "person1": {
                        "name": "Rosemary Hayes",
                        "age": 30,
                        "address": "130 Bay Parkway, Marshall, Virgin Islands, 298",
                        "phone": "+1 (984) 437-3226"
                    },
                    "person2": {
                        "name": "Mindy Beasley",
                        "age": 62,
                        "address": "628 Brevoort Place, Bellamy, Kansas, 2696",
                        "phone": "+1 (862) 503-2197"
                    },
                    "common_friends": [{"name": "Ted Watson",
                                        "phone": "+1 (862) 603-2197",
                                        "address": "62 Brevoort Place, Bellamy, Kansas, 2696",
                                        "age": 62
                                        }]
        }

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), expected)


if __name__ == '__main__':
    unittest.main()
