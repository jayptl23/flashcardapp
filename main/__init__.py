from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'users.login'


def create_app(config_class=Config):
    # Create app and setup config
    app = Flask(__name__)
    app.config.from_object(Config)

    # Link extensions to the app
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)

    # Add route imports
    from main.users.routes import users
    from main.decks.routes import decks
    from main.cards.routes import cards
    from main.errors.handlers import errors

    # Register blueprints
    app.register_blueprint(users)
    app.register_blueprint(decks)
    app.register_blueprint(cards)
    app.register_blueprint(errors)

    return app
