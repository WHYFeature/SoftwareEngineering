from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import request

from models import db
from blueprints import Book as BookPy

from sqlalchemy import func

bp = Blueprint("root", __name__, url_prefix="/")

"""
url = /
GET方法调用函数获取排行榜前十图书
"""
@bp.route('/')
def index():
    
    books = BookPy.GetHotBook()

    return render_template('index.html', books=books)

"""
url = /logout
GET方法清除session
"""
@bp.route('/logout',methods = ["GET","POST"])
def logout():
    
    session.pop('username', None)
    response = redirect(url_for('root.index'))
    response.delete_cookie('session')

    return response