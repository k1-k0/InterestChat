from flask import Flask, request, render_template, redirect, url_for
from user import User

app = Flask(__name__)
person = None

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
    if request.method == 'POST':
        print('WIP')
    else:
        return render_template('lobby.html', username=person.username)