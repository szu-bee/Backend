from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base
from bcrypt import hashpw, gensalt


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(100), nullable=False)
    feeds = relationship(
        'Feed',
        backref='user',
        lazy='dynamic',
        primaryjoin='User.id == Feed.user_id'
    )

    def __init__(self, name, email, pwd):
        self.name = name
        self.email = email
        self.hashed_pass = hashpw(pwd.encode('utf8'), gensalt())


class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    feed_url = Column(String(120), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    articles = relationship(
        'Article',
        backref='feed',
        lazy='dynamic',
        primaryjoin='Feed.id == Article.feed_id'
    )

    def __init__(self, name, url):
        self.name = name
        self.feed_url = url


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=True)
    desc = Column(String(500), nullable=True)
    pic = Column(String(120), nullable=True)
    isStarred = Column(Boolean, nullable=False)
    isRead = Column(Boolean, nullable=False)
    feed_id = Column(Integer, ForeignKey('feeds.id'))

    def __init__(self, title, desc, pic):
        self.title = title
        self.desc = desc
        self.pic = pic
        self.isStarred = False
        self.isRead = False
