import json
import os

import urllib3

def handler(event, context):
    """
    :param event:
    :param context:
    :return:
    """
    user_attributes = event['request']['userAttributes']
    email = user_attributes.get('email', None)
    if email:
        user_attributes['email'] = email.lower()

    return event