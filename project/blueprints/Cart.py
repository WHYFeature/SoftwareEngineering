from flask import Blueprint, request, session, render_template, redirect, url_for, flash
from sqlalchemy import func
from datetime import datetime

from blueprints.Profile import getAllAddress
from models import db, User, UserAddress, Book, OrderForm, OrderDetails

bp = Blueprint("Cart", __name__, url_prefix="/cart")

# Helper: 检查库存，若库存不足则返回 True
def is_stock_insufficient(bid, change_qty):
    book = Book.query.get(bid)
    if not book:
        return True
    return book.number < change_qty

@bp.route('/', methods=["GET"])
def view_cart():
    """ 显示当前用户购物车 """
    if 'uid' not in session:
        flash("请先登录再查看购物车。", "warning")
        return redirect(url_for('Book.book_list'))

    uid = session['uid']
    addresses = getAllAddress(uid)
    # 获取未完成订单
    order = OrderForm.query.filter_by(uid=uid, status=0).first()
    cart = {}
    total = 0

    if order:
        details = OrderDetails.query.filter_by(oid=order.oid).all()
        for item in details:
            book = Book.query.get(item.bid)
            if not book:
                continue
            subtotal = float(item.price) * item.number
            cart[item.bid] = {
                'title': book.bookname,
                'price': float(item.price),
                'quantity': item.number,
                'subtotal': subtotal
            }
            total += subtotal

    return render_template('cart.html', cart=cart, total=total,addresses=addresses)

@bp.route('/add', methods=["POST"])
def add_to_cart():
    """ 添加图书到购物车 """
    if 'uid' not in session:
        flash("请先登录后再添加购物车。", "warning")
        return redirect(request.referrer or url_for('Book.book_list'))

    uid = session['uid']
    bid = int(request.form.get('bid', 0))
    qty = int(request.form.get('quantity', 1))

    if is_stock_insufficient(bid, qty):
        flash("库存不足，无法添加。", "danger")
        return redirect(request.referrer or url_for('Book.book_list'))

    # 获取或创建购物车订单
    order = OrderForm.query.filter_by(uid=uid, status=0).first()
    if not order:
        next_oid = db.session.query(func.max(OrderForm.oid)).scalar() or 0
        order = OrderForm(oid=next_oid + 1, uid=uid, status=0, time=datetime.now())
        db.session.add(order)
        db.session.commit()

    # 添加或更新详情
    detail = OrderDetails.query.filter_by(oid=order.oid, bid=bid).first()
    book = Book.query.get(bid)
    if detail:
        detail.number += qty
        detail.price = book.price
    else:
        detail = OrderDetails(oid=order.oid, bid=bid, number=qty, price=book.price)
        db.session.add(detail)
    # 减少库存
    book.number -= qty

    db.session.commit()
    flash("已添加到购物车。", "success")
    return redirect(request.referrer or url_for('Cart.view_cart'))

@bp.route('/update', methods=["POST"])
def update_cart():
    """ 更新购物车商品数量 """
    if 'uid' not in session:
        flash("请先登录。", "warning")
        return redirect(url_for('Book.book_list'))

    uid = session['uid']
    order = OrderForm.query.filter_by(uid=uid, status=0).first()
    if not order:
        flash("购物车为空。", "info")
        return redirect(url_for('Cart.view_cart'))

    successNum = 0
    for key, value in request.form.items():
        if key.startswith('quantity_'):
            bid = int(key.split('_', 1)[1])
            new_qty = int(value)
            detail = OrderDetails.query.filter_by(oid=order.oid, bid=bid).first()
            if detail:
                diff = new_qty - detail.number
                if is_stock_insufficient(bid, diff if diff > 0 else 0):
                    data = Book.query.filter(Book.bid == bid).first()
                    flash(f"《{data.bookname}》库存不足。", "danger")
                    continue
                # 修改库存和数量
                if diff is 0:
                    continue
                book = Book.query.get(bid)
                book.number -= diff
                detail.number = new_qty
                successNum = successNum +1
    db.session.commit()
    if successNum:
        flash("购物车更新完成。", "success")
    return redirect(url_for('Cart.view_cart'))

@bp.route('/pay', methods=["POST"])
def pay():
    uid = session.get('uid')
    if not uid:
        flash("请先登录", "danger")
        return redirect(url_for("user.login"))

    selected_items = request.form.get("selected_items", "")  # 逗号分隔的 book_id
    address_id = request.form.get("address_id")

    if not selected_items or not address_id:
        flash("请选择商品和收货地址", "danger")
        return redirect(url_for("Cart.view_cart"))

    selected_bids = [int(bid) for bid in selected_items.split(",") if bid]
    if not selected_bids:
        flash("未选择商品", "warning")
        return redirect(url_for("Cart.view_cart"))

    # 找出该用户所有未支付订单（理论上只有一个）
    original_order = OrderForm.query.filter_by(uid=uid, status=0).first()
    if not original_order:
        flash("没有找到未支付订单", "warning")
        return redirect(url_for("Cart.view_cart"))

    # 获取所有订单明细
    details = OrderDetails.query.filter_by(oid=original_order.oid).all()

    # 分离：选中商品 vs 未选中商品
    selected_details = []
    unselected_details = []
    for d in details:
        if d.bid in selected_bids:
            selected_details.append(d)
        else:
            unselected_details.append(d)

    if not selected_details:
        flash("没有选择支付的商品", "warning")
        return redirect(url_for("Cart.view_cart"))

    #  原订单：只保留选中的商品
    for d in unselected_details:
        db.session.delete(d)

    original_order.status = 1
    original_order.uaid = address_id
    original_order.time = datetime.now()

    #  如有未选择商品：创建新订单保存它们
    if unselected_details:
        max_oid = db.session.query(db.func.max(OrderForm.oid)).scalar() or 0
        new_oid = max_oid + 1

        new_order = OrderForm(
            oid=new_oid,
            uid=uid,
            status=0,
            time=datetime.now(),  # 未支付也记时间
            uaid=None  # 地址未选
        )
        db.session.add(new_order)
        db.session.flush()

        for old_detail in unselected_details:
            new_detail = OrderDetails(
                oid=new_oid,
                bid=old_detail.bid,
                number=old_detail.number,
                price=old_detail.price
            )
            db.session.add(new_detail)

    db.session.commit()

    # 更新购物车中已支付的商品
    cart = session.get("cart", {})
    for bid in selected_bids:
        cart.pop(str(bid), None)
    session["cart"] = cart

    flash("订单支付成功！", "success")
    return redirect(url_for("Orders.view_orders"))


@bp.route('/remove/<int:bid>', methods=["GET"])
def remove_from_cart(bid):
    """ 从购物车移除商品 """
    if 'uid' not in session:
        flash("请先登录。", "warning")
        return redirect(url_for('Book.book_list'))

    uid = session['uid']
    order = OrderForm.query.filter_by(uid=uid, status=0).first()
    if order:
        detail = OrderDetails.query.filter_by(oid=order.oid, bid=bid).first()
        if detail:
            # 恢复库存
            book = Book.query.get(bid)
            book.number += detail.number
            db.session.delete(detail)
            db.session.commit()
            flash("已从购物车移除。", "success")
    return redirect(url_for('Cart.view_cart'))
