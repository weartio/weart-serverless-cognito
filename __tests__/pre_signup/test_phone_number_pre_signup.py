import json
import os
from unittest import mock

from __tests__.utils.extended_test_case import ExtendedTestCase, get_mock_file
from src.functions.pre_signup.handler import handler


@mock.patch('src.functions.pre_signup.handler.verify_recaptcha', return_value=True)
class TestPhoneNumberPreSignUp(ExtendedTestCase):
    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email,phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_with_missing_phone_number_and_email(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_email_and_phone_number")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Email or Phone number is required!", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_valid_parameters(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "valid_event_phone_number")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_missing_name(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_name")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number"})
    def test_pre_signup_email_with_no_user_group_environment_variable(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "valid_event_phone_number")) as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_missing_user_group(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "event_with_missing_user_group")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "User Group is required!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_invalid_user_group(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "event_with_invalid_user_group")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(ValueError, "User group is not valid!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_invalid_phone_number(self, verify_recaptcha):
        context = None

        with open(get_mock_file("pre_signup", "event_with_invalid_phone_number")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(ValueError, "Phone number is not valid!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_phone_with_wrong_environment_variable(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "valid_event_phone_number")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Email address is required!", handler, event, context)

    def test_pre_signup_with_no_environment_variables(self, verify_recaptcha):
        context = None
        with open(get_mock_file("pre_signup", "valid_event_email")) as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "PLATFORM_ALLOWED_SCOPE is required", handler, event,
                                     context)
