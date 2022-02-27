import unittest
import json
from unittest.mock import patch
import boto3

from __tests__.utils.extended_test_case import ExtendedTestCase
from __tests__.utils.mock_api_call import mock_make_api_call
from src.functions.post_confirmation.core.users import list_similar_users


class TestPostConfirmation(ExtendedTestCase):

    def test_post_confirmation_with_empty_parameters(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_username_attribute(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_user_pool_id_attribute(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_user_attributes(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_trigger_source(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_platform_parameter(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_custom_user_group_parameter(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_custom_parameter(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_without_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_valid_parameters(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_invalid_trigger_source(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_empty_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_invalid_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_email_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_phone_number_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_google_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_facebook_registration_method(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_new_email(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_new_phone_number(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_existing_email(self):
        self.fail('Not Implemented Yet!')

    def test_post_confirmation_with_existing_phone_number(self):
        self.fail('Not Implemented Yet!')
