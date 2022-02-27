import os
import json
import unittest
from unittest import mock

from __tests__.utils.extended_test_case import ExtendedTestCase
from src.functions.pre_signup.handler import handler


class TestEmailPreSignUp(ExtendedTestCase):
    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_valid_parameters(self):
        context = None

        with open('mock_data/valid_event_email.json') as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_missing_name(self):
        context = None

        with open('mock_data/event_with_missing_name.json') as json_file:
            event = json.load(json_file)

        response = handler(event, context)

        # the response should be the same as the event
        self.assertEqual(sorted(event.items()), sorted(response.items()))

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email"})
    def test_pre_signup_email_with_no_user_group_environment_variable(self):
        context = None

        with open('mock_data/valid_event_email.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(ValueError, "User group is undefined!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_missing_user_group(self):
        context = None

        with open('mock_data/event_with_missing_user_group.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "User Group is required!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_invalid_user_group(self):
        context = None

        with open('mock_data/event_with_invalid_user_group.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(ValueError, "User group is not valid!", handler, event, context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email,phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_with_missing_phone_number_and_email(self):
        context = None

        with open('mock_data/event_with_missing_email_and_phone_number.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Email or Phone number is required!", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "email", "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_empty_parameters(self):
        context = None
        event = None

        self.assertRaisesWithMessage(TypeError, "'NoneType' object is not subscriptable", handler, event,
                                     context)

    @mock.patch.dict(os.environ, {"PLATFORM_ALLOWED_SCOPE": "phone_number",
                                  "USER_GROUPS_ALLOWED": "PROFESSIONAL,HOMEOWNER"})
    def test_pre_signup_email_with_wrong_environment_variable(self):
        context = None
        with open('mock_data/valid_event_email.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "Phone number is required!", handler, event, context)

    def test_pre_signup_with_no_environment_variables(self):
        context = None
        with open('mock_data/valid_event_email.json') as json_file:
            event = json.load(json_file)

        self.assertRaisesWithMessage(AttributeError, "PLATFORM_ALLOWED_SCOPE is required", handler, event,
                                     context)
