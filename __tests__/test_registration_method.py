import json
import os

from __tests__.utils.extended_test_case import ExtendedTestCase, get_mock_file

AWS_DEFAULT_REGION = "eu-central-1"
os.environ["AWS_DEFAULT_REGION"] = AWS_DEFAULT_REGION

from src.functions.post_confirmation.core.users import EMAIL, MOBILE, GOOGLE, APPLE
from src.functions.post_confirmation.handler import get_registration_method


class TestRegistrationMethod(ExtendedTestCase):
    def test_email(self):
        with open(get_mock_file("post_confirmation", "user_with_email_event")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, EMAIL)

    def test_phone_number(self):
        with open(get_mock_file("post_confirmation", "user_with_phone_number_event")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, MOBILE)

    def test_google(self):
        with open(get_mock_file("post_confirmation", "user_with_google_event")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, GOOGLE)

    def test_apple(self):
        with open(get_mock_file("post_confirmation", "user_with_apple_event")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, APPLE)

    def test_missing_identities_attribute_should_return_email(self):
        with open(get_mock_file("post_confirmation", "valid_event")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, EMAIL)

    def test_provider_name_is_missing_should_return_email(self):
        with open(get_mock_file("post_confirmation", "event_with_missing_provider_name")) as json_file:
            event = json.load(json_file)

            user_attributes = event['request'].get('userAttributes', None)

            response = get_registration_method(user_attributes)

            self.assertEqual(response, EMAIL)
