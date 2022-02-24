import unittest

class ExtendedTestCase(unittest.TestCase):

  def assertRaisesWithMessage(self, errorType, msg, function, *args, **kwargs):
    try:
      function(*args, **kwargs)
      self.assertFail()
    except Exception as ex:
      self.assertEqual(type(ex), errorType)
      self.assertEqual(str(ex), msg)