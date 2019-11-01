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