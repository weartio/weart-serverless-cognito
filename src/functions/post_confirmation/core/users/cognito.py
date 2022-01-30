from . import EMAIL
from .abstract_user import AbstractUser


class Cognito(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email=None, phone_number=None):
        self.username = username
        self.cognito_id = cognito_id
        self.registration_method = EMAIL
        self.email = email
        self.phone_number = phone_number
        self.user_pool_id = user_pool_id

    def link_accounts(self, client, user_pool_id, user_accounts):
        """user has already previous accounts"""
        print('Linking accounts from Email {} with provider {}: is not possible'.format(
            self.email,
            EMAIL
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

    # @staticmethod
    # def create_custom_cognito_user(social_user, native_user_username):
    #     cognito_user_attributes = {
    #         'email': social_user.email,
    #         'name': social_user.first_name,
    #         'family_name': social_user.last_name,
    #         'picture': social_user.picture
    #     }
    #
    #     print("Start Creating custom cognito user for {}".format(native_user_username))
    #     cognito_user = Cognito(cognito_user_attributes, social_user.user_group, native_user_username)
    #     print("Custom Cognito User data {}".format(cognito_user))
    #
    #     return cognito_user
