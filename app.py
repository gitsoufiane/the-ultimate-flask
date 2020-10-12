from flask import Flask, jsonify, request

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


if __name__ == "__main__":
    app.run(debug=True)
