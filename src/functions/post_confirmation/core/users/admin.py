from . import ADMIN
from .abstract_user import AbstractUser


class Admin(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email, phone_number):
        self.username = username
        self.cognito_id = user_pool_id
        self.registration_method = ADMIN
        self.email = email.lower() if email else email

    def payload(self):
        pass

    def link_accounts(self, client, user_pool_id, user_accounts):
        pass
