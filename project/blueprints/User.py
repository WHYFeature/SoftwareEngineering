from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models import User
from models import db
from sqlalchemy import func
"""
将blueprints包中导入Book模块，blueprints为自定义目录下的包
"""
from blueprints import Book as bookpy

bp = Blueprint("User", __name__, url_prefix="/user")

"""
VerifyPossword函数检查密码正确性:
长度大于8、仅包含字母和数字
"""


def VerifyPassword(password):
    if len(password) < 8:
        return True
    for p in password:
        if p < 'a' or p > 'z':
            if p < 'A' or p > 'Z':
                if p > '9' or p < '0':
                    return True
    return False


"""
url = /user/register
POST方法传入用户名username、密码password、性别sex
"""


@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sex = request.form['sex']  # 1男 2女
        # sex = 1  # 测试用例

        # 检查用户名重复
        data = User.query.filter(User.username == username).all()
        if data != []:
            flash("重复的用户名", "danger")
            return render_template('register.html')

        # 检查密码格式
        if (VerifyPassword(password)):
            flash("密码格式错误", "danger")
            return render_template('register.html')

        uid = 0

        # 添加新用户
        uid = db.session.query(func.max(User.uid)).scalar() or 0
        uid += 1
        newUser = User(uid=uid, username=username,
                       sex=sex, level=0, password=generate_password_hash(password))
        print(newUser.password)
        db.session.add(newUser)
        db.session.commit()

        flash("注册成功", "success")
        session['status'] = 0  # 成功

        return redirect(url_for('User.login'))
    return render_template('register.html')


"""
url = /user/login
POST方法传入用户名username、密码password
"""


@bp.route('/login', methods=["GET", "POST"])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check_password_hash函数检查密码正确性
        data = User.query.filter(User.username == username).first()

        if data is None:
            flash("用户名错误", "danger")
            return redirect(url_for('User.login'))

        if check_password_hash(data.password, password):
            session['username'] = data.username
            session['uid'] = data.uid
            session['level'] = data.level
            # return render_template('index.html', books=bookpy.GetHotBook())
            flash("登录成功", "success")
            return redirect(url_for('root.index'))
        else:
            flash("密码错误", "danger")
            return redirect(url_for('User.login'))

    return render_template('login.html')


@bp.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop("uid", None)
    session.clear()
    response = redirect(url_for('root.index'))
    response.delete_cookie('session')
    # 删除cookie可能存在session未删除干净的问题，可能需要clear

    return response


@bp.route('/clear_status')
def clear_status():
    session.pop('status', None)
    return '', 204
