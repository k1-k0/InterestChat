from flask import Flask, request, render_template, redirect, url_for, g
from user import User
from room import Room

app = Flask(__name__)
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
        room_name = request.form['room']
        return redirect(url_for('room', room_name=room_name))
    else:
        return render_template('lobby.html', username=person.username)


@app.route('/room/<room_name>', methods=['GET', 'POST'])
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
            return render_template('room.html', room_name=room_name)
        else:
            return redirect(url_for('lobby'))
    else:
        if request.form['message']:
            room.messages.append(request.form['message'])
            return render_template("room.html", room_name=room.name)
        else:
            print("STUB")