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
            '''select
                id,name,password,expert,admin
                from users
                where name = ?''', [user])
        user_resutlt = user_cur.fetchone()
    return user_resutlt


@app.route('/')
def index():
    user = get_current_user()
    db = get_db()
    questions_cur = db.execute(
        '''select
            questions.id as question_id,
            questions.question_text,
            askers.name as asker_name,
            experts.name as expert_name
            from questions
            join users as askers on questions.asked_by_id=askers.id
            join users as experts on  experts.id=questions.expert_id
            where questions.answer_text is not null''')
    questions_results = questions_cur.fetchall()
    return render_template('home.html', user=user, questions=questions_results)


@app.route('/register', methods=['post', 'get'])
def register():
    db = get_db()
    user = get_current_user()
    if request.method == "POST":
        name = request.form['name']
        existing_user_cur = db.execute(
            'select id from users where name=?', [name])
        existing_user = existing_user_cur.fetchone()
        if existing_user:
            return render_template('register.html', user=user, error='User Already Exists!!')
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
    errors = None
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_cur = db.execute(
            'select id,name,password from users where name=?', [name])
        user_result = user_cur.fetchone()
        if user_result:
            if check_password_hash(user_result['password'], password):
                session['user'] = user_result['name']
                return redirect(url_for('index'))
            else:
                errors = 'the password is incorrect'
        else:
            errors = 'the username is incorect'

    return render_template('login.html', user=user,  error=errors)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/question/<question_id>')
def question(question_id):
    user = get_current_user()
    db = get_db()
    question_cur = db.execute(
        '''select
        questions.id as question_id,
        questions.question_text,
        questions.answer_text,
        askers.name as asker_name,
        experts.name as expert_name
        from questions
        join users as askers on questions.asked_by_id=askers.id
        join users as experts on  experts.id=questions.expert_id
        where questions.id=?''', [question_id])
    question_result = question_cur.fetchone()
    return render_template('question.html', user=user, question=question_result)


@ app.route('/answer/<question_id>', methods=['POST', 'GET'])
def answer(question_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    db = get_db()
    question_cur = db.execute(
        'select id,question_text from questions where id = ?', [question_id])
    question_result = question_cur.fetchone()
    if request.method == 'POST':
        answer = request.form['answer']
        db.execute('update questions set answer_text=? where id=?',
                   [answer, question_id])
        db.commit()
        return redirect(url_for('unanswered'))
    return render_template('answer.html', user=user, question=question_result)


@ app.route('/ask', methods=['POST', 'GET'])
def ask():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        question_text = request.form['question']
        expert_id = request.form['expert']
        db.execute('insert into questions (question_text,asked_by_id,expert_id) values (?,?,?)', [
                   question_text, user['id'], expert_id])
        db.commit()
        return redirect(url_for('ask'))
    expert_cur = db.execute('select id,name from users where expert=1')
    expert_results = expert_cur.fetchall()
    return render_template('ask.html', user=user, experts=expert_results)


@ app.route('/unanswered')
def unanswered():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    db = get_db()
    unanswered_cur = db.execute(
        '''select
        questions.id,
        questions.question_text,
        users.name
        from questions
        join users on users.id = questions.asked_by_id
        where questions.answer_text is NULL and questions.expert_id=?''', [user['id']])
    unanswered_results = unanswered_cur.fetchall()
    return render_template('unanswered.html', user=user, questions=unanswered_results)


@ app.route('/users')
def users():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user['admin'] == 0:
        return redirect(url_for('index'))
    db = get_db()
    users_cur = db.execute('select id,name,expert,admin from users')
    users_results = users_cur.fetchall()
    return render_template('users.html', user=user, users=users_results)


@app.route('/promote/<user_id>')
def promote(user_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('update users set expert=1 where id=?', [user_id])
    db.commit()
    return redirect(url_for('users'))


if __name__ == "__main__":
    app.run(debug=True)
