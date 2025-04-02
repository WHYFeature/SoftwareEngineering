from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from models import User
from models import db
from sqlalchemy import func
from blueprints import Book as bookpy
bp = Blueprint("User", __name__, url_prefix="/user")


def VerifyPassword(password):
    if len(password) < 8:
        return True
    for p in password:
        if p < 'a' or p > 'z':
            if p < 'A' or p > 'Z':
                if p > '9' or p < '0':
                    return True
    return False


@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']  # 1男 2女
        # sex = 1  # 测试用例

        data = User.query.filter(User.username == username).all()
        if data != []:
            session['status'] = 1  # 错误，重复用户名
            return render_template('register.html')

        if (VerifyPassword(password)):
            session['status'] = 2  # 错误，密码格式错误
            return render_template('register.html')

        uid = (db.session.query(func.max(User.uid)
                                ).group_by("uid").all())[-1][-1]+1
        newUser = User(uid=uid, username=username,
                       sex=sex, level=0, password=password)
        print(newUser.password)
        db.session.add(newUser)
        db.session.commit()

        session['status'] = 0  # 成功

        return redirect(url_for('User.login'))
    return render_template('register.html')


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
            # return render_template('index.html', books=bookpy.GetHotBook())
            return redirect(url_for('root.index'))
        else:
            session['status'] = 'ERROR'

    return render_template('login.html')
