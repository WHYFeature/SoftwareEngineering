from exts import db
from datetime import datetime

class user(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer)
    sex = db.Column(db.Integer)

class Useraddress(db.Model):
    uaid = db.Column(db.Integer, primary_key=True,autoincrement=True)
    uid = db.Column(db.Integer,db.ForeignKey("user.uid"))
    address = db.Column(db.String(255), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    phone =db.Column(db.String(20))
    is_defailt = db.Column(db.Integer)