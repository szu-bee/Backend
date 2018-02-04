from sqlalchemy import Column, Integer, String
from db import Base
from bcrypt import hashpw, gensalt


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    hashed_pass = Column(String(100), nullable=False)

    def __init__(self, name, email, pwd):
        self.name = name
        self.email = email
        self.hashed_pass = hashpw(pwd.encode('utf8'), gensalt())


class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    feed_url = Column(String(120), unique=True, nullable=False)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=True)
    desc = Column(String(500), nullable=True)
    pic = Column(String(120), nullable=True)