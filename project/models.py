from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer)
    sex = db.Column(db.Integer)


class UserAddress(db.Model):
    __tablename__ = "useraddress"
    uaid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    address = db.Column(db.String(255), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    is_default = db.Column(db.Integer)


class Book(db.Model):
    bid = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    type_ = db.Column(db.String(255))
    version = db.Column(db.String(255))
    number = db.Column(db.Integer)
    price = db.Column(db.Integer)
    content = db.Column(db.String(255))
    publisher = db.Column(db.String(255))


class UserCollect(db.Model):
    __tablename__ = "usercollect"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    bid = db.Column(db.Integer, db.ForeignKey("book.bid"))
    collect_time = db.Column(db.TIMESTAMP, default=datetime.now)


class OrderForm(db.Model):
    __tablename__ = "orderform"
    oid = db.Column(db.Integer, primary_key=True)
    uid = uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    status = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    uaid = db.Column(db.Integer, db.ForeignKey(
        "useraddress.uaid"), nullable=False)


class OrderDetails(db.Model):
    __tablename__ = "orderdetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey(
        "orderform.oid"), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey("book.bid"), nullable=False)
    number = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2))
