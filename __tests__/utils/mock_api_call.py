import botocore

orig = botocore.client.BaseClient._make_api_call


def mock_make_api_call(self, operation_name, kwarg):
    if operation_name == 'ListUsers':
        parsed_response = {'Users': []}
        return parsed_response
    return orig(self, operation_name, kwarg)