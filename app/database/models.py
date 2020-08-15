import mongoengine as me
from .db import db


class Interest(me.Document):
    name = me.StringField(required=True)


class User(me.Document):
    username = me.StringField(required=True)
    password = me.StringField(required=True)
    interests = me.ListField(Interest)


class Room(me.Document):
    name = me.StringField(required=True)
    users = me.ListField(User)
    interests = me.ListField(Interest)
    messages = me.ListField(me.StringField())
