from flask import Flask, render_template, request, redirect, url_for, session

from exts import db
import config

app = Flask(__name__)
#app.secret_key = 'your_secret_key_here'  # 用于session加密

# 模拟数据
books = [
    {"id": 1, "title": "Python编程从入门到实践", "price": 89.00, "category": "编程"},
    {"id": 2, "title": "三体全集", "price": 128.00, "category": "科幻"},
    {"id": 3, "title": "人类简史", "price": 68.00, "category": "历史"}
]

@app.route('/')
def index():
    """首页：展示书店简介和图书分类"""
    return render_template('index.html', books=books)

@app.route('/books')
def book_list():
    """图书列表页"""
    category = request.args.get('category')
    filtered_books = [b for b in books if not category or b['category'] == category]
    return render_template('books.html', books=filtered_books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面"""
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # 简单模拟登录
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    """退出登录"""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    """购物车页面（需要登录）"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/register', methods=['GET', 'POST'])
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