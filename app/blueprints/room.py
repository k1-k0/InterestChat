from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.local import LocalProxy
from werkzeug.security import check_password_hash, generate_password_hash
from ..database.models import Room, User


bp = Blueprint('room', __name__, url_prefix='/room')

@bp.before_app_request
def load_rooms():
    # NOTE: Is it good approach to touch database on every request?
    g.rooms = [room.name for room in Room.objects()]


@bp.route('/', methods=['POST'])
def index():
    room_name = request.form['room_name']

    if g.user_id is None:
        flash('Not authorized user!')
        return redirect(url_for('auth.login'))

    room = Room.objects(name=room_name).first()
    if room is None:
        user = User.objects(id=g.user_id).first()
        new_room = Room(name=room_name, users=[user])
        new_room.save()

        session['room_id'] = str(new_room.id)
        g.rooms.append(room_name)

        return redirect(f'{room_name}')

    else:
        flash('Room is existed!')
        return redirect(url_for('main.lobby'))


@bp.route('/<room_name>', methods=['GET'])
def room(room_name):
    if g.user_id is None:
        flash('Not authorized user!')
        return redirect(url_for('auth.login'))

    room = Room.objects(name=room_name).first()
    if room is not None:
        user = User.objects(id=g.user_id).first()
        session['room_id'] = str(room.id)
        
        if user not in room.users:
            room.users.append(user)

        room.save()

        return render_template('room.html', room_name=room_name)

    else:
        flash('Room is not created!')
        return redirect(url_for('main.lobby'))

