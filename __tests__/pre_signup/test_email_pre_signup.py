import json
import os
from unittest import mock

from __tests__.utils.extended_test_case import ExtendedTestCase, get_mock_file
from src.functions.pre_signup.handler import handler

MOBILE_POOL_CLIENT_ID = "mobile-test-pool-client-id"
RECAPTCHA_SECRET_KEY = "RECAPTCHA-SECRET-KEY"


class TestEmailPreSignUp(ExtendedTestCase):

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_valid_parameters(self):
        context = None
        with open(get_mock_file("pre_signup", "valid_event_email")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_missing_name(self):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_name")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_no_user_group_environment_variable(self):
        context = None

        with open(get_mock_file("pre_signup", "valid_event_email")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_missing_user_group(self):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_user_group")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "User Group is required!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_invalid_user_group(self):
        context = None

        with open(get_mock_file("pre_signup", "event_with_invalid_user_group")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(ValueError, "User group is not valid!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email,phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_with_missing_phone_number_and_email(self):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_email_and_phone_number")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Email or Phone number is required!", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_empty_parameters(self):
        context = None
        event = None

        self.assertRaisesWithMessage(AttributeError, "Event is required!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_pre_signup_email_with_wrong_environment_variable(self):
        context = None
        with open(get_mock_file("pre_signup", "valid_event_email")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Phone number is required!", handler, event, context)

    def test_pre_signup_with_no_environment_variables(self):
        context = None
        with open(get_mock_file("pre_signup", "valid_event_email")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "PLATFORM_ALLOWED_SCOPE is required", handler, event,
                                     context)


@mock.patch('src.functions.pre_signup.handler.verify_recaptcha', return_value=True)
@mock.patch.dict({"RECAPTCHA_SECRET_KEY": RECAPTCHA_SECRET_KEY})
class TestRecaptchaPreSignUp(ExtendedTestCase):

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_missing_validation_data(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "web_missing_validation_data")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Wrong captcha: validationData is missing", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID})
    def test_missing_validation_data(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "web_valid_recaptcha_token")) as json_file:
            event = json.load(json_file)
        response = handler(event, context)

        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID,
                                  "RECAPTCHA_SECRET_KEY": RECAPTCHA_SECRET_KEY})
    def test_not_provided_recaptcha_token(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "web_not_provided_recaptcha_token")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Wrong captcha: recaptchaToken is not provided", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER",
                                  "MOBILE_POOL_CLIENT_ID": MOBILE_POOL_CLIENT_ID,
                                  "RECAPTCHA_SECRET_KEY": RECAPTCHA_SECRET_KEY})
    def test_missing_recaptcha_token(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "web_missing_recaptcha_token")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Wrong captcha: recaptchaToken is missing", handler, event,
                                     context)
