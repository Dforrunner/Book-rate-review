from flask import request, url_for
from flask_login import current_user


# Helper function to redirect to previous page.
def redirect_back(default):
    default_url = default
    return request.args.get('next') or \
           request.referrer or \
           url_for(default_url)


# Helper method to redirect users to their profile if they are already logged in
def redirect_to_profile():
    return url_for('user.user_profile', username=current_user.username)


# Helper function that checks if
def is_book_in_bookshelf(book_id):
    book_in_bookshelf = False
    # The code below checks to see if the book the user is looking at is currently in their bookshelf.
    # if so it sets the book_in_bookshelf variable to true.
    # This variable is used in book_page.html to change the Add to Bookshelf button to Book Added button
    if current_user.is_authenticated:
        u = current_user
        user_books = u.bookshelf.all()
        for book in user_books:
            if book.id == book_id:
                book_in_bookshelf = True
                break
    return book_in_bookshelf
