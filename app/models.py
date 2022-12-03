from .extensions import db
from flask_login import UserMixin

log_user = db.Table(
    'log_user',
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('user.id'),
              primary_key=True),
)


class LogFoodUser(db.Model):
    log_id = db.Column(db.Integer, db.ForeignKey('log.id'), primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.Text)
    logs = db.relationship('Log',
                           secondary=log_user,
                           backref='user',
                           lazy='dynamic')


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logDate = db.Column(db.Date, nullable=False)
