import datetime
from is_safe_url import is_safe_url
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
# Flask Login
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
# Third party api module
from third_party_api.goodreads_api import get_reviews, get_review_stats
# Forms
from forms.account_forms import SignInForm, SignUpForm, CSRFProtect
# Models
from db.models import Books, User
# Config
from config import Config
# Utils
from util.token import generate_confirmation_token, confirm_token
from util.email import send_email
from util.decorators import check_confirmed

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
    return User.query.get(int(user_id))


@app.route('/profile/<string:username>')
@login_required
@check_confirmed
def user_profile(username):
    if not current_user.is_authenticated or (current_user.id == 0):
        user_not_signed_in()
    return render_template("user_account/profile.html", user=current_user)


# Helper method to redirect users to their profile if they are already logged in
def redirect_to_profile():
    return redirect(url_for('user_profile', username=current_user.username))


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    user = db.session.query(User).filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account! (check email inbox and spam). ', 'warning')
    return render_template('user_account/account_activation/unconfirmed.html')


@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('user_account/account_activation/confirmation_email.html', confirm_url=confirm_url, username=current_user.username)
    subject = "Book R&R Email Confirmation"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('unconfirmed'))


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(salt_pass(form.password.data)):
                return render_template("user_account/signin.html", form=form, message_bottom="Invalid username or password")

            # Load user if user authorized
            login_user(user, remember=form.remember_me.data)
            next_url = request.args.get('next')

            if is_safe_url(next_url, allowed_hosts=app.config['ALLOWED_HOSTS']):
                abort(400)

            return redirect(next_url or redirect_to_profile())

    return render_template('user_account/signin.html', form=form)


@login_manager.unauthorized_handler
def user_not_signed_in():
    flash('Sign in required.', 'info')
    next_url = request.url
    login_url = '%s?next=%s' % (url_for('signin'), next_url)
    return redirect(login_url)


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('home'))


def salt_pass(pw):
    return pw + app.config['SECURITY_PASSWORD_SALT']


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect_to_profile()

    form = SignUpForm()
    if form.validate_on_submit():
        # Create user and add to database
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=salt_pass(form.password.data),
                    confirmed=False)

        db.session.add(user)
        db.session.commit()

        # User Activation
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('user_account/account_activation/confirmation_email.html', confirm_url=confirm_url, username=user.username)
        subject = "Book R&R Email Confirmation"
        send_email(user.email, subject, html)

        # Once user has created an account and authenticated successfully log them in
        # Otherwise if they are not authenticated redirect them to sign in page
        login_user(user)
        if current_user.is_authenticated:
            return redirect(url_for("unconfirmed"))
        else:
            return redirect(url_for('signin'))

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
        books = db.session.query(Books).filter(Books.document.op('@@')(db.func.to_tsquery(queryable_terms))).paginate(page=page, per_page=21)
        return render_template('home.html', books=books)


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    books = Books.query.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])

    next_url = url_for('home', page=books.next_num) \
        if books.has_next else None
    prev_url = url_for('home', page=books.prev_num) \
        if books.has_prev else None
    return render_template("home.html", books=books, next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
    app.run()
