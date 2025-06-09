"""
本文件为各数据库表建立了对应的ORM映射
对各表的控制按对应类对象的操作方式操作

对象关系映射（ORM）是 SQLAlchemy 的核心功能之一。
它允许你使用 Python 类来表示数据库表，使用类的实例表示表中的记录，
通过操作这些类和实例就能实现对数据库的增删改查操作
"""

from exts import db
from datetime import datetime
from enum import IntEnum


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
    uid = db.Column(db.Integer, db.ForeignKey("user.uid", ondelete='CASCADE'))
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
    uid = db.Column(db.Integer, db.ForeignKey("user.uid", ondelete='CASCADE'))
    bid = db.Column(db.Integer, db.ForeignKey("book.bid", ondelete='CASCADE'))
    collect_time = db.Column(db.TIMESTAMP, default=datetime.now)


class OrderForm(db.Model):
    __tablename__ = "orderform"
    oid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = uid = db.Column(db.Integer, db.ForeignKey(
        "user.uid", ondelete='CASCADE'))
    status = db.Column(db.Integer, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now)
    uaid = db.Column(db.Integer, db.ForeignKey(
        "useraddress.uaid", ondelete='CASCADE'))


class OrderDetails(db.Model):
    __tablename__ = "orderdetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oid = db.Column(db.Integer, db.ForeignKey(
        "orderform.oid", ondelete='CASCADE'), nullable=False)
    bid = db.Column(db.Integer, db.ForeignKey(
        "book.bid", ondelete='CASCADE'), nullable=False)
    number = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(10, 2))


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.bid', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.uid', ondelete='CASCADE'), nullable=False)
    comment_time = db.Column(
        db.DateTime, nullable=False, default=datetime.now)
    like_count = db.Column(db.Integer, default=0)
    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    book = db.relationship('Book', backref=db.backref('comments', lazy=True))


class LikeComment(db.Model):
    __tablename__ = "likecomment"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_id = db.Column(db.Integer, db.ForeignKey(
        'comment.comment_id', ondelete='CASCADE'), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey(
        'user.uid', ondelete='CASCADE'), nullable=False)
    # 联合唯一约束，防止一个用户对同一条评论重复点赞
    __table_args__ = (
        db.UniqueConstraint('comment_id', 'uid', name='uix_comment_uid'),
    )


class ImageUsage(IntEnum):
    AVATAR = 1    # 头像
    BOOK = 2      # 图书封面
    COMMENT = 3   # 评论配图
    OTHER = 4     # 其他


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    xusage = db.Column(db.Integer, nullable=False)
    xid = db.Column(db.Integer, nullable=False)
    img_path = db.Column(db.String(255), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('xusage', 'xid', name='uix_usage_xid'),
    )
