from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    cash = db.Column(db.Float, default=10000)
    transaction = db.relationship('Transactions', backref='transactor', lazy='dynamic')

    def __repr__(self):
        return '<User {}, Email {}, Cash {}, id {}>'.format(self.username, self.email, self.cash, self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    coins_id = db.Column(db.Integer, db.ForeignKey('coins.id'))
    number = db.Column(db.Float)
    price = db.Column(db.Float)

    def __repr__(self):
        return '<User: {}, Coin: {}, Amount: {}, Price: {}, Time: {}>'.format(self.user_id, self.coins_id, self.number, self.price, self.timestamp)

class Coins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    longname = db.Column(db.String(200), index=True, unique=True)
    short = db.Column(db.String(15), index=True, unique=True)
    transaction = db.relationship('Transactions', backref='usedcoin', lazy='dynamic')

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.id, self.longname, self.short)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# db.session.query(func.sum(Transactions.number).label("sum")).filter_by(user_id=1).all() 
