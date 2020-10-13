from flask import Flask, jsonify, request, url_for, redirect, session, render_template

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'xtc2ORKM0eKKmYDoP9ntfauVfu4RqfPE'


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
        # return f'name : {name}'
        return redirect(url_for('helloName', name=name, age=12))
    return render_template('form.html')


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return jsonify({'results': 'Success', 'username': username, 'password': password})


if __name__ == "__main__":
    app.run(debug=True)
