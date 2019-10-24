from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    image = db.Column(db.String, nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    book_shelf = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=True)

    def check_password(self, pw):
        return check_password_hash(self.password, pw)

    def add_book(self, book):
        self.book_shelf.append_foreign_key(book)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, email, username, password, confirmed, confirmed_on=None, **kwargs):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

