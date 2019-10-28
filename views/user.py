from flask import Blueprint, render_template
from util.decorators import check_confirmed
from flask_login import login_required, current_user
from views.accounts import user_not_signed_in

user = Blueprint('user', __name__)


@user.route('/profile/<string:username>')
@login_required
@check_confirmed
def user_profile(username):
    if not current_user.is_authenticated or (current_user.id == 0):
        user_not_signed_in()
    return render_template("user_account/profile.html", user=current_user)
