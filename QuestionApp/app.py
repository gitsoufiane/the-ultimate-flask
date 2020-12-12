from flask import Flask, render_template, url_for, g, request, session, redirect
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_current_user():
    user = None
    user_resutlt = None
    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute(
            'select id,name,password,expert,admin from users where name = ?', [user])
        user_resutlt = user_cur.fetchone()
    return user_resutlt


@app.route('/')
def index():
    # user = None
    # if 'user' in session:
    #     user = session['user']
    user = get_current_user()
    return render_template('home.html', user=user)


@app.route('/register', methods=['post', 'get'])
def register():
    db = get_db()
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        hashed_password = generate_password_hash(
            request.form['password'], method='sha256')
        db.execute('insert into users (name,password,expert,admin) values (?,?,?,?)', [
                   name, hashed_password, 0, 0])
        db.commit()
        session['user'] = name
        return redirect(url_for('index'))
    return render_template('register.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    user = get_current_user()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cur = db.execute(
            'select id,name,password from users where name=?', [name])
        user_result = user_cur.fetchone()
        if check_password_hash(user_result['password'], password):
            session['user'] = user_result['name']
            return redirect(url_for('index'))
        return '<h1>wrong passowrd</h1>'
    return render_template('login.html', user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/question')
def question():
    user = get_current_user()
    return render_template('question.html', user=user)


@ app.route('/answer')
def answer():
    user = get_current_user()
    return render_template('answer.html', user=user)


@ app.route('/ask')
def ask():
    user = get_current_user()
    return render_template('ask.html', user=user)


@ app.route('/unanswered')
def unanswered():
    user = get_current_user()
    return render_template('unanswered.html', user=user)


@ app.route('/users')
def users():
    user = get_current_user()
    db = get_db()
    users_cur = db.execute('select id,name,expert,admin from users')
    users_results = users_cur.fetchall()
    return render_template('users.html', user=user, users=users_results)


@app.route('/promote/<user_id>')
def promote(user_id):
    db = get_db()
    db.execute('update users set expert=1 where id=?', [user_id])
    db.commit()

    return redirect(url_for('users'))


if __name__ == "__main__":
    app.run(debug=True)
