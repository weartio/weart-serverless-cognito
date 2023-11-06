import json
import os
from datetime import datetime
import urllib3

def handler(event, context):
    """
    :param event:
    :param context:
    :return:
    """
    try:
        user_attributes = event['request']['userAttributes']
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_attributes['custom:lastLogin'] = current_time
    except:
        pass

    return event