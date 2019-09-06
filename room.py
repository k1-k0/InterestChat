import uuid

class Room:
    def __init__(self):
        self.id = uuid.uuid4()
        self.users = []