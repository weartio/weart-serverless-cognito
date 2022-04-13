import json
import os

import urllib3


def verify_recaptcha(recaptcha_secret_key, recaptcha_token):
    """
    Verify the recaptcha with google
    :param recaptcha_secret_key:
    :param recaptcha_token:
    :return:
    """
    payload = {
        "secret": recaptcha_secret_key,
        "response": recaptcha_token
    }
    url = 'https://www.google.com/recaptcha/api/siteverify'
    http = urllib3.PoolManager()
    verify_response = http.request('POST', url, payload)
    response = json.loads(verify_response.data)

    return 'success' in response


def handler(event, context):
    """
    Assign Client To Group lambda function
    :param event:
    :param context:
    :return:
    """
    RECAPTCHA_SECRET_KEY = os.environ.get('RECAPTCHA_SECRET_KEY', None)
    MOBILE_POOL_CLIENT_ID = os.environ.get('MOBILE_POOL_CLIENT_ID', None)

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
    user_pool_app_client_id = event['callerContext']['clientId']
    scopes = PLATFORM_ALLOWED_SCOPE.split(",")

    # Preconditions:
    # - if the request is coming from mobile, skip captcha validation
    # - if the request is coming from social media, skip the captcha validation

    if not request:
        raise AttributeError('Request parameter is required!')

    skip_captcha_check = user_pool_app_client_id == MOBILE_POOL_CLIENT_ID \
                         or trigger_source == "PreSignUp_ExternalProvider" \
                         or trigger_source == "PreSignUp_AdminCreateUser" \
                         or RECAPTCHA_SECRET_KEY is None

    if not skip_captcha_check:
        if "validationData" not in request or request["validationData"] is None:
            raise AttributeError('Wrong captcha: validationData is missing')

        if "recaptchaToken" not in request["validationData"]:
            raise AttributeError('Wrong captcha: recaptchaToken is missing')

        if not request["validationData"]["recaptchaToken"]:
            raise AttributeError('Wrong captcha: recaptchaToken is not provided')

        validation_data = request["validationData"]["recaptchaToken"]

        if not verify_recaptcha(RECAPTCHA_SECRET_KEY, validation_data):
            raise ValueError('reCAPTCHA verification failed')

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
