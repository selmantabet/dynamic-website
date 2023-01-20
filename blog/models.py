"""
Database Models

Developed by Selman Tabet @ https://selman.io/
------------------------------------------------
Developed for Coursework 2 of the CMT120 course at Cardiff University

Based on a template by Dr. Natasha Edwards (Instructor - Cardiff University COMSC)
"""

from datetime import datetime
from blog import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128))
    creation_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    settings_json = db.Column(db.String(200), default="{}")
    post = db.relationship('Post', backref='user',
                           lazy=True, cascade="all, delete")
    comment = db.relationship(
        'Comment', backref='user', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(40), nullable=False,
                           default='default.jpg')
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship(
        'Comment', backref='post', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"Post('{self.date}', '{self.title}', '{self.content}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.author_id} on {self.date}', '{self.content}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
