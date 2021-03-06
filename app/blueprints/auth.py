from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from ..database.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user_id = None
    else:
        g.user_id = user_id


@bp.route('/')
def default():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('main.lobby'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'
        elif User.objects(username=username):
            error = f"Username '{username}'' is used!"

        if error is None:
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            new_user.save()
            return redirect(url_for('.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        if username is None:
            error = 'Incorrect username!'
        elif password is None:
            error = 'Empty password!'

        if error is None:
            user = User.objects(username=username).first()
            if not user:
                error = 'User is not exist!'
            elif not check_password_hash(user.password, password):
                error = 'Incorrect password!'

        if error is None:
            session.clear()
            session['user_id'] = str(user.id)
            return redirect(url_for('main.lobby'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.login'))
