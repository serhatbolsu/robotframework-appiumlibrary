import unittest

from AppiumLibrary.utils import ApplicationCache


class ApplicationCacheTests(unittest.TestCase):
    import six
    if six.PY2:
        assertRegex = unittest.TestCase.assertRegexpMatches
        assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

    def test_no_current_message(self):
        cache = ApplicationCache()
        with self.assertRaisesRegex(RuntimeError, "No current application"):
            cache.current.anyMember()
