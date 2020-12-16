from flask import Flask

app = Flask(__name__)


@app.route('/members', methods=['GET'])
def get_members():
    pass


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    pass


@app.route('/member', methods=['POST'])
def add_member():
    pass


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    pass


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)
