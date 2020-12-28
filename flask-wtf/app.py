from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecretKey'


class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
