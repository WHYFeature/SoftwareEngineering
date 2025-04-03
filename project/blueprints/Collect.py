from flask import Blueprint
from flask import request
from flask import render_template

from sqlalchemy import func

bp = Blueprint("Collect", __name__, url_prefix="/collect")

@bp.route('/addCollect')
def addCart():
    return 0