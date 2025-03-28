import os
import logging

from flask import Flask
from flask_migrate import Migrate
from api.models import db
from api.config import DevelopmentConfig, TestingConfig
from api.controllers.user_controller import user_bp

def create_app():
    app = Flask(__name__)
    env = os.getenv('ENV', 'development')
    configure_logging(app)

    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    if env == 'testing':
        app.config.from_object(TestingConfig)

    db.init_app(app)
    migrate = Migrate(app, db)

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