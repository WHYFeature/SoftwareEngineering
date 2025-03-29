from flask import Blueprint
from flask import request
from flask import render_template

from models import Book
from models import db

from sqlalchemy import func

def GetHotBook():
    datas = Book.query.all()

    books = []
    for data in datas:
        if len(books) == 10 :
            break
        book_ = {}
        book_["id"]=data.bid
        book_["title"]=data.bookname
        book_["author"]=data.author
        book_["price"]=data.price
        book_["category"]=data.type_
        books.append(book_)
        
    return books

bp = Blueprint("Book", __name__, url_prefix="/books")

@bp.route('/')
def book_list():
    datas = Book.query.all()

    books = []
    for data in datas:
        book_ = {}
        book_["id"]=data.bid
        book_["title"]=data.bookname
        book_["author"]=data.author
        book_["price"]=data.price
        book_["category"]=data.type_
        books.append(book_)

    """图书列表页"""
    category = request.args.get('category')
    filtered_books = [b for b in books if not category or b['category'] == category]
    return render_template('books.html', books=filtered_books)
