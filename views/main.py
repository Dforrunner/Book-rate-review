from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from ext import db
from models import Books

main = Blueprint('main', __name__)


@main.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    # split the searched terms into a list
    searched_terms = request.args.get('query').split()
    # if nothing searched redirect to homepage
    if len(searched_terms) == 0:
        return redirect(url_for('home'))
    else:
        queryable_terms = '&'.join(searched_terms)  # Postgres requires the & operator to search multiple terms
        books = db.session.query(Books).filter(Books.document.op('@@')(db.func.to_tsquery(queryable_terms))).paginate(page=page, per_page=app.config['POSTS_PER_HOME_PAGE'])
        message = ''
        if len(books.items) == 0:
            message = 'No search results found.'
        return render_template('home.html', books=books, message=message)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Books.query.paginate(page=page, per_page=app.config['POSTS_PER_HOME_PAGE'])

    next_url = url_for('main.home', page=books.next_num) \
        if books.has_next else None
    prev_url = url_for('main.home', page=books.prev_num) \
        if books.has_prev else None
    return render_template("home.html", books=books, next_url=next_url, prev_url=prev_url)