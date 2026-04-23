from flask import Flask
from ingestion.extensions import db, ma, migrate
from ingestion.config import get_config


def create_app():
    app = Flask("ingestion")

    # Basic configuration
    app_config = get_config()
    app.config.from_object(app_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Create tables within application context
    with app.app_context():
        db.create_all()

    # Registrer models
    from . import models

    # Register routes
    from .routes import blueprint

    app.register_blueprint(blueprint)

    return app
