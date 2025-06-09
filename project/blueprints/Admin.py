from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Book, User, UserCollect, UserAddress, OrderDetails, OrderForm
from sqlalchemy import or_
from datetime import datetime

bp = Blueprint("Admin", __name__, url_prefix="/admin")

# 权限验证装饰器
def admin_required(view_func):
    def wrapper(*args, **kwargs):
        uid = session.get('uid')
        user = User.query.get(uid)
        if not user or user.level != 1:
            flash("您无权访问管理员页面", "danger")
            return redirect(url_for("index"))
        return view_func(*args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@bp.route("/", methods=["GET"])
@admin_required
def admin_page():
    tab = request.args.get("tab", "book")
    # 从请求参数获取搜索关键词
    book_search = request.args.get("book_search", "").strip()
    user_search = request.args.get("user_search", "").strip()

    # 书籍查询，支持模糊匹配书名和作者
    if book_search:
        book_list = Book.query.filter(
            or_(
                Book.bookname.like(f"%{book_search}%"),
                Book.author.like(f"%{book_search}%")
            )
        ).all()
    else:
        book_list = Book.query.all()

    # 用户查询，支持用户名模糊匹配
    if user_search:
        user_list = User.query.filter(
            User.username.like(f"%{user_search}%")
        ).all()
    else:
        user_list = User.query.all()

    return render_template("admin.html", books=book_list, users=user_list,
                           book_search=book_search, user_search=user_search,tab=tab)


@bp.route('/delete_book')
def delete_book():
    bid = request.args.get("bid")
    if not bid:
        flash("未指定书籍ID", "warning")
        return redirect(url_for("Admin.admin_page"))

    book = Book.query.get(bid)
    if not book:
        flash("书籍不存在", "warning")
        return redirect(url_for("Admin.admin_page"))

    # 查询该书是否存在订单详情，且对应订单状态为 1（已支付未完成）
    paid_unfinished_orders = (
        db.session.query(OrderDetails)
        .join(OrderForm, OrderDetails.oid == OrderForm.oid)
        .filter(OrderDetails.bid == bid, OrderForm.status == 1)
        .first()
    )
    if paid_unfinished_orders:
        flash("该书有未完成的已支付订单，无法删除", "danger")
        return redirect(url_for("Admin.admin_page"))

    # 如果无未完成订单，先删除相关收藏和订单详情
    UserCollect.query.filter_by(bid=bid).delete()
    OrderDetails.query.filter_by(bid=bid).delete()
    # 删除书籍
    db.session.delete(book)
    db.session.commit()
    flash("书籍删除成功", "success")
    return redirect(url_for("Admin.admin_page"))


@bp.route('/edit_book', methods=['GET', 'POST'])
def edit_book():
    if session.get('level') != 1:
        flash("没有权限操作", "danger")
        return redirect(url_for("Admin.admin_page"))

    bid = request.args.get("bid")
    book = Book.query.get(bid)

    if not book:
        flash("书籍不存在", "warning")
        return redirect(url_for("Admin.admin_page"))

    if request.method == 'POST':
        # 更新书籍信息
        book.bookname = request.form.get("bookname")
        book.author = request.form.get("author")
        book.type_ = request.form.get("type_")
        book.version = request.form.get("version")
        book.number = request.form.get("number")
        book.price = request.form.get("price")
        book.publisher = request.form.get("publisher")
        book.content = request.form.get("content")

        db.session.commit()
        flash("书籍信息修改成功", "success")
        return redirect(url_for("Admin.admin_page"))

    # GET 请求，显示修改页面
    return render_template("edit_book.html", book=book)

@bp.route('/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        bid = request.form.get('bid')
        # 先判断bid是否为空
        if not bid or not bid.isdigit():
            flash("书号必须填写且为数字", "warning")
            return redirect(url_for('Admin.add_book'))

        # 检查书号是否已存在
        existing = Book.query.get(int(bid))
        if existing:
            flash("书号已存在，请使用其他书号", "warning")
            return redirect(url_for('Admin.add_book'))

        book = Book(
            bid=int(bid),
            bookname=request.form.get('bookname'),
            author=request.form.get('author'),
            type_=request.form.get('type_'),
            version=request.form.get('version'),
            number=int(request.form.get('number') or 0),
            price=float(request.form.get('price') or 0),
            content=request.form.get('content'),
            publisher=request.form.get('publisher')
        )
        db.session.add(book)
        db.session.commit()
        flash("书籍添加成功", "success")
        return redirect(url_for('Admin.admin_page'))

    # GET请求，展示添加页面
    return render_template('add_book.html')

@bp.route("/user/delete/<int:uid>", methods=["POST"])
@admin_required
def delete_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("Admin.admin_page"))