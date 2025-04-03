from flask import Blueprint
from flask import request
from flask import render_template

from sqlalchemy import func

from models import User
from models import db
from models import UserCollect

def getAllCollect(uid):
    datas = UserCollect.query.filter(UserCollect.uid==uid).all()

    collects = []

    if datas == []:
        collects = []
    else:
        collect = {}
        
    return collects
    


bp = Blueprint("Collect", __name__, url_prefix="/collect")

@bp.route('/addCollect')
def addCart():
    return 0