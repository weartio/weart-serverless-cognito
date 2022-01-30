import boto3


class AbstractUser:
    username = None
    email = None
    phone_number = None
    first_name = None
    last_name = None
    cognito_id = None
    boto3_client = boto3.client('cognito-idp')
    user_pool_id = None

    def payload(self):
        return {}

    def link_accounts(self, client, user_pool_id, user_accounts):
        pass

    def update_user_email(self, client, user_pool_id):
        client.admin_update_user_attributes(
            UserPoolId=user_pool_id,
            Username=self.cognito_id,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                }, {
                    'Name': 'email',
                    'Value': self.email
                }, {
                    'Name': 'name',
                    'Value': self.email
                }
            ]
        )

    # def update_user_alias_email(self):
    #     print("Start Update user alias email {}".format(self.username))
    #     self.boto3_client.admin_update_user_attributes(
    #         UserPoolId=self.user_pool_id,
    #         Username=self.username,
    #         UserAttributes=[
    #             {
    #                 'Name': 'custom:alias_email',
    #                 'Value': self.email
    #             }
    #         ]
    #     )
