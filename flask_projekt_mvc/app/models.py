from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    lastname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    contact = db.Column(db.String(140))
    counter = db.Column(db.Integer)
    status =db.Column(db.String(64), index=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.firstname)


class Offers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    about_this = db.Column(db.String(140))
    name = db.Column(db.String(64), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Offers {}>'.format(self.name)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
