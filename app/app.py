from flask import Flask
from flask_migrate import Migrate

from app.config import DevConfig
from app import db, ma


def create_app():
    """Intialize flask app."""
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    register_blueprints(app)

    db.init_app(app)
    ma.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    from app.views.auth.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.views.user.user import user_blueprint
    app.register_blueprint(user_blueprint)

