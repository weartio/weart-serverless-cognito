import json
import os

import urllib3

def handler(event, context):
    """
    :param event:
    :param context:
    :return:
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_attributes['custom:lastLogin'] = current_time

    return event