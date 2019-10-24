import os


class Config(object):
    """Base configurations"""

    # main config
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
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
    MAIL_USERNAME = os.environ.get("APP_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("APP_MAIL_PASSWORD")

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # Todo: update allowed host before launch
    # Allowed hosts
    ALLOWED_HOSTS = '127.0.0.1'

    # Pagination
    POSTS_PER_PAGE = 21
