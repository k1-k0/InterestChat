import uuid
import json


class User:
    def __init__(self, user_id, username, interests=None):
        self.id = user_id
        self.username = username
        self.interests = interests or list()

    def toJSON(self):
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'interests': self.interests
        })

    @staticmethod
    def fromJSON(user_json):
        user = json.loads(user_json)
        return User(
            user['id'],
            user['username'],
            user['interests']
        )
