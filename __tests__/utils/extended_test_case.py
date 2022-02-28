import unittest


class ExtendedTestCase(unittest.TestCase):

    def assertRaisesWithMessage(self, error_type, msg, method, *args, **kwargs):
        try:
            method(*args, **kwargs)
            self.assertFail()
        except Exception as ex:
            self.assertEqual(type(ex), error_type)
            self.assertEqual(str(ex), msg)
