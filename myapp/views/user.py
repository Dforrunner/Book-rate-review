from flask import Blueprint, render_template, request, url_for, redirect, flash, current_app as app
from myapp.util.decorators import check_confirmed
from flask_login import login_required, current_user
from myapp.views.accounts import user_not_signed_in
from myapp.forms.account_forms import ChangePassForm, DeleteAccount, ChangeUsername
from myapp.ext import db

user = Blueprint('user', __name__, url_prefix='/profile', template_folder='templates')


@user.route('/<string:username>')
@login_required
@check_confirmed
def user_profile(username):
    if not current_user.is_authenticated or (current_user.id == 0):
        user_not_signed_in()
    return redirect(url_for('user.bookshelf'))


@user.route('/bookshelf')
@login_required
@check_confirmed
def bookshelf():
    page = request.args.get('page', 1, type=int)
    bookshelf = current_user.bookshelf.paginate(page=page, per_page=app.config['POSTS_PER_PROFILE_PAGE'])
    message = ''
    if len(bookshelf.items) == 0:
        message = "You currently don't have books in bookshelf."

    next_url = url_for('user.user_profile', username=current_user.username, page=bookshelf.next_num) \
        if bookshelf.has_next else None
    prev_url = url_for('user.user_profile', username=current_user.username, page=bookshelf.prev_num) \
        if bookshelf.has_prev else None
    return render_template("user_account/bookshelf.html",
                           user=current_user,
                           bookshelf=bookshelf,
                           next_url=next_url,
                           prev_url=prev_url,
                           message=message,
                           section_tittle='Bookshelf')


@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('user_account/settings/setting_options.html',
                           user=current_user,
                           section_tittle='Settings',
                           showBackArrow=False)


@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePassForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                u = current_user
                u.set_password(form.password.data)
                db.session.commit()
            except:
                flash("An error occured while attempting to change your password. Please try again later.", 'danger')
                return render_template('user_account/settings/change_password.html',
                                       user=current_user,
                                       form=form,
                                       section_tittle='Change Password',
                                       showBackArrow=True)
            flash("Password successfully changed.", "success")
    return render_template('user_account/settings/change_password.html',
                           user=current_user,
                           form=form,
                           section_tittle='Change Password',
                           showBackArrow=True)


@user.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsername()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                u = current_user
                u.username = form.username.data
                db.session.commit()
            except:
                flash("An error occurred while attempting to change your username. Please try again later. ", 'danger')
                return render_template('user_account/settings/change_username.html',
                                       user=current_user,
                                       form=form,
                                       section_tittle='Change Username',
                                       showBackArrow=True)

            flash("Username successfully change.", 'success')
    return render_template('user_account/settings/change_username.html',
                           user=current_user,
                           form=form,
                           section_tittle='Change Username',
                           showBackArrow=True)


@user.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    form = DeleteAccount()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                db.session.delete(current_user)
                db.session.commit()
            except:
                flash('An error occurred when attempting to delete your account. Please try again later.', 'danger')
                return render_template('user_account/settings/delete_account.html',
                                       user=current_user,
                                       form=form,
                                       section_tittle='Delete Account',
                                       showBackArrow=True)
            flash("Account successfully deleted. We'll miss you!", 'success')
            return redirect(url_for('main.home'))
    return render_template('user_account/settings/delete_account.html',
                           user=current_user,
                           form=form,
                           section_tittle='Delete Account',
                           showBackArrow=True)
