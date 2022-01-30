import http.client
import json
import os


def handler(event, context):
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

    url = 'hooks.slack.com'
    print(SLACK_WEBHOOK_URL)
    message = event['Records'][0]['Sns']['Message']
    message_object = json.loads(message)
    message = """New user has registered.
    Email:\t{}
    Phone Number:\t{}
    Username:\t{}
    CogId:\t{}
    UserPoolId:\t{} """.format(message_object['email'], message_object['phone_number'], message_object['username'],
                               message_object['cognito_id'], message_object['user_pool_id'])

    connection = http.client.HTTPSConnection(url)
    connection.request('POST', '/services/{}'.format(SLACK_WEBHOOK_URL),
                       body=json.dumps({"text": message}),
                       headers={'Content-Type': 'application/json'})
    response = connection.getresponse()
    print(response.read().decode())
