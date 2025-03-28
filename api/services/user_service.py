import logging
from api.daos.user_dao import UserDAO
from api.utils.email import Email

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def get_users(self):
        return self.user_dao.get_all()

    def create_user(self, data):
        email = Email(data.get('email')).address
        username = data.get('username')
        password = data.get('password')

        if not username:
            msg = 'No username provided'
            logger.error(msg)
            raise ValueError(msg)
        if not password:
            msg = 'No password provided'
            logger.error(msg)
            raise ValueError(msg)
        if self.user_dao.get_user_by_email(email):
            msg = 'Email already in use'
            logger.error(msg)
            raise ValueError(msg)
        if self.user_dao.get_user_by_username(username):
            msg = 'Username already in use'
            logger.error(msg)
            raise ValueError(msg)

        user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        logger.info(f'Creating user with username {username} and email {email}')
        
        return self.user_dao.create(user_data)

    def update_user(self, user_id, data):
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return None
        return self.user_dao.update(user, data)

    def delete_user(self, user_id):
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return None
        self.user_dao.delete(user)
        return user
