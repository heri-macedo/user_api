from api.models import db
from api.models.user_model import User

class UserDAO:
    def get_all(self):
        return User.query.all()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def create(self, data):
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )
    
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update(self, user, data):
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
