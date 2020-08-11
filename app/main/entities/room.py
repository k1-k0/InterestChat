import json

class Room:
    counter = 0

    def __init__(self,
                 name=f"Room #{Room.counter}",
                 interests=None,
                 users=None,
                 messages=None):
        self.name = name
        self.interests = interests or list()
        self.users = users or list()
        self.messages = messages or list()

    def toJSON(self):
        return json.dumps({
            'name': self.name,
            'interests': self.interests,
            'users': self.users,
            'messages': self.messages,
        })

    @staticmethod
    def fromJSON(room_json):
        room = json.loads(room_json)
        return Room(
            room['name'],
            room['interests'],
            room['users'],
            room['messages']
        )


