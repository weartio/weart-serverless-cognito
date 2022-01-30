from . import APPLE
from .abstract_user import AbstractUser


class Apple(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email=None, phone_number=None, first_name=None,
                 last_name=None):
        self.email = email
        self.username = username
        self.cognito_id = cognito_id
        self.registration_method = APPLE
        self.user_pool_id = user_pool_id

    def payload(self):
        """

        :return:
        """
        return {
            "username": self.username,
            "cognito_id": self.cognito_id,
            "registration_method": self.registration_method,
            "email": self.email,
            "user_pool_id": self.user_pool_id
        }

    def link_accounts(self, client, user_pool_id, user_accounts):
        """user has already previous accounts"""
        pass
