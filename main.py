from flask import Flask, request
from flask_cors import CORS
from db import db_session, init_db
from models import User
from validate_email import validate_email
from bcrypt import checkpw
import config

app = Flask(__name__)
app.config.from_object(config)

DEFAULT_PASS_LEN = 8


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/', methods=['GET'])
def index():
    return 'Hello!'


@app.route('/regi', methods=['POST'])
def regi():
    json_body = request.json
    name = json_body['username']
    password = json_body['password']
    email = json_body['email']

    if name is None or \
            len(name) is 0 or \
            password is None or \
            len(password) < DEFAULT_PASS_LEN or \
            not validate_email(email):
        return 'req params not valid.', 400

    if User.query.filter(User.email == email).count() is not 0:
        return 'user already exists.', 400

    user = User(name, email, password)
    db_session.add(user)
    db_session.commit()
    return 'create user successfully!', 200


@app.route('/login', methods=['POST'])
def login():
    json_body = request.json
    email = json_body['email'].encode('utf8')
    password = json_body['password'].encode('utf8')

    if not validate_email(email) or \
            password is None or \
            len(password) < DEFAULT_PASS_LEN:
        return 'req params not valid.', 400

    usr = User.query.filter_by(email=email).first()

    if usr is None:
        return 'user not exist.', 400
    else:
        if checkpw(password, usr.hashed_pass):
            return 'login successfully!', 200
        else:
            return 'password wrong.', 400


if __name__ == '__main__':
    init_db()
    CORS(app)
    app.run(port=9000)
