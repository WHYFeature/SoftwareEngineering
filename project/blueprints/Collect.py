from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect, url_for

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

    #检查登录状态
    if "uid" not in session:
        session["status"] =  100
        return redirect(url_for('Book.BookDetails', bid=bid))

    uid = session["uid"]

    #检查书籍是否已收藏
    session["status"] = 0
    data = UserCollect.query.filter(
        UserCollect.uid == uid, UserCollect.bid == bid).first()
    if data is not None:
        session["status"]=1 #重复的收藏
        return redirect(url_for('Book.BookDetails', bid=bid))
        
    #添加新收藏到数据库
    newCollect = UserCollect(uid=uid, bid=bid)
    db.session.add(newCollect)
    db.session.commit()
    return redirect(url_for('Book.BookDetails', bid=bid))
