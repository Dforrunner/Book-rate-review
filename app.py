import requests
import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager, UserMixin
from flask_wtf.csrf import CSRFProtect
from goodreads_api import *
from book_cover_api import *
from db.models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
    return render_template('register/signin.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('register/signup.html')


@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    terms = request.args.get('query')
    books = Books.query.filter("weights @@ to_tsquery(:terms)").params(terms=terms).paginate(page=page, per_page=21)
    return render_template('home.html', books=books)


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Books.query.paginate(page=page, per_page=21)
    return render_template("home.html", books=books)


if __name__ == '__main__':
    app.run()
