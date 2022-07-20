import json
import os

import boto3

from .abstract_user import AbstractUser
import random
import string

FACEBOOK = "FACEBOOK"
GOOGLE = "GOOGLE"
APPLE = "APPLE"
EMAIL = "EMAIL"
ADMIN = "ADMIN"
MOBILE = "MOBILE"


def get_random_string(length):
    """
    Generate random string
    :param length:
    :return:
    """
    letters_length = length - 1
    digits_length = 1

    letters = string.ascii_lowercase
    digits = string.digits

    letters_string = ''.join(random.choices(letters, k=letters_length))
    digits_string = ''.join(random.choices(digits, k=digits_length))
    return letters_string + digits_string


def list_similar_users(client, user_pool_id, email, username):
    """

    :param client:
    :param user_pool_id:
    :param email:
    :param username:
    :return:
    """
    response = client.list_users(
        UserPoolId=user_pool_id,
        AttributesToGet=[
            'email',
            'sub'
        ],
        Filter='email = "{}"'.format(email)
    )
    users = []
    for user in response['Users']:
        if 'Username' in user and user['Username'] != username:
            users.append(user)
    return users


def merge_users(client, user_pool_id, username, provider, user_id):
    # If the signup is coming from a social provider, link the accounts
    # with admin_link_provider_for_user function
    print('> Linking user: ', username)
    print('> Provider Id: ', user_id)
    try:
        response = client.admin_link_provider_for_user(
            UserPoolId=user_pool_id,
            DestinationUser={
                'ProviderName': 'Cognito',
                'ProviderAttributeValue': username
            },
            SourceUser={
                'ProviderName': provider,
                'ProviderAttributeName': 'Cognito_Subject',
                'ProviderAttributeValue': user_id
            }
        )

        return response
    except Exception as e:
        print('exception in merge users: ', e)
        pass


def create_native_user(client, user_pool_id, email):
    user = client.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        UserAttributes=[
            {
                'Name': 'email',
                'Value': email
            },
            {
                'Name': 'email_verified',
                'Value': "true"
            },
        ],
        ValidationData=[
            {
                'Name': 'string',
                'Value': 'string'
            },
        ],
        MessageAction='SUPPRESS',
        DesiredDeliveryMediums=[
            'EMAIL',
        ]
    )

    client.admin_set_user_password(
        UserPoolId=user_pool_id,
        Username=email,
        Password=get_random_string(8),
        Permanent=True
    )
    return user


def create_client(usr: AbstractUser, platform: str, user_group: str, custom: str):
    print("username: ", usr.username, usr.email, usr.cognito_id, user_group)
    print("Creating new client at {} in progress ...".format(platform))
    TOPIC_ARN = os.getenv("PUBLISH_TOPIC_ARN")
    if not TOPIC_ARN:
        raise AttributeError("No topic available in order to publish user {}".format(usr.username))

    event = usr.payload()
    event['platform'] = platform
    event['user_group'] = user_group
    event['custom'] = custom

    client = boto3.client('sns')
    return client.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps({'default': json.dumps(event)}),
        MessageStructure='json'
    )
