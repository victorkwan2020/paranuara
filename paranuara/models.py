from .db import db, FOOD_COLLECTION, PEOPLE_COLLECTION, COMPANY_COLLECTION


class Company(db.Document):
    meta = {'collection': COMPANY_COLLECTION}
    index = db.IntField(required=True)
    company = db.StringField()


class Food(db.Document):
    meta = {'collection': FOOD_COLLECTION}
    name = db.StringField(required=True)
    category = db.StringField(required=True)


class Friend(db.EmbeddedDocument):
    index = db.IntField(required=True)


class People(db.Document):
    meta = {'collection': PEOPLE_COLLECTION}
    _id = db.ObjectIdField(required=True)
    index = db.IntField(required=True)
    has_died = db.BooleanField(required=True)
    eyeColor = db.StringField(required=True)
    name = db.StringField(required=True)
    age = db.IntField(required=True)
    address = db.StringField(required=True)
    phone = db.StringField(required=True)
    friends = db.EmbeddedDocumentListField(Friend)
    favouriteFood = db.ListField(db.StringField())
    company_id = db.IntField(required=True)
    gender = db.StringField(required=True)
    tags = db.ListField(db.StringField())
    registered = db.StringField()
    greeting = db.StringField()
    email = db.EmailField()
    about = db.StringField()
    guid = db.StringField()
    balance = db.StringField()
    picture = db.URLField()

    def friend_list(self):
        return [x['index'] for x in self.friends]

    def common_friends(self, other_person):
        common = []
        for index in self.friend_list():
            if index == self.index or index == other_person.index:
                # handling self reference in freinds list
                continue
            elif index in other_person.friend_list():
                common.append(index)
        return common

    def short_dict(self):
        return {'name': self.name, 'age': self.age,  'address': self.address,
                'phone': self.phone}
