from flask import (
    Flask, blueprints, request, render_template, redirect, url_for, session, g
)

from ..database.models import User
from ..database.models import Room


bp = blueprints.Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def lobby():
    if g.user_id is None:
        return redirect(url_for('auth.login'))

    person = User.objects(id=g.user_id).first()
    return render_template('lobby.html', username=person['username'])