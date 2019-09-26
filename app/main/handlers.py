from flask_socketio import SocketIO
from flask import session

from .entities.user import User
from .entities.room import Room

from .views import app
from .views import rooms

from .constants import session_entity

socketio = SocketIO(app)


@socketio.on('chat_message')
def processing_message(message):
    person = User.fromJSON(session.get(session_entity.USER))

    print('Receive and broadcast message: ', message)
    message = '{0}: {1}'.format(person.username, message)
    socketio.emit('chat_message', message)


@socketio.on('create_room')
def room_creation(room_name):
    rooms.append(Room(room_name))
    print('{} room was created'.format(room_name))
    socketio.emit('get_rooms', [room.name for room in rooms])
