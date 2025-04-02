from flask import Blueprint
from flask import request
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from models import User
from models import db
from sqlalchemy import func

bp = Blueprint("Profile", __name__, url_prefix="/profile")

@bp.route('/', methods=["GET", "POST"])
def _profile():
    return render_template('profile.html')