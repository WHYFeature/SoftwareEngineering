from flask import Flask, render_template, request, redirect, url_for, session

from exts import db
import config

from blueprints import Book as BookPy
from blueprints import User
from blueprints import root

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 用于session加密

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

app.register_blueprint(BookPy.bp)
app.register_blueprint(User.bp)
app.register_blueprint(root.bp)

@app.route('/cart')
def cart():
    """购物车页面（需要登录）"""
    if 'username' not in session:
        return render_template('login.html')
    return render_template('cart.html')

@app.route('/user/register', methods=['GET', 'POST'])
def register():
    """注册页面"""
    if request.method == 'POST':
        # 实际开发中需要验证数据并存储到数据库
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/message', methods=['GET', 'POST'])
def message_board():
    """留言板页面"""
    if request.method == 'POST':
        # 处理留言提交
        pass
    return render_template('messages.html')

if __name__ == '__main__':
    app.run(debug=True)