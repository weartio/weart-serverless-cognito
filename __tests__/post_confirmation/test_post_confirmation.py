import json
import os
from unittest import mock
from unittest.mock import patch

from __tests__.utils.extended_test_case import ExtendedTestCase, get_mock_file
from __tests__.utils.mock_api_call import mock_make_api_call

AWS_DEFAULT_REGION = "eu-central-1"
os.environ["AWS_DEFAULT_REGION"] = AWS_DEFAULT_REGION
from src.functions.post_confirmation.handler import handler


class TestEmailAddress(ExtendedTestCase):
    def setUp(self) -> None:
        with open(get_mock_file("post_confirmation",
                                "user_with_email_event")) as json_file:
            self.event = json.load(json_file)

    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call([
               {'operation_name': 'ListUsers', 'returned_data': {'Users': []}}
           ]))
    @patch('src.functions.post_confirmation.handler.create_client')
    def test_new_user(self, mocked_created_client):
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()

    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call([
               {'operation_name': 'ListUsers', 'returned_data': {'Users': [{'Username': "user1"}]}}
           ]))
    @patch('src.functions.post_confirmation.handler.create_client')
    def test_with_multiple_native_accounts(self, mocked_created_client):
        """
        This is an impossible case.
        :return:
        """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'

        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": AWS_DEFAULT_REGION})
class TestMobileNumber(ExtendedTestCase):
    def setUp(self) -> None:
        with open(get_mock_file("post_confirmation", "user_with_phone_number_event")) as json_file:
            self.event = json.load(json_file)

    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call([
               {'operation_name': 'ListUsers', 'returned_data': {'Users': []}}
           ]))
    @patch('src.functions.post_confirmation.handler.create_client')
    def test_new_user(self, mocked_created_client):
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()

    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call([
               {'operation_name': 'ListUsers', 'returned_data': {'Users': [{'Username': "user1"}]}}
           ]))
    @patch('src.functions.post_confirmation.handler.create_client')
    def test_with_multiple_native_accounts(self, mocked_created_client):
        """
        This is an impossible case.
        :return:
        """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'

        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": AWS_DEFAULT_REGION})
class TestGoogleExternalProvider(ExtendedTestCase):
    def setUp(self) -> None:
        with open(get_mock_file("post_confirmation", "user_with_google_event")) as json_file:
            self.event = json.load(json_file)

    @patch('src.functions.post_confirmation.handler.create_client')
    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call(
               [
                   {'operation_name': 'ListUsers', 'returned_data': {'Users': []}},
                   {'operation_name': 'AdminCreateUser', 'returned_data': {'User': {'Username': 'weArt'}}},
                   {'operation_name': 'AdminSetUserPassword', 'returned_data': 'done'},
                   {'operation_name': 'AdminLinkProviderForUser', 'returned_data': 'done'},
                   {'operation_name': 'AdminUpdateUserAttributes', 'returned_data': 'done'}
               ]
           ))
    def test_new_user(self, mocked_created_client):
        """
        When user tries to sign up with google, without previous native account
        :param mocked_created_client:
        :return:
        """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        self.assertEqual(mocked_created_client.call_count, 2)

    @patch('src.functions.post_confirmation.handler.create_client')
    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call(
               [
                   {'operation_name': 'ListUsers', 'returned_data': {'Users': [{'Username': "user1"}]}},
                   {'operation_name': 'AdminCreateUser', 'returned_data': {'User': {'Username': 'weArt'}}},
                   {'operation_name': 'AdminSetUserPassword', 'returned_data': 'done'},
                   {'operation_name': 'AdminLinkProviderForUser', 'returned_data': 'done'},
                   {'operation_name': 'AdminUpdateUserAttributes', 'returned_data': 'done'}
               ]
           ))
    def test_existing_user(self, mocked_created_client):
        """
        When user tries to sign up with google, with existing native account
        :param mocked_created_client:
        :return:
        """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": AWS_DEFAULT_REGION})
class TestAppleExternalProvider(ExtendedTestCase):
    def setUp(self) -> None:
        with open(get_mock_file("post_confirmation", "user_with_apple_event")) as json_file:
            self.event = json.load(json_file)

    @patch('src.functions.post_confirmation.handler.create_client')
    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call(
               [
                   {'operation_name': 'ListUsers', 'returned_data': {'Users': []}},
                   {'operation_name': 'AdminCreateUser', 'returned_data': {'User': {'Username': 'weArt'}}},
                   {'operation_name': 'AdminSetUserPassword', 'returned_data': 'done'},
                   {'operation_name': 'AdminLinkProviderForUser', 'returned_data': 'done'},
                   {'operation_name': 'AdminUpdateUserAttributes', 'returned_data': 'done'}
               ]
           ))
    def test_new_user(self, mocked_created_client):
        """
         When user tries to sign up with apple, without previous native account
         :param mocked_created_client:
         :return:
         """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        self.assertEqual(mocked_created_client.call_count, 2)

    @patch('src.functions.post_confirmation.handler.create_client')
    @patch('botocore.client.BaseClient._make_api_call',
           new=mock_make_api_call(
               [
                   {'operation_name': 'ListUsers', 'returned_data': {'Users': [{'Username': "user1"}]}},
                   {'operation_name': 'AdminCreateUser', 'returned_data': {'User': {'Username': 'weArt'}}},
                   {'operation_name': 'AdminSetUserPassword', 'returned_data': 'done'},
                   {'operation_name': 'AdminLinkProviderForUser', 'returned_data': 'done'},
                   {'operation_name': 'AdminUpdateUserAttributes', 'returned_data': 'done'}
               ]
           ))
    def test_existing_user(self, mocked_created_client):
        """
       When user tries to sign up with apple, with existing native account
       :param mocked_created_client:
       :return:
       """
        mocked_created_client.return_value = 'SNS_MESSAGE_ID'
        response = handler(self.event, None)

        self.assertEqual(sorted(self.event.items()), sorted(response.items()))
        mocked_created_client.assert_called_once()


class TestGeneralCases(ExtendedTestCase):
    def test_with_empty_parameters(self):
        context = None
        event = None

        self.assertRaisesWithMessage(AttributeError, "Event is required!", handler, event, context)
