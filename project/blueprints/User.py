from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from models import User
from models import db

from sqlalchemy import func

bp = Blueprint("User", __name__, url_prefix="/user")


@bp.route('/register')
def register():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # 简单模拟登录
        return redirect(url_for('index'))
    return render_template('login.html')


@bp.route('/login', methods=["GET", "POST"])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = User.query.filter(User.username == username).first()
        if data.password == password:
            session['status'] = 'SUCCESS'
            session['username'] = data.username
            session['uid'] = data.uid
            session['level'] = data.level
            return render_template('index.html')
        else:
            session['status'] = 'ERROR'

    return render_template('login.html')
