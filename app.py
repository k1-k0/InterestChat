from flask import Flask, request, render_template, redirect, url_for, g

from flask_socketio import SocketIO

from user import User
from room import Room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'like_secret!'
socketio = SocketIO(app)


person = None
rooms = [
    Room('love'),
    Room('death'),
    Room('robots')
]

@app.route('/')
def default():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global person # Don't like that!
        person = User(request.form['username'])
        print("User {} has been logged".format(person.username))
        return redirect(url_for('lobby'))
    else:
        return render_template('login.html')


@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    g.rooms = rooms

    if request.method == 'POST':
        if request.form['join_room']:
            room_name = request.form['join_room']
            return redirect(url_for('room', room_name=room_name))
        elif request.form['create_room']:
            pass
    else:
        return render_template('lobby.html', username=person.username)


@app.route('/room/<room_name>', methods=['GET'])
def room(room_name):
    room = None
    for _ in rooms:
        if room_name == _.name:
            room = _
            g.rooms_messages = room.messages
            break
    else:
        return redirect(url_for('lobby'))

    if request.method == 'GET':
        rooms_name = [room.name for room in rooms]
        if room_name in rooms_name:
            print('User {} has been joined to "{}" room'.format(person.username, room.name))
            
            #TODO: Need send message about user joined to room
            
            return render_template('room.html', room_name=room_name)
        else:
            return redirect(url_for('lobby'))
    # else:
    #     text_message = request.form['message']
    #     if text_message:
    #         print('User {username} in the "{room}" room say: "{message}"'.format(room=room_name,
    #                                                                              username=person.username,
    #                                                                              message=text_message))
    #         room.messages.append(text_message)
    #         # return render_template("room.html", room_name=room.name)
    #         return None
    #     else:
    #         print("STUB")


@socketio.on('chat_message')
def processing_message(message):
    print('Receive and broadcast message: ', message)
    socketio.emit('chat_message', message)


if __name__ == "__main__":
    socketio.run(app, debug=True)