from flask import Flask, g,  request
from database import get_db


app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/members', methods=['GET'])
def get_members():
    pass


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    pass


@app.route('/member', methods=['POST'])
def add_member():
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('insert into members (name,email,level) values (?,?,?)', [
               name, email, level])
    db.commit()
    return '{}- {} -{}'.format(name, email, level)


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    pass


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
