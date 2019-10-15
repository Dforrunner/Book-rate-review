import requests
import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from goodreads_api import *
from librarything_api import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/book_page/<string:title>/<string:author>/<string:year>/<string:isbn>')
def book_page(isbn, title, author, year):
    return render_template("book_page.html",
                           review_widget=get_reviews(isbn),
                           image_url=get_cover_image_url(isbn, "large"),
                           review_stat=get_review_stats(isbn),
                           title=title,
                           author=author,
                           year=year
                           )


@app.route('/')
@app.route('/home')
def home():
    books = db.execute("SELECT * FROM books").fetchall()
    return render_template("home.html", books=books)


def main():
    isbn = "1857231082"
    return render_template("home.html", image_url=get_cover_image_url(isbn, "large"))


if __name__ == '__main__':
    app.run()
