from . import EMAIL, MOBILE
from .abstract_user import AbstractUser


class Cognito(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email=None, phone_number=None):
        self.username = username
        self.cognito_id = cognito_id
        self.registration_method = MOBILE if phone_number else EMAIL
        self.email = email.lower() if email else email
        self.phone_number = phone_number
        self.user_pool_id = user_pool_id

    def link_accounts(self, client, user_pool_id, user_accounts):
        """user has already previous accounts"""
        print('Linking accounts from Email {} with provider {}: is not possible'.format(
            self.email,
            self.registration_method
        ))

        return [self]

    def payload(self):
        """

        :return:
        """
        return {
            "username": self.username,
            "cognito_id": self.cognito_id,
            "registration_method": self.registration_method,
            "email": self.email,
            "phone_number": self.phone_number,
            "user_pool_id": self.user_pool_id
        }
