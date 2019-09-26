import uuid
import json


class User:
    def __init__(self, username, room=None, id=uuid.uuid4().hex):
        self.username = username
        self.room = room
        self.id = id

    def connect(self, room_id):
        self.room = room_id

    def disconnect(self):
        self.room = None

    def toJSON(self):
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'room': self.room
        })

    @staticmethod
    def fromJSON(user_json):
        user = json.loads(user_json)
        return User(user['username'],
                    user['room'],
                    user['id'])
