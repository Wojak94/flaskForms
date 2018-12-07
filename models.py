from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    idUser = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    paswd = db.Column(db.String(120), unique=False)

    surveys = db.relationship('Survey', backref='users', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, login):
        return cls.query.filter_by(login = login).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.login,
                'password': x.paswd
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return '<User %r>' % self.login

class Survey(db.Model):
    __tablename__ = 'surveys'
    idSurvey = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    desc = db.Column(db.Text, unique=False)
    idUser = db.Column(db.Integer, db.ForeignKey('users.idUser'))
    isActive = db.Column(db.Boolean, default=0)
    subCount = db.Column(db.Integer, default=0)
    dueDate = db.Column(db.DateTime)

    questions = db.relationship('Question', backref='surveys', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

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

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
