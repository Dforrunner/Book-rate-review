import os

if not os.getenv("SECRET_KEY"):
    raise Exception(" ERROR: Secret key is not set.")
if not os.environ.get("DATABASE_URL"):
    raise Exception('ERROR: Database Url is not set.')
if not os.environ.get("SECURITY_PASSWORD_SALT"):
    raise Exception('ERROR: Security password salt is not set.')
if not os.environ.get("APP_MAIL_USERNAME"):
    raise Exception('ERROR: Mail username is not set')
if not os.environ.get("APP_MAIL_PASSWORD"):
    raise Exception('ERROR: Mail password is not set.')


class Config(object):
    """Base configurations"""

    # main config
    SECRET_KEY = os.getenv("SECRET_KEY")  # TODO: set SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")  # TODO: set DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")  # TODO: set SECURITY_PASSWORD_SALT
    DEBUG = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    USE_SESSION_FOR_NEXT = True

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Gmail authentication
    MAIL_USERNAME = os.environ.get("APP_MAIL_USERNAME")  # your email TODO: set APP_MAIL_USERNAME
    MAIL_PASSWORD = os.environ.get("APP_MAIL_PASSWORD")  # TODO: set APP_MAIL_PASSWORD

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")  # also your email TODO: set MAIL_DEFAULT_SENDER

    # Todo: update allowed host before launch
    # Allowed hosts
    ALLOWED_HOSTS = '127.0.0.1'

    # Pagination
    POSTS_PER_HOME_PAGE = 21
    POSTS_PER_PROFILE_PAGE = 18
