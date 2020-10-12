from flask import Flask, jsonify, request, url_for, redirect

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello</h1>'


@app.route('/helloName', methods=['POST', 'GET'], defaults={'name': 'NAME', 'age': 0})
@app.route('/helloName/<string:name>/<int:age>', methods=['POST', 'GET'])
def helloName(name, age):
    return f'<h1>Hello {name} , you are {age} years old</h1>'


@app.route('/json')
def json():
    response = {
        'key': 1,
        'value': ['Soufiane', 'Man']
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
    return '''<form method="POST">
    <input type="text" name="name">
    <input type="submit">
    </form>
    '''


@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return jsonify({'results': 'Success', 'username': username, 'password': password})
if __name__ == "__main__":
    app.run(debug=True)
