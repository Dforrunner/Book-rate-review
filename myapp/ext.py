"""Extensions module. Each extension is initialized in app.py"""
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_bcrypt import Bcrypt

csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
