from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello</h1>'


@app.route('/<name>')
def helloName(name):
    return f'<h1>Hello {name}</h1>'


@app.route('/json')
def json():
    response = {
        'key': 1,
        'value': ['Soufiane', 'Man']
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
