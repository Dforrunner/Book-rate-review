from flask import Flask
from myapp.ext import db, csrf_protect, login_manager, mail, bcrypt
from config import Config


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Flask Extensions
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        # Include our views
        from myapp.views import accounts, main, user, book_page

        # Registers Blueprints
        app.register_blueprint(user.user)
        app.register_blueprint(accounts.account)
        app.register_blueprint(book_page.book_pg)
        app.register_blueprint(main.main)

        return app
