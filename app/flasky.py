from main.views import app
from main.handlers import socketio

if __name__ == "__main__":
    socketio.run(app, debug=True)
