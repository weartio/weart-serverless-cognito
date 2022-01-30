from . import ADMIN
from .abstract_user import AbstractUser


class Admin(AbstractUser):
    def __init__(self, user_attributes, user_group, username=None, user_pool_id=None):
        self.username = username
        self.cognito_id = user_attributes.get('sub', username)
        self.registration_method = ADMIN
        self.user_group = user_group
        self.email = user_attributes.get('email')
        self.first_name = user_attributes.get('name', None)
        self.last_name = user_attributes.get('family_name', None)
        self.profile_image = user_attributes.get('picture', None)
        self.zip = user_attributes.get('custom:zip', None)

    def payload(self):
        pass

    def link_accounts(self, client, user_pool_id, user_accounts):
        pass
