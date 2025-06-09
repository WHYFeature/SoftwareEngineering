from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import db, Book, OrderForm, OrderDetails, UserAddress

bp = Blueprint("Orders", __name__, url_prefix="/orders")

def build_order_list(orders):
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
            'total': total,
            'status': order.status
        })
    return order_list

@bp.route('/', methods=["GET"])
def view_orders():
    if 'uid' not in session:
        flash("请先登录再查看订单。", "warning")
        return redirect(url_for('Book.book_list'))

    uid = session['uid']
    paid_orders_raw = OrderForm.query.filter_by(uid=uid, status=1).order_by(OrderForm.time.desc()).all()
    completed_orders_raw = OrderForm.query.filter_by(uid=uid, status=2).order_by(OrderForm.time.desc()).all()

    return render_template("orders.html",
                           paid_orders=build_order_list(paid_orders_raw),
                           completed_orders=build_order_list(completed_orders_raw),
                           active_tab="paid")  # 默认显示已支付

@bp.route('/confirm/<int:oid>', methods=['POST'])
def confirm_receipt(oid):
    if 'uid' not in session:
        flash("请先登录。", "warning")
        return redirect(url_for('Book.book_list'))  # 根据实际情况调整

    uid = session['uid']
    order = OrderForm.query.filter_by(oid=oid, uid=uid).first()

    if not order:
        flash("订单不存在。", "danger")
        return redirect(url_for('Orders.view_orders'))

    if order.status != 1:
        flash("订单无法确认收货。", "warning")
        return redirect(url_for('Orders.view_orders'))

    order.status = 2
    db.session.commit()
    flash("确认收货成功！", "success")
    return redirect(url_for('Orders.view_orders'))