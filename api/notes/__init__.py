import logging

from flask import Flask

from notes import config, db
from notes.errors import register_error_handlers
from notes.health import bp as health_bp
from notes.routes import bp as notes_bp


def create_app(overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)
    if overrides:
        app.config.update(overrides)

    logging.basicConfig(
        filename=app.config["LOG_FILE"],
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    db.init_app(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(notes_bp)
    register_error_handlers(app)
    return app
