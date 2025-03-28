import logging
from deprecated import deprecated

from api.daos.user_dao import UserDAO
from api.utils.email import Email

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self):
        self.user_dao = UserDAO()

    def get_user(self, id):
        user = self.user_dao.get_user_by_id(id)

        if not user:            
            msg = "User does not exist"
            logger.error(msg)
            raise ValueError(msg)

        return user.to_dict()

    @deprecated("This method is deprecated. Use get_users_paginated instead.")
    def get_users(self):
        users_list = [user.to_dict() for user in self.user_dao.get_all()]
        logger.info(f"Returning {len(users_list)} users")
        return users_list

  
    def get_users_paginated(self, page, per_page):
        pagination = self.user_dao.paginate_users(page, per_page)
        return {
            "users": [user.to_dict() for user in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "next_page": pagination.next_num,
            "per_page": per_page
        }


    def create_user(self, data):
        email = data.email.address
        username = data.username
        password = data.password

        if not username:
            msg = "No username provided"
            logger.error(msg)
            raise ValueError(msg)
        if not password:
            msg = "No password provided"
            logger.error(msg)
            raise ValueError(msg)
        if self.user_dao.get_user_by_email(email):
            msg = "Email already in use"
            logger.error(msg)
            raise ValueError(msg)
        if self.user_dao.get_user_by_username(username):
            msg = "Username already in use"
            logger.error(msg)
            raise ValueError(msg)

        user_data = {
            "username": username,
            "email": email,
            "password": password
        }

        logger.info(f"Creating user with username {username} and email {email}")
        
        return self.user_dao.create(user_data)


    def update_user(self, id, data):
        current_user = self.user_dao.get_user_by_id(id=id)
        if not current_user:
            raise ValueError("User does not exist")
        if data.get("email") == current_user.email:
            raise ValueError("Email matches current one.")
        if data.get("username") == current_user.username:
            raise ValueError("Username matches current one")

        return self.user_dao.update_user(current_user, data)


    def delete_user(self, id):
        user = self.user_dao.get_user_by_id(id)
        if not user:
            raise ValueError("User does not exist")
        self.user_dao.delete(user)
        
    
    def soft_delete(self, id):
        # Implement if time left.
        raise NotImplementedError
