from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect,url_for

from sqlalchemy import func

from models import User
from models import db
from models import UserCollect
from models import Book

def getAllCollect(uid):
    datas = UserCollect.query.filter(UserCollect.uid==uid).all()

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

@bp.route('/addCollect',methods = ["POST"])
def addCollect():
    bid = request.form["bid"]
    uid = session["uid"]
    
    newCollect = UserCollect(uid = uid,bid=bid)
    db.session.add(newCollect)
    db.session.commit()
    return redirect(url_for('Book.BookDetails', bid=bid))