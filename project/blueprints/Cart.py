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


def verifyQuantity(bid, quantity):
    data = Book.query.filter(Book.bid == bid).first()
    if data.number <= quantity:
        return False
    else:
        return True


@bp.route('/addCart', methods=["POST"])
def addCart():
    quantity = request.form["quantity"]
    bid = request.form["bid"]
    print(bid)
    uid = session["uid"]
    session["status"] = 0

    if verifyQuantity(bid=bid, quantity=quantity):
        session["status"] = 1  # 库存数量不足
        return redirect(url_for('Book.BookDetails', bid=bid))

    forms = OrderForm.query.filter(
        OrderForm.uid == uid, OrderForm.status == 0).all()
    if forms == []:
        oid = db.session.query(func.max(OrderForm.oid)).scalar() or 0
        oid += 1
        form = OrderForm(oid=oid, uid=uid, status=0)
        db.session.add(form)
        db.session.commit()

    form = OrderForm.query.filter(OrderForm.uid == uid,OrderForm.status == 0).first()

    detail = OrderDetails.query.filter(OrderDetails.oid == form.oid,OrderDetails.bid == bid).first()
    book = Book.query.filter(Book.bid == bid).first()
    if detail is None:
        detail = OrderDetails(oid = form.oid,bid = form.bid,number = quantity,price = book.price)
        db.session.add(detail)
    else:
        detail.number =detail.number+quantity
        detail.price = book.price
    book.number =bid.number - quantity

    db.session.close()

    return 0
