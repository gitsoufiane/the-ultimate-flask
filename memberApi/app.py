from flask import Flask, g,  request, jsonify
from database import get_db
from functools import wraps
api_username = 'admin'
api_password = 'admin'

app = Flask(__name__)


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'authentication failed !'}), 403
    return decorated


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/members', methods=['GET'])
@protected
def get_members():
    db = get_db()
    members_cur = db.execute('select id,name,email,level from members')
    members_results = members_cur.fetchall()
    members = []
    for member in members_results:
        member_dict = {'id': member['id'], 'name': member['name'],
                       'email': member['email'], 'level': member['level']}
        members.append(member_dict)

    return jsonify({'members': members})


@app.route('/member/<int:member_id>', methods=['GET'])
@protected
def get_member(member_id):
    db = get_db()
    member_curs = db.execute(
        'select id,name,email,level from members where id=?', [member_id])
    member_result = member_curs.fetchone()
    response = {'id': member_result['id'], 'name': member_result['name'],
                'email': member_result['email'], 'level': member_result['level']}
    return jsonify({'member': response})


@app.route('/member', methods=['POST'])
@protected
def add_member():
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('insert into members (name,email,level) values (?,?,?)', [
               name, email, level])
    db.commit()

    member_cur = db.execute(
        'select id,name,email,level from members where name=?', [name])
    member_result = member_cur.fetchone()
    response = {'id': member_result['id'], 'name': member_result['name'],
                'email': member_result['email'], 'level': member_result['level']}
    return jsonify(response)


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
@protected
def edit_member(member_id):
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']
    db = get_db()
    db.execute('update members set name=?, email=?,level=? WHERE id=?', [
               name, email, level, member_id])
    db.commit()
    member_cur = db.execute(
        'select id,name,email,level from members where id = ?', [member_id])
    member_result = member_cur.fetchone()
    response = {'id': member_result['id'], 'name': member_result['name'],
                'email': member_result['email'], 'level': member_result['level']}
    return jsonify({'memeber': response})


@app.route('/member/<int:member_id>', methods=['DELETE'])
@protected
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id=?', [member_id])
    db.commit()
    return jsonify({'message': 'the member has been deleted'})


if __name__ == '__main__':
    app.run(debug=True)
