from flask import Flask, request
from flask_cors import CORS
from db import db_session, init_db
from models import User
import validators
from bcrypt import checkpw
from feedparser import parse
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
            not validators.email(email):
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
    email = json_body['email']
    password = json_body['password'].encode('utf8')

    if not validators.email(email) or \
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


@app.route('/subsc', methods=['POST', 'GET'])
def subsc():
    if request.method == 'POST':
        feed_url = request.json['feed_url']

        if feed_url is None or not validators.url(feed_url):
            return 'req params not valid.', 400

        feed = parse(feed_url)
        if len(feed['entries']) is 0:
            return 'could not find a feed at the specified location.', 404

        # get articles new updates
        # feed = parse(url, modified=feed.modified, etag=feed.etag)

        for article in feed.entries:
            print article.title + ": " + article.link

        return 'ok', 200
    else:
        url = 'http://www.zhangxinxu.com/wordpress/?feed=rss2'
        rss_url = 'http://www.oschina.net/news/rss'
        return


if __name__ == '__main__':
    init_db()
    CORS(app)
    app.run(port=9000)
