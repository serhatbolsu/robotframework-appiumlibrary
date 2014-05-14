import unittest
import os
from AppiumLibrary.utils import ApplicationCache


class ApplicationCacheTests(unittest.TestCase): 

    def test_no_current_message(self):
        cache = ApplicationCache()
        try:
            self.assertRaises(RuntimeError, cache.current.anyMember())
        except RuntimeError as e:
            self.assertEqual(e.message, "No current application")