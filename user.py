import uuid

class User:
    def __init__(self, username):
        self.id = uuid.uuid4()
        self.username = username
        self.room = None

    def connect(self, room_id):
        self.room = room_id

    def disconnect(self):
        self.room = None
