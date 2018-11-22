from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    idUser = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    mail = db.Column(db.String(120), unique=True)
    paswd = db.Column(db.String(50), unique=False)

    surveys = db.relationship('Survey', backref='users', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.login

class Survey(db.Model):
    __tablename__ = 'surveys'
    idSurvey = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    desc = db.Column(db.Text, unique=False)
    idUser = db.Column(db.Integer, db.ForeignKey('users.idUser'))
    isActive = db.Column(db.Boolean)
    subCount = db.Column(db.Integer)
    dueDate = db.Column(db.DateTime)

    questions = db.relationship('Question', backref='surveys', lazy=True)

    def __repr__(self):
        return '<Survey %r>' % self.name

class Question(db.Model):
    __tablename__ = 'questions'
    idQuestion = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    type = db.Column(db.String(50), unique=False)
    idSurvey = db.Column(db.Integer, db.ForeignKey('surveys.idSurvey'))
    replyContent = db.Column(JSON)

    replies = db.relationship('Reply', backref='questions', lazy=True)

    def __repr__(self):
        return '<Question %r>' % self.content

class Reply(db.Model):
    __tablename__ = 'replies'
    idReply = db.Column(db.Integer, primary_key=True)
    idQuestion = db.Column(db.Integer, db.ForeignKey('questions.idQuestion'))
    reply = db.Column(JSON)

    def __repr__(self):
        return '<Question %r>' % self.content
