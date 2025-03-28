from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }