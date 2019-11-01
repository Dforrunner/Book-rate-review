from flask import Blueprint, render_template, redirect
from flask_login import current_user
from third_party_api.goodreads_api import get_reviews, get_review_stats
from models import Books
from helpers import redirect_back
from ext import db

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
                           year=year
                           )


@book_pg.route('/<int:book_id>')
def add_to_bookshelf(book_id):
    book = Books.query.get(book_id)
    current_user.add_book(book)
    db.session.commit()
    return redirect(redirect_back('user.user_profile'))


@book_pg.route('/rate-and-review')
def add_review():
    return render_template('add_review.html')
