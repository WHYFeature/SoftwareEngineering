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

@bp.route('/')
def index():
    
    books = BookPy.GetHotBook()
    """首页：展示书店简介和图书分类"""
    return render_template('index.html', books=books)

@bp.route('/logout',methods = ["GET","POST"])
def logout():
    """退出登录"""
    session.pop('username', None)
    return redirect(url_for('root.index'))