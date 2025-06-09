"""
本文件为各数据库表建立了对应的ORM映射
对各表的控制按对应类对象的操作方式操作

对象关系映射（ORM）是 SQLAlchemy 的核心功能之一。
它允许你使用 Python 类来表示数据库表，使用类的实例表示表中的记录，
通过操作这些类和实例就能实现对数据库的增删改查操作
"""

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
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = uid = db.Column(db.Integer, db.ForeignKey("user.uid"))
    status = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    uaid = db.Column(db.Integer, db.ForeignKey("useraddress.uaid"))


class OrderDetails(db.Model):
    __tablename__ = "orderdetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey(
        "orderform.oid"), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey("book.bid"), nullable=False)
    number = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2))
