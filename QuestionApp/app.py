from flask import Flask, render_template, url_for, g, request
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['post', 'get'])
def register():
    db = get_db()
    if request.method == "POST":
        name = request.form['name']
        hashed_password = generate_password_hash(
            request.form['password'], method='sha256')
        db.execute('insert into users (name,password,expert,admin) values (?,?,?,?)', [
                   name, hashed_password, 0, 0])
        db.commit()
        return 'USER CREATED'
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cur = db.execute(
            'select id,name,password from users where name=?', [name])
        user_result = user_cur.fetchone()
    return render_template('login.html')


@app.route('/question')
def question():
    return render_template('question.html')


@app.route('/answer')
def answer():
    return render_template('answer.html')


@app.route('/ask')
def ask():
    return render_template('ask.html')


@app.route('/unanswered')
def unanswered():
    return render_template('unanswered.html')


@app.route('/users')
def users():
    return render_template('users.html')


if __name__ == "__main__":
    app.run(debug=True)
