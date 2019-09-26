from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import g

from .entities.user import User
from .entities.room import Room

from .constants.methods import GET
from .constants.methods import POST
from .constants import session_entity
from .constants import urls

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
app.config['SECRET_KEY'] = 'like_secret!'

rooms = []


@app.route('/')
def default():
    return redirect(url_for(urls.LOGIN))


@app.route('/login', methods=[GET, POST])
def login():
    if request.method == POST:
        username = request.form['username']

        if not username:
            # TODO: Need using Flash message( Flask built-in )
            print('Empty username')
            return render_template('login.html')
        else:
            session[session_entity.USER] = User(username).toJSON()

            print("User {} has been logged".format(username))
            return redirect(url_for(urls.LOBBY))
    else:
        return render_template('login.html')


@app.route('/lobby')
def lobby():
    g.rooms = rooms
    person = User.fromJSON(session.get(session_entity.USER))
    print('Total rooms: ', len(rooms))
    return render_template('lobby.html', username=person.username)


@app.route('/room/<room_name>', methods=[GET])
def room(room_name):
    room = None
    # person = User.fromJSON(session.get(session_entity.USER))

    for _ in rooms:
        if room_name == _.name:
            room = _
            g.rooms_messages = room.messages
            break
    else:
        return redirect(url_for(urls.LOBBY))

    if request.method == GET:
        rooms_name = [room.name for room in rooms]
        if room_name in rooms_name:
            # TODO: Need using Flash message( Flask built-in )
            return render_template('room.html', room_name=room_name)
        else:
            return redirect(url_for(urls.LOBBY))
