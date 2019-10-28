from flask import Blueprint, render_template
from third_party_api.goodreads_api import get_reviews, get_review_stats

book_pg = Blueprint('book_pg', __name__)


@book_pg.route('/book_page/<string:title>/<string:author>/<string:year>/<string:isbn>/<path:image_url>')
def book_page(isbn, title, author, year, image_url):
    return render_template("book_page.html",
                           review_widget=get_reviews(isbn),
                           image_url=image_url,
                           review_stat=get_review_stats(isbn),
                           title=title,
                           author=author,
                           year=year
                           )


@book_pg.route('/rate-and-review')
def add_review():
    return render_template('add_review.html')
