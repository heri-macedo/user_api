import os
import logging

from flask import Flask
from api.models import db
from api.config import DevelopmentConfig
from api.controllers.user_controller import user_bp

def create_app():
    app = Flask(__name__)
    env = os.getenv('env', 'development')
    configure_logging(app)

    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_bp)

    return app

def configure_logging(app):
    if not app.logger.handlers:
        if not app.debug:
            file_handler = logging.FileHandler('app.log')
            file_handler.setLevel(logging.WARNING)
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d - %(funcName)s]'
            )
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)
        else:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
            console_handler.setFormatter(formatter)
            app.logger.addHandler(console_handler)