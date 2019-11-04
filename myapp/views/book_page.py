from flask import Blueprint, render_template, redirect, flash
from flask_login import current_user
from myapp.third_party_api.goodreads_api import get_reviews, get_review_stats
from myapp.models import Books
from myapp.helpers import redirect_back, is_book_in_bookshelf
from myapp.ext import db

book_pg = Blueprint('book_pg', __name__)


@book_pg.route('/book_page/<int:book_id>/<string:title>/<string:author>/<string:year>/<string:isbn>/<path:image_url>')
def book_page(book_id, isbn, title, author, year, image_url):
    return render_template("book_page.html",
                           book_id=book_id,
                           review_widget=get_reviews(isbn),
                           image_url=image_url,
                           review_stat=get_review_stats(isbn),
                           title=title,
                           author=author,
                           year=year,
                           book_in_bookshelf=is_book_in_bookshelf(book_id)
                           )


@book_pg.route('/add/<int:book_id>')
def add_to_bookshelf(book_id):
    try:
        book = Books.query.get(book_id)
        current_user.add_book(book)
        db.session.commit()
    except:
        flash('That book is already in your bookshelf.', 'info')
    return redirect(redirect_back('user.user_profile'))


@book_pg.route('/rm/<int:book_id>')
def remove_from_bookshelf(book_id):
    if current_user.is_authenticated:
        u = current_user
        user_books = u.bookshelf.all()
        for book in user_books:
            if book.id == book_id:
                user_books.remove(book)
                u.bookshelf = user_books
                db.session.commit()
                break
    return redirect(redirect_back('user.user_profile'))


