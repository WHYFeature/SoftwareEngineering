from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, Book, OrderForm, OrderDetails, UserAddress

bp = Blueprint("Orders", __name__, url_prefix="/orders")

@bp.route('/', methods=["GET"])
def view_orders():
    if 'uid' not in session:
        flash("请先登录再查看订单。", "warning")
        return redirect(url_for('Book.book_list'))  # 请根据你的实际登录路由调整

    uid = session['uid']
    orders = OrderForm.query.filter_by(uid=uid, status=1).order_by(OrderForm.time.desc()).all()

    order_list = []
    for order in orders:
        address = UserAddress.query.get(order.uaid)
        details = OrderDetails.query.filter_by(oid=order.oid).all()
        items = []
        total = 0
        for detail in details:
            book = Book.query.get(detail.bid)
            if book:
                subtotal = float(detail.price) * detail.number
                total += subtotal
                items.append({
                    'bookname': book.bookname,
                    'author': book.author,
                    'price': float(detail.price),
                    'quantity': detail.number,
                    'subtotal': subtotal
                })
        order_list.append({
            'oid': order.oid,
            'time': order.time.strftime('%Y-%m-%d %H:%M:%S'),
            'address': f"{address.receiver} {address.phone} - {address.address}" if address else "地址信息缺失",
            'orders_items': items,
            'total': total
        })

    return render_template("orders.html", orders=order_list)
