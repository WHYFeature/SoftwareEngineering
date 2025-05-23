from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect, url_for, flash

from sqlalchemy import func

from models import User
from models import db
from models import UserCollect
from models import Book

"""
getAllCollect函数获取当前uid的所有收藏数据
"""


def getAllCollect(uid):
    datas = UserCollect.query.filter(UserCollect.uid == uid).all()

    collects = []

    if datas == []:
        collects = []
    else:
        for data in datas:
            collect = {}
            collect["bid"] = data.bid
            collect["collect_time"] = data.collect_time
            book = Book.query.filter(Book.bid == data.bid).first()
            collect["name"] = book.bookname
            collect["author"] = book.author
            collect["publisher"] = book.publisher
            collects.append(collect)

    return collects


bp = Blueprint("Collect", __name__, url_prefix="/collect")

"""
url = /collect/addCollect
仅允许POST传递书编号bid
"""


@bp.route('/addCollect', methods=["POST"])
def addCollect():
    bid = request.form["bid"]

    # 检查登录状态
    if "uid" not in session:
        flash("请登录后操作", "warning")
        return redirect(url_for('Book.BookDetails', bid=bid))

    uid = session["uid"]

    # 检查书籍是否已收藏
    session["status"] = 0
    data = UserCollect.query.filter(
        UserCollect.uid == uid, UserCollect.bid == bid).first()
    if data is not None:
        flash("请勿重复收藏", "warning")
        return redirect(url_for('Book.BookDetails', bid=bid))

    # 添加新收藏到数据库
    newCollect = UserCollect(uid=uid, bid=bid)
    db.session.add(newCollect)
    db.session.commit()
    flash("添加收藏成功", "success")
    return redirect(url_for('Book.BookDetails', bid=bid))


@bp.route('/delete_Collect', methods=["POST"])
def deleteCollect():
    bid = request.form["bid"]
    # 检查登录状态
    if "uid" not in session:
        flash("请登录后操作", "warning")
        return redirect(url_for('Book.BookDetails', bid=bid))

    uid = session["uid"]

    data = UserCollect.query.filter(
        UserCollect.uid == uid, UserCollect.bid == bid).first()

    db.session.delete(data)
    db.session.commit()
    flash("取消收藏成功", "success")
