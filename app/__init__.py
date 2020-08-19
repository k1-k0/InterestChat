from flask import Flask, g
from flask_socketio import SocketIO

from .database.models import Room


socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'like_secret!'
    app.config['MONGODB_SETTINGS'] = {
        'db': 'interest_chat',
        'host': '127.0.0.1',
        'port': 27017
    }

    from .database import db
    from .blueprints import main
    from .blueprints import auth
    from .blueprints import room

    db.initialize_db(app)
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(room.bp)

    socketio.init_app(app)
    return app
