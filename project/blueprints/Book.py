from flask import Blueprint
from flask import request
from flask import render_template, session

from models import Book
from models import db
from models import UserCollect
from models import Comment
from models import User
from models import LikeComment

from sqlalchemy import func
from sqlalchemy import desc

from blueprints import UseImage
"""
GetHotBook获取了热度前十的书目录
返回各书的详细信息的列表
"""


def GetHotBook():
    datas = Book.query.all()

    books = []
    for data in datas:
        if len(books) == 10:
            break
        book_ = {}
        book_["id"] = data.bid
        book_["title"] = data.bookname
        book_["author"] = data.author
        book_["price"] = data.price
        book_["category"] = data.type_
        books.append(book_)

    return books


bp = Blueprint("Book", __name__, url_prefix="/books")

"""
url=/books/
仅允许GET方法
获取全部书籍数据放入books返回
"""


@bp.route('/')
def book_list():
    # 获取搜索关键字
    keyword = request.args.get('q', '').strip()

    # 使用SQLAlchemy进行过滤查询，如有关键字则按书名模糊匹配
    if keyword:
        # 注意：这里使用 ilike 实现大小写不敏感搜索，数据库需支持
        datas = Book.query.filter(Book.bookname.ilike(f"%{keyword}%")).all()
    else:
        datas = Book.query.all()

    # 构建前端需要的字典列表
    books = []
    for data in datas:
        books.append({
            'bid': data.bid,
            'title': data.bookname,
            'author': data.author,
            'price': data.price,
            'category': data.type_
        })

    return render_template('books.html', books=books)


"""
url=/book/details
使用带参数bid的GET方法
获取编号为bid的书籍的详细信息
"""


@bp.route('/details')
def BookDetails():
    bid = request.args.get('bid')
    # print(bid)
    data = Book.query.filter(Book.bid == bid).first()
    book = {}
    book["bid"] = data.bid
    book["bookname"] = data.bookname
    book["author"] = data.author
    book["type_"] = data.type_
    book["version"] = data.version
    book["number"] = data.number
    book["price"] = data.price
    book["content"] = data.content
    book["publisher"] = data.publisher
    book["img_path"] = UseImage.get_bookimage(bid)
    print(book["img_path"])

    book["inCollect"] = 0
    if "uid" in session:  # 检查是否处于登录状态，若处于登录状态则检查是否已收藏
        uid = session["uid"]
        # print(uid)
        collect = UserCollect.query.filter(
            UserCollect.uid == uid, UserCollect.bid == bid).first()
        if collect is not None:
            book["inCollect"] = 1  # 已收藏

    commentsdata = Comment.query.filter(Comment.book_id == bid) \
        .order_by(desc(Comment.like_count), desc(Comment.comment_time)) \
        .all()

    comments = []
    for c in commentsdata:
        cdata = {
            "comment_id": c.comment_id,
            "content": c.content,
            "comment_time": c.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
            "like_count": c.like_count,
        }
        user = User.query.filter(User.uid == c.user_id).first()
        username = user.username
        cdata["username"] = username
        liked = 0
        if "uid" in session:
            uid = session["uid"]
            lc = LikeComment.query.filter(
                LikeComment.comment_id == c.comment_id, LikeComment.uid == uid).first()
            if lc is not None:
                liked = 1
        cdata["liked"] = liked
        likenum = LikeComment.query.filter(LikeComment.comment_id == c.comment_id).count()
        if cdata["like_count"] is not likenum:
            c.like_count = likenum
            cdata["like_count"] = likenum
            db.session.commit()
        comments.append(cdata)

    book["comments"] = comments

    return render_template('book_detail.html', book=book)
