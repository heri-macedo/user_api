import pytest
import os
import sys

from api import create_app
from api.models import db
from api.services.user_service import UserService
from api.schemas.user import UserCreate

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["ENV"] = "testing"
user_service = UserService()

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def user(app):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123"
    }
    user_validated = UserCreate(**user_data)
    with app.app_context():
        user = user_service.create_user(user_validated)
        return user.to_dict()