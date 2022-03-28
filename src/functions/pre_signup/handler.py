import json
import os
import requests
RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']


def handler(event, context):
    """
    Assign Client To Group lambda function
    :param event:
    :param context:
    :return:
    """
    if not event:
        raise AttributeError('Event is required!')

    print("Event {}".format(json.dumps(event)))

    PLATFORM_ALLOWED_SCOPE = os.getenv("PLATFORM_ALLOWED_SCOPE")
    USER_GROUPS_ALLOWED = os.getenv("USER_GROUPS_ALLOWED")

    if not PLATFORM_ALLOWED_SCOPE:
        raise AttributeError("PLATFORM_ALLOWED_SCOPE is required")

    request = event['request']
    trigger_source = event['triggerSource']
    user_attributes = request['userAttributes']
    scopes = PLATFORM_ALLOWED_SCOPE.split(",")

    if not request:
        raise AttributeError('Request parameter is required!')

    if not request.validation_data:
        raise AttributeError('Missing validation data')

    if not verify_recaptcha(event.request.validation_data.recaptcha_token):
        raise Exception('reCAPTCHA verification failed')
    skip_user_groups_validation = True if not USER_GROUPS_ALLOWED else False

    if not skip_user_groups_validation:
        user_groups_allowed = USER_GROUPS_ALLOWED.split(",")

        user_group = user_attributes.get('custom:user_group', None)
        if not user_group:
            raise AttributeError("User Group is required!")

        if user_group not in user_groups_allowed:
            raise ValueError("User group is not valid!")

    if trigger_source == "PreSignUp_ExternalProvider":
        """Cases are Google, Facebook, Apple"""
        social_media_provider = event['userName'].split("_")[0].lower()
        if social_media_provider not in scopes:
            raise ValueError("{} is not supported as a valid registration method".format(social_media_provider))

    if trigger_source == "PreSignUp_SignUp":
        """Cases are email, phone_number"""
        email = user_attributes.get('email', None)
        phone_number = user_attributes.get('phone_number', None)

        if {'email', 'phone_number'}.issubset(set(scopes)):
            """
            Must have at least email or phone_number
            """
            if phone_number is None and email is None:
                raise AttributeError("Email or Phone number is required!")

        if {'phone_number'}.issubset(set(scopes)) and not {'email'}.issubset(set(scopes)):
            """
            Must have at least email or phone_number
            """
            if phone_number is None:
                raise AttributeError("Phone number is required!")
            else:
                if not (str(phone_number).startswith("+") or str(phone_number).startswith("00")):
                    raise ValueError("Phone number is not valid!")

        if {'email'}.issubset(set(scopes)) and not {'phone_number'}.issubset(set(scopes)):
            """
            Must have at least email or phone_number
            """
            if email is None:
                raise AttributeError("Email address is required!")

    if trigger_source == "PreSignUp_AdminCreateUser":
        pass

    return event


def verify_recaptcha(recaptcha_token):
    payload = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": recaptcha_token
    }
    url = 'https://www.google.com/recaptcha/api/siteverify'
    verify_response = requests.post(url, payload)
    print('verify_response: ', verify_response)
    if not verify_response.status_code == 200:
        return False
    return True
