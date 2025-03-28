from api.models import db
from api.models.user_model import User

import logging

logger = logging.getLogger(__name__)

class UserDAO:
    def get_all(self):
        return User.query.limit(2).all()

    def paginate_users(self, page: int, per_page: int):
        return User.query.paginate(page=page, per_page=per_page, error_out=False)

    def get_user_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_user_by_username(self, username: str):
        return User.query.filter_by(username=username).first()

    def get_user_by_id(self, id: int):
        return User.query.filter_by(id=id).first()

    def create(self, data: dict):
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password")
        )
    
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def update_user(self, user, data: dict):
        user.username = data.get("username", user.username)
        
        user.email = str(data.get("email", user.email))
        try:
            db.session.commit()
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            db.session.rollback()
            raise e
        return userz
    

    def update_password(self, data):
        raise NotImplementedError
    
    def soft_delte(self, user):
        raise NotImplementedError

    def delete(self, user):
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            db.session.rollback()
