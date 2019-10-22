from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from is_safe_url import is_safe_url
# Flask Login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# Third party api module
from third_party_api.goodreads_api import get_reviews, get_review_stats
# Forms
from forms.account_forms import SignInForm, SignUpForm, CSRFProtect
# Models
from db.models import Books, Users
# Config
from config import Config

db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
# This is called when the user is logged in, but they need to be reauthenticated because their session is stale
login_manager.refresh_view = 'signin'

# CSRF
csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/profile/<string:username>')
@login_required
def user_profile(username):
    if not current_user.is_authenticated or (current_user.id == 0):
        user_not_signed_in()

    user = Users.query.get(current_user.id)
    return render_template("user_account/profile.html", user=user)


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                return render_template("user_account/signin.html", form=form, message_bottom="Invalid username or password")

            # Load user if user authorized
            login_user(user, remember=form.remember_me.data)

            return redirect(url_for('user_profile', username=current_user.username))

    return render_template('user_account/signin.html', form=form)


@login_manager.unauthorized_handler
def user_not_signed_in():
    form = SignInForm()
    return render_template("user_account/signin.html", form=form, message_top="*Sign in first.")


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Create user and add to database
        user = Users(first_name=form.firstname.data,
                     last_name=form.lastname.data,
                     email=form.email.data,
                     username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Once user has created an account log them in
        login_user(user)

        return redirect(url_for('user_profile', username=form.username.data))

    return render_template('user_account/signup.html', form=form)


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
