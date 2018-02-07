from flask import Flask, request
from flask_cors import CORS
from validate_email import validate_email
import json

import config
from db import db_session, init_db
from models import User

app = Flask(__name__)
app.config.from_object(config)

DEFAULT_NAME_LEN = 8


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
    if name is None or len(name) is 0 or \
            password is None or \
            len(password) < DEFAULT_NAME_LEN or \
            not validate_email(email):
        return 'req params not valid.', 400

    if User.query.filter(User.email == email).count() is not 0:
        return 'user already exists.', 400

    user = User(name, email, password)
    db_session.add(user)
    db_session.commit()
    return 'create user successfully!', 200


if __name__ == '__main__':
    init_db()
    CORS(app)
    app.run(port=9000)
