from flask import Flask, render_template, request, redirect, url_for, session

from exts import db
import config

from blueprints import Book as BookPy  #蓝图模块，将应用模块化，方便管理和扩展
from blueprints import User
from blueprints import root
from blueprints import Profile
from blueprints import Cart
from blueprints import Collect
from blueprints import Orders
from blueprints import Comment
from blueprints import Admin

app = Flask(__name__)  #初始化Flask应用
app.secret_key = 'your_secret_key_here'  # 用于session加密

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI #配置数据库链接
db.init_app(app) #SQLAlchemy初始化与Flask app绑定

app.register_blueprint(BookPy.bp)  #蓝图注册，每个蓝图对应一个功能模块
app.register_blueprint(User.bp)
app.register_blueprint(root.bp)
app.register_blueprint(Profile.bp)
app.register_blueprint(Cart.bp)
app.register_blueprint(Collect.bp)
app.register_blueprint(Orders.bp)
app.register_blueprint(Comment.bp)
app.register_blueprint(Admin.bp)

@app.route('/message', methods=['GET', 'POST']) #定义一个路由/message，支持get和post请求
def message_board():
    """留言板页面"""
    if request.method == 'POST':
        # 处理留言提交
        pass
    return render_template('messages.html')

if __name__ == '__main__':
    app.run(debug=True)