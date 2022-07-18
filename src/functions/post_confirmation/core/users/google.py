from . import GOOGLE, merge_users, create_native_user
from .abstract_user import AbstractUser
from .cognito import Cognito


class Google(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email=None, phone_number=None, first_name=None,
                 last_name=None):
        self.email = email
        if self.email is None:
            """
            This should never happened
            """
            raise Exception("Google must provide email address for user {}".format(username))
        # self.access_token = user_attributes.get('custom:access_token')
        self.username = username

        username_list = username.split("_")
        if len(username_list) != 2:
            """This is unexpected condition"""
            raise AttributeError("Username is incorrect")
        user_id = username_list[1]
        self.google_id = user_id
        self.cognito_id = cognito_id
        self.first_name = first_name
        self.last_name = last_name
        self.registration_method = GOOGLE
        self.user_pool_id = user_pool_id

    def update_user_email(self, client, user_pool_id):
        client.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=self.username,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'false'
                }, {
                    'Name': 'email',
                    'Value': ''
                }, {
                    'Name': 'name',
                    'Value': ''
                }
            ]
        )

    def payload(self):
        """

        :return:
        """
        return {
            "username": self.username,
            "cognito_id": self.cognito_id,
            "registration_method": self.registration_method,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "picture_url": None,  # @TODO Coming soon
            "phone_number": self.phone_number,
            "user_pool_id": self.user_pool_id
        }

    def link_accounts(self, client, user_pool_id, user_accounts):
        """user has already previous accounts"""
        print('Linking accounts from Email {} with provider {}: '.format(
            self.email,
            GOOGLE
        ))

        users = []
        # stop clearing google client data (email, email_verification, name)
        # self.update_user_email(client, user_pool_id)
        if len(user_accounts):
            # When user registers but he/she has account before.
            print("Start merge user {} accounts".format(self))
            for account in user_accounts:
                merge_users(client, user_pool_id, account['Username'], 'Google', self.username)
        else:
            # When user registers for the first time
            native_user = create_native_user(client, user_pool_id, self.email)
            print("Native User created with {}".format(native_user))
            username = native_user['User']['Username']
            merge_users(client, user_pool_id, username, 'Google', self.username)

            cognito_user = Cognito(username, username, user_pool_id, self.email)
            users.append(cognito_user)

        users.append(self)
        return users
