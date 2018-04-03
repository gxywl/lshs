from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True, index=True)
    pin = db.Column(db.String(64))
    username = db.Column(db.String(64))

    isadm=db.Column(db.Boolean,default=False)

    bujuans = db.relationship('Bujuan', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username


    def verify_pin(self, pin):
        return self.pin == pin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Xiangmu(db.Model):
    __tablename__ = 'xiangmus'
    id = db.Column(db.Integer, primary_key=True)
    xiangmu = db.Column(db.String(64))
    bujuans = db.relationship('Bujuan', backref='xiangmu', lazy='dynamic')

    def __repr__(self):
        return '<Xiangmu %r>' % self.xiangmu

class Bujuan(db.Model):
    __tablename__ = 'bujuans'
    id = db.Column(db.Integer, primary_key=True)
    #xiangmu = db.Column(db.String(64))
    jine = db.Column(db.Integer)
    outtime = db.Column(db.DateTime(), default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    xiangmu_id = db.Column(db.Integer, db.ForeignKey('xiangmus.id'))

    def __repr__(self):
        return '<Bujuan %r>' % self.id

