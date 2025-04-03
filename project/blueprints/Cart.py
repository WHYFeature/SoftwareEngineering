from flask import Blueprint
from flask import request
from flask import render_template

from sqlalchemy import func

bp = Blueprint("Cart", __name__, url_prefix="/cart")

@bp.route('/addCart')
def addCart():
    return 0