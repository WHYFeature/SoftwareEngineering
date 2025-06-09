from models import ImageUsage
from models import Image


def get_bookimage(bid):
    xid = bid
    xusage = ImageUsage.BOOK.value
    data = Image.query.filter(Image.xid == xid, Image.xusage == xusage).first()
    path = ''
    if data is None:
        path = '../static/uploads/default.png'
    else:
        path = data.img_path
    return path
