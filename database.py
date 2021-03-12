from flask_sqlalchemy import SQLAlchemy
from datetime import date


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # words = db.relationship("Word", lazy="select", backref=db.backref("user", lazy="joined"))


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    date_found = db.Column(db.DateTime, nullable=False, default=date.today())
    user = db.relationship('User', backref=db.backref('words', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # words = db.relationship("RepDate", lazy="select", backref=db.backref("word", lazy="joined"))


class RepDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=date.today())
    word = db.relationship('Word', backref=db.backref('dates', lazy=True))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)