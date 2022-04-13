import unittest

from __tests__ import TEST_DIRECTORY


class ExtendedTestCase(unittest.TestCase):

    def assertRaisesWithMessage(self, error_type, msg, method, *args, **kwargs):
        try:
            method(*args, **kwargs)
            self.assertFail()
        except Exception as ex:
            self.assertEqual(type(ex), error_type)
            self.assertEqual(str(ex), msg)


def get_mock_file(module, file_name):
    """
    Return the mock file path
    :param module:
    :param file_name:
    :return:
    """
    return """{}/{}/mock_data/{}.json""".format(TEST_DIRECTORY, module, file_name)
