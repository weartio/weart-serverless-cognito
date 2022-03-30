import json
import os
import sys

import boto3

sys.path.append(os.path.join(os.path.dirname(__file__)))

from core.users import GOOGLE, EMAIL, list_similar_users, create_client, FACEBOOK, APPLE, MOBILE
from core.users.factory import UserFactory


def get_registration_method(user_attributes):
    """
    return user registration method
    :param user_attributes:
    :return:
    """
    if 'phone_number' in user_attributes:
        return MOBILE
    if 'identities' not in user_attributes:
        return EMAIL

    identities = user_attributes['identities']
    identities = json.loads(identities)

    if not identities:
        return EMAIL

    identity = identities[0]
    if 'providerName' not in identity:
        return EMAIL

    if identity['providerName'] == 'Google':
        return GOOGLE

    if identity['providerName'] == 'SignInWithApple':
        return APPLE

    return EMAIL


def assign_user_to_group(client, username, user_group, user_pool_id):
    """
    Assign user to group
    :param client:
    :param username:
    :param user_group:
    :param user_pool_id:
    :return:
    """
    client.admin_add_user_to_group(
        UserPoolId=user_pool_id,
        Username=username,
        GroupName=user_group
    )


def handler(event, context):
    """
    Assign Client To Group lambda function
    :param event:
    :param context:
    :return:
    """
    if event is None:
        raise AttributeError('Event is required!')

    client = boto3.client('cognito-idp')

    print("Event {}".format(json.dumps(event)))
    username = event.get('userName', None)
    user_pool_id = event.get('userPoolId', None)
    user_attributes = event['request'].get('userAttributes', None)
    post_confirmation_type = event.get('triggerSource', None)

    if not username:
        raise AttributeError('Username is required!')

    if not user_pool_id:
        raise AttributeError('UserPoolId is required!')

    if not user_attributes:
        raise AttributeError('UserAttributes is required!')

    if not post_confirmation_type:
        raise AttributeError('Trigger Source is required!')

    # Note: platform, user_group, custom have to be validated at the PreSignup lambda function.
    platform = user_attributes.get('platform', None)
    user_group = user_attributes.get('custom:user_group', None)
    custom = user_attributes.get('custom:custom', None)

    if post_confirmation_type == 'PostConfirmation_ConfirmSignUp':
        registration_method = get_registration_method(user_attributes)
        print("User is trying to register by {}".format(registration_method))
        # Get the correct user instance [Cognito, Google, ..]
        current_user = UserFactory.factory(registration_method, user_attributes, username, user_pool_id)

        # Check if the user has already previous native accounts, in case the user already has email.
        if current_user.email:
            # which simply means for now, if the user is coming from the social media and has email
            previous_registered_users = list_similar_users(client, user_pool_id, current_user.email, username)
            users = current_user.link_accounts(client, user_pool_id, previous_registered_users)

            for usr in users:
                print("Start Sending user {} to boss".format(usr.email))
                create_client(usr, platform, user_group, custom)
        else:
            create_client(current_user, platform, user_group, custom)

    return event


"""
Scenario 1
- new Native user to sign up .. email, password.
- new Native user to sign up .. phone, password.
- new Google user to sign up .. email

- already native user to sign up with Google
    - create new google account and link with the native
    - update the email field at the native
"""
