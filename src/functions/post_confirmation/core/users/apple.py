from . import APPLE, merge_users, create_native_user
from .cognito import Cognito
from .abstract_user import AbstractUser


class Apple(AbstractUser):
    def __init__(self, username, cognito_id, user_pool_id, email=None, phone_number=None, first_name=None,
                 last_name=None):
        self.email = email
        self.username = username
        self.cognito_id = cognito_id
        self.registration_method = APPLE
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
            "picture_url": None,
            "phone_number": self.phone_number,
            "user_pool_id": self.user_pool_id
        }

    def link_accounts(self, client, user_pool_id, user_accounts):
        """user has already previous accounts"""
        print('Linking accounts from Email {} with provider {}: '.format(
            self.email,
            APPLE
        ))

        users = []
        # stop clearing google client data (email, email_verification, name)
        # self.update_user_email(client, user_pool_id)
        if len(user_accounts):
            # When user registers but he/she has account before.
            print("Start merge user {} accounts".format(self))
            for account in user_accounts:
                merge_users(client, user_pool_id, account['Username'], 'SignInWithApple', self.username)
        else:
            # When user registers for the first time
            native_user = create_native_user(client, user_pool_id, self.email)
            print("Native User created with {}".format(native_user))
            username = native_user['User']['Username']
            merge_users(client, user_pool_id, username, 'SignInWithApple', self.username)

            cognito_user = Cognito(username, username, user_pool_id, self.email)
            users.append(cognito_user)

        users.append(self)
        return users
