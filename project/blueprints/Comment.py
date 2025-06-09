from flask import Blueprint, request, session, redirect, url_for, flash,render_template
from models import db, Book, User, Comment
from sqlalchemy import desc

bp = Blueprint("Comment", __name__, url_prefix="/comment")


@bp.route("/", methods=["GET"])
def showComment():
    comments = Comment.query.order_by(
        desc(Comment.like_count), desc(Comment.comment_time)).all()
    result = []
    for c in comments:
        cdata = {
            "comment_id": c.comment_id,
            "content": c.content,
            "book_id": c.book_id,
            "comment_time": c.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
            "like_count": c.like_count,
        }
        user = User.query.filter(User.uid == c.uid).first()
        username = user.username
        cdata["username"] = username
        book = Book.query.filter(Book.bid == c.book_id).first()
        bookname = book.bookname
        cdata["bookname"] = bookname
        result.append(cdata)
    return render_template('messages.html', comments = result)


@bp.route("/add", methods=["POST"])
def add_comment():
    content = request.form.get("content")
    bid = request.form.get("bid")

    if "uid" not in session:
        flash("请登录后操作", "warning")
        return redirect(url_for('Book.BookDetails', bid=bid))

    uid = session['uid']
    theBook = Book.query.filter(Book.bid == bid).first()

    if theBook is None:
        flash("无该书籍", "danger")
        return redirect(url_for('root.index'))

    comment = Comment(
        content=content,
        book_id=bid,
        user_id=uid,
        like_count=0
    )
    db.session.add(comment)
    db.session.commit()

    flash("评论添加成功", "success")
    return redirect(url_for('Book.BookDetails', bid=bid))

@bp.route("/delete", methods=["POST"])
def delete_comment():
    comment_id = request.form.get("comment_id")
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash("评论已删除", "success")
    return redirect(url_for('Profile._profile'))
