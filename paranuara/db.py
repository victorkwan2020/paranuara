from flask_mongoengine import MongoEngine

db = MongoEngine()
FOOD_COLLECTION = 'food'
PEOPLE_COLLECTION = 'people'
COMPANY_COLLECTION = 'company'


def initialize_db(app):
    db.init_app(app)
