from .extensions import db

log_food = db.Table(
    'log_food',
    db.Column('log_id', db.Integer, db.ForeignKey('log.id'), primary_key=True),
    db.Column('food_id',
              db.Integer,
              db.ForeignKey('food.id'),
              primary_key=True),
)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logDate = db.Column(db.Date, nullable=False)
    foods = db.relationship('Food',
                            secondary=log_food,
                            backref='log',
                            lazy='dynamic')
