from flask_login import UserMixin
import datetime
from ext import bcrypt, db

user_book_relation = db.Table('relationship_table',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                              db.Column('book_id', db.Integer, db.ForeignKey('books.id'), nullable=False),
                              db.PrimaryKeyConstraint('user_id', 'book_id'))


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    bookshelf = db.relationship("Books", secondary=user_book_relation, backref='user', lazy='dynamic')

    def add_book(self, book):
        self.bookshelf.append(book)

    def check_password(self, pw):
        return bcrypt.check_password_hash(self.password, pw)

    def set_password(self, pw):
        self.password = bcrypt.generate_password_hash(pw).decode('utf-8')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, email, username, password, confirmed, confirmed_on=None, **kwargs):
        self.username = username
        self.email = email
        self.set_password(password)  # set password using the set_password() function
        self.registered_on = datetime.datetime.now()
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on


class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    image = db.Column(db.String, nullable=True)
    document = db.Column(db.String)