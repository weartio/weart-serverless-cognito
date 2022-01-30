import json


def handler(event, context):
    """
    Assign Client To Group lambda function
    :param event:
    :param context:
    :return:
    """
    print("Event {}".format(json.dumps(event)))
    return event
