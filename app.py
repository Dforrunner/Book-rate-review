from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# Flask Login
from flask_login import LoginManager
# Third party api module
from third_party_api.goodreads_api import get_reviews, get_review_stats
# Forms
from forms.account_forms import SignInForm, SignUpForm, CSRFProtect
# Models
from db.models import Books
# Config
from config import Config

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)

# CSRF
csrf = CSRFProtect(app)




'''
TODO:
ERROR below FIX
Look up passing url as argument 
https://www.youtube.com/watch?v=qYeWemghBxI
'''
@app.route('/book_page/<string:title>/<string:author>/<string:year>/<string:isbn>/<path:image_url>')
def book_page(isbn, title, author, year, image_url):
    return render_template("book_page.html",
                           review_widget=get_reviews(isbn),
                           image_url=image_url,
                           review_stat=get_review_stats(isbn),
                           title=title,
                           author=author,
                           year=year
                           )


@app.route('/signin', methods=["GET", "POST"])
def signin():
    form = SignInForm()
    return render_template('register/signin.html', title="Sign In", form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    return render_template('register/signup.html', title="Sign Up", form=form)


@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    searched_terms = request.args.get('query').split()
    if len(searched_terms) == 0:
        return redirect(url_for('home'))
    else:
        queryable_terms = '&'.join(searched_terms)  # Postgres requires the & operator to search multiple terms
        books = Books.query.filter("document @@ to_tsquery(:query)").params(query=queryable_terms).paginate(page=page, per_page=21)
        return render_template('home.html', books=books)


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Books.query.paginate(page=page, per_page=21)
    return render_template("home.html", books=books)


if __name__ == '__main__':
    app.run()
