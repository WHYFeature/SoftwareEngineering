from flask import Blueprint
from flask import request
from flask import session
from flask import render_template
from flask import redirect, url_for

from sqlalchemy import func

from models import User
from models import db
from models import UserAddress
from models import Book
from models import OrderForm
from models import OrderDetails

bp = Blueprint("Cart", __name__, url_prefix="/cart")

"""
verifyQuantity函数检查编号为bid的书籍
检查其数量是否满足quantity
满足则返回False,否则返回True
"""


def verifyQuantity(bid, quantity):
    data = Book.query.filter(Book.bid == bid).first()
    if data.number >= quantity:
        return False
    else:
        return True


"""
getUSerCart函数返回uid用户的购物车订单
购物车订单根据购物逻辑，仅会有一个订单status = False
"""


def getUserCart(uid):
    orderform = OrderForm.query(
        OrderForm.uid == uid, OrderForm.status == False).first()
    cartDetails = []
    datas = OrderDetails.query(OrderDetails.oid == orderform.oid).all()
    for data in datas:
        book = Book.query(Book.bid == data.bid).first()
        cartDetails.append({
            "bid": data.bid,
            "name": book.bookname,
            "author": book.author,
            "type_": book.type_,
            "version": book.version,
            "publiser": book.publiser,
            "number": data.number,
            "price": data.price
        })
    return cartDetails


"""
url=/cart/addCart
仅支持POST方式,提供bid和quantity
"""


@bp.route('/addCart', methods=["POST"])
def addCart():
    quantity = int(request.form["quantity"])
    bid = request.form["bid"]

    # 检查登录状态
    if "uid" not in session:
        session["status"] = 100
        return redirect(url_for('Book.BookDetails', bid=bid))

    uid = session["uid"]
    session["status"] = 0

    # 检查数量合法性
    if verifyQuantity(bid=bid, quantity=quantity):
        session["status"] = 1  # 库存数量不足
        return redirect(url_for('Book.BookDetails', bid=bid))
    # print(f"quantity = {quantity}")
    # 检查用户是否有购物车订单，如果没有则建立新订单
    forms = OrderForm.query.filter(
        OrderForm.uid == uid, OrderForm.status == 0).all()
    if forms == []:
        oid = db.session.query(func.max(OrderForm.oid)).scalar() or 0
        oid += 1
        form = OrderForm(oid=oid, uid=uid, status=0)
        db.session.add(form)
        db.session.commit()

    form = OrderForm.query.filter(
        OrderForm.uid == uid, OrderForm.status == 0).first()

    # 检查订单中是否具有相同图书，如果有则添加数量，否则建立新detail
    detail = OrderDetails.query.filter(
        OrderDetails.oid == form.oid, OrderDetails.bid == bid).first()
    book = Book.query.filter(Book.bid == bid).first()
    if detail is None:
        detail = OrderDetails(oid=form.oid, bid=bid,
                              number=quantity, price=book.price)
        db.session.add(detail)
    else:
        detail.number = detail.number+quantity
        detail.price = book.price
    book.number = book.number - quantity

    db.session.commit()
    return redirect(url_for('Book.BookDetails', bid=bid))


@bp.route('/')
def UserCart():
    uid = session['uid']
    cartdata = getUserCart(uid)
    return render_template('cart.html', items = cartdata)
