import boto3
import botocore

orig = botocore.client.BaseClient._make_api_call


def _mock_make_api_call(operations):
    def inner(self, operation_name, kwarg):
        for operation in operations:
            if operation['operation_name'] == operation_name:
                parsed_response = operation['returned_data']  # {'Users': []}
                return parsed_response

        return orig(self, operation_name, kwarg)

    return inner


def mock_make_api_call(operations):
    return _mock_make_api_call(operations=operations)
