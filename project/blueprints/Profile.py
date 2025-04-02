from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from models import User
from models import UserAddress
from models import db
from sqlalchemy import func

bp = Blueprint("Profile", __name__, url_prefix="/profile")


def getAllAddress(uid):
    datas = UserAddress.query.filter(UserAddress.uid == uid).all()
    addresses = []
    for data in datas:
        address = {}
        address['name'] = data.receiver
        address['phone'] = data.phone
        address['full_address'] = data.address
        addresses.append(address)
    return addresses

@bp.route('/', methods=["GET", "POST"])
def _profile():
    uid = session['uid']

    addresses = []
    addresses = getAllAddress(uid)
    print(addresses)

    return render_template('profile.html', address=addresses)


@bp.route('/update_profile', methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        username = request.form['username']

    return redirect(url_for('Profile._profile'))


@bp.route('/add_address', methods=["GET", "POST"])
def add_address():
    if request.method == "POST":
        phone = request.form['phone']
        receiver = request.form['name']
        address = request.form['full_address']
        uid = session['uid']

        newUserAddress = UserAddress(
            uid=uid, address=address, receiver=receiver, phone=phone, is_default=0)
        db.session.add(newUserAddress)
        db.session.commit()
        address = getAllAddress(uid)
        return redirect(url_for('Profile._profile'))

@bp.route('/change_password', methods=["GET", "POST"])
def change_password():
    return 0