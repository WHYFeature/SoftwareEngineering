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
        book_["bid"]=data.bid
        book_["title"]=data.bookname
        book_["author"]=data.author
        book_["price"]=data.price
        book_["category"]=data.type_
        books.append(book_)

    """图书列表页"""
    category = request.args.get('category')
    filtered_books = [b for b in books if not category or b['category'] == category]
    return render_template('books.html', books=filtered_books)

@bp.route('/details')
def BookDetails():
    bid = request.args.get('bid')
    print(bid)
    data = Book.query.filter(Book.bid == bid).first()
    book ={}
    book["bookname"]= data.bookname
    book["author"]= data.author
    book["type_"]=data.type_
    book["version"]=data.version
    book["number"]=data.number
    book["price"]=data.price
    book["content"]=data.content
    book["publisher"]=data.publisher

    return render_template('book_detail.html', book=book)