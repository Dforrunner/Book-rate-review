import datetime
from flask import current_app as app
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from ext import login_manager, db
from flask_login import current_user, login_user, logout_user, login_required
from is_safe_url import is_safe_url
# Forms
from forms.account_forms import SignInForm, SignUpForm, PassResetEmailForm, PassResetForm
# Utils
from util.token import generate_confirmation_token, confirm_token
from util.email import send_email
# User model
from models import User
# Helper functions
from helpers import redirect_to_profile, redirect_back

account = Blueprint('account', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def user_not_signed_in():
    flash('Sign in required.', 'info')
    next_url = request.url
    login_url = '%s?next=%s' % (url_for('account.signin'), next_url)
    return redirect(login_url)


def validate_email_verification_url(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')

    return email


@account.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('main.home'))


@account.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect_to_profile()

    form = SignUpForm()
    if form.validate_on_submit():
        # Create user and add to database
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    confirmed=False)

        db.session.add(user)
        db.session.commit()

        # User Activation
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('account.confirm_user', token=token, _external=True)
        html = render_template('user_account/account_activation/confirmation_email.html', confirm_url=confirm_url, username=user.username)
        subject = "Book R&R Email Confirmation"
        send_email(user.email, subject, html)

        # Once user has created an account and authenticated successfully log them in
        # Otherwise if they are not authenticated redirect them to sign in page
        login_user(user)
        if current_user.is_authenticated:
            return redirect(url_for("account.unconfirmed"))
        else:
            return redirect(url_for('account.signin'))

    return render_template('user_account/signup.html', form=form)


@account.route('/signin', methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = SignInForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                return render_template("user_account/signin.html", form=form, message_bottom="Invalid username or password")

            # Load user if user authorized
            login_user(user, remember=form.remember_me.data)
            next_url = request.args.get('next')

            if is_safe_url(next_url, allowed_hosts=app.config['ALLOWED_HOSTS']):
                abort(400)

            return redirect(next_url or redirect_to_profile())

    return render_template('user_account/signin.html', form=form)


"""******* ACTIVATE USER ******"""


@account.route('/confirm/<token>')
@login_required
def confirm_user(token):
    email = validate_email_verification_url(token)
    user = db.session.query(User).filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('main.home'))


@account.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('main.home')
    flash('Please confirm your account! (check email inbox and spam). ', 'warning')
    return render_template('user_account/account_activation/unconfirmed.html')


@account.route('/resend')
@login_required
def resend_confirmation():
    try:
        token = generate_confirmation_token(current_user.email)
        confirm_url = url_for('account.confirm_user', token=token, _external=True)
        html = render_template('user_account/account_activation/confirmation_email.html', confirm_url=confirm_url, username=current_user.username)
        subject = "Book R&R Email Confirmation"
        send_email(current_user.email, subject, html)
    except:
        flash('An error occurred while attempting to resend confirmation email. Please try again later. ', 'danger')
        return redirect(url_for('account.unconfirmed'))
    flash('A new confirmation email has been sent.', 'success')
    return redirect(redirect_back('account.unconfirmed'))


"""******* ACTIVATE USER END******"""

"""******* RESET PASSWORD ******"""


@account.route('/reset-password', methods=["GET", "POST"])
def send_pass_reset_email():
    form = PassResetEmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Generate user pass reset email
            token = generate_confirmation_token(form.email.data)
            pass_reset_url = url_for('account.confirm_pass_reset_url', token=token, _external=True)
            html = render_template('user_account/pass_reset/pass_reset_email.html', pass_reset_url=pass_reset_url)
            subject = "BookR&R Password Reset Email"
            send_email(form.email.data, subject, html)
            flash('Password reset email has been sent. Check your email inbox (or spam) for further instructions.', 'success')
    return render_template('user_account/pass_reset/enter_email.html', form=form)


@account.route('/reset-pass/confirm/<token>', methods=["GET", "POST"])
def confirm_pass_reset_url(token):
    email = validate_email_verification_url(token)
    user = db.session.query(User).filter_by(email=email).first_or_404()
    if user is not None:
        form = PassResetForm()
        if request.method == 'POST':
            if form.validate_on_submit():
                user.set_password(form.password.data)
                db.session.commit()
                flash('You successfully changed your password. Try signing in now.', 'success')
                return redirect(url_for('account.signin'))
        return render_template('user_account/pass_reset/reset_forgotten_pass.html', form=form)
    else:
        flash('Error trying to validate email. Try again.', 'danger')


"""******* RESET PASSWORD END ******"""


