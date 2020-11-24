from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin,db.Model):
    """User model"""
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),nullable=False)
    email=db.Column(db.String(30),unique=True, nullable=False)
    password=db.Column(db.String(), nullable=False)
    room=db.Column(db.String(25), nullable=True)
    image_name=db.Column(db.String(), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<{self.username}>"

class Friend(db.Model):
    """User Friend"""
    __tablename__ = 'friend'
    id=db.Column(db.Integer,primary_key=True)
    send=db.Column(db.Integer,nullable=False)
    receive=db.Column(db.Integer,nullable=False)
    room_name=db.Column(db.String(25),nullable=False)

    def __init__(self, send,receive,room_name):
        self.send=send 
        self.receive=receive 
        self.room_name=room_name

    def __repr__(self):
        return f"<{self.room_name}>"            