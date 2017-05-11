from mongoengine import *
from flask_login import UserMixin


class User(Document, UserMixin, object):
    username = StringField(required=True, unique=True)
    email = StringField()

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.username

    def __str__(self):
        return self.username
