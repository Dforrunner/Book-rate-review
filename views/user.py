from flask import Blueprint, render_template, request, url_for, current_app as app
from util.decorators import check_confirmed
from flask_login import login_required, current_user
from views.accounts import user_not_signed_in

user = Blueprint('user', __name__, url_prefix='/profile')


@user.route('/<string:username>')
@login_required
@check_confirmed
def user_profile(username):
    page = request.args.get('page', 1, type=int)
    bookshelf = current_user.bookshelf.paginate(page=page, per_page=app.config['POSTS_PER_PROFILE_PAGE'])
    message = ''
    if len(bookshelf.items) == 0:
        message = "You currently don't have books in bookshelf."

    next_url = url_for('user.user_profile', username=current_user.username, page=bookshelf.next_num) \
        if bookshelf.has_next else None
    prev_url = url_for('user.user_profile', username=current_user.username, page=bookshelf.prev_num) \
        if bookshelf.has_prev else None

    if not current_user.is_authenticated or (current_user.id == 0):
        user_not_signed_in()
    return render_template("user_account/profile.html",
                           user=current_user,
                           bookshelf=bookshelf,
                           next_url=next_url,
                           prev_url=prev_url,
                           message=message)


