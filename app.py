from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'xtc2ORKM0eKKmYDoP9ntfauVfu4RqfPE'


def connect_db():
    sql = sqlite3.connect('./data.db')
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return '<h1>Hello</h1>'


@app.route('/helloName', methods=['POST', 'GET'], defaults={'name': 'NAME', 'age': 0})
@app.route('/helloName/<string:name>/<int:age>', methods=['POST', 'GET'])
def helloName(name, age):
    session['name'] = name
    return render_template('home.html', name=name, age=age, display=True, myList=[1, 2, 3, 4, 5])


@app.route('/json')
def json():
    name = session['name']
    response = {
        'key': 1,
        'value': ['Soufiane', 'Man'],
        'name': name
    }
    return jsonify(response)


@app.route('/query')
def query():
    name = request.args.get('name')
    age = request.args.get('age')
    return f"you are on Query Page --- name : {name} | age : {age}"


@app.route('/formData', methods=['POST', 'GET'])
def formData():
    if (request.method == 'POST'):
        name = request.form['name']
        location = request.form['location']
        # return f'name : {name}'
        db = get_db()
        db.execute('insert into users (name, location) values (?,?)', [
                   name, location])
        db.commit()
        return redirect(url_for('helloName', name=name, age=12))
    return render_template('form.html')


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return jsonify({'results': 'Success', 'username': username, 'password': password})


@app.route('/sqlresults')
def sqlresults():
    db = get_db()
    cursor = db.execute('select * from users')
    results = cursor.fetchall()
    data = []
    for row in results:
        data.append(list(row))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
