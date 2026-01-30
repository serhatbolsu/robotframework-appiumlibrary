import unittest

from AppiumLibrary.utils import ApplicationCache


class ApplicationCacheTests(unittest.TestCase):
    def test_no_current_message(self):
        cache = ApplicationCache()
        with self.assertRaisesRegex(RuntimeError, "No current application"):
            cache.current.anyMember()
