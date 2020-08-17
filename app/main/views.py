from flask import (
    Flask, request, render_template, redirect, url_for, session, g
)

from . import auth
from . import room

from database import db
from database.models import User

from flask_socketio import SocketIO

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')

app.config['SECRET_KEY'] = 'like_secret!'
app.config['MONGODB_SETTINGS'] = {
    'db': 'interest_chat',
    'host': '127.0.0.1',
    'port': 27017
}


db.initialize_db(app)

app.register_blueprint(auth.bp)
app.register_blueprint(room.bp)

socketio = SocketIO(app)

rooms = []

@app.route('/lobby')
def lobby():
    if not g.user_id:
        return redirect(url_for('auth.login'))

    person = User.objects(id=g.user_id).first()
    print('Total rooms: ', len(rooms))
    return render_template('lobby.html', username=person['username'])