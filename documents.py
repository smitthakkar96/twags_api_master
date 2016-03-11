import connect
from mongoengine import *

class globalInterests(DynamicDocument):
    text = StringField(unique=True)

class user(DynamicDocument):
    name = StringField()
    email = StringField(unique=True)
    interests = ListField(StringField())

class tweets(DynamicDocument):
    text = StringField()
    createdAt = DateTimeField()
    by_name = StringField()
    tag = StringField()
    by_profilepicture = StringField()
