import unittest

import appium
import mock
from webdriverremotemock import WebdriverRemoteMock

from AppiumLibrary import _ApplicationManagementKeywords


class ApplicationManagementKeywordsTests(unittest.TestCase):

    def test_close_application_clean_cache_sucessful(self):
        am = _ApplicationManagementKeywords()
        application = mock.Mock()
        am._debug = mock.Mock()
        self.assertFalse(am._cache.current)
        am._cache.register(application, 'alias')
        self.assertTrue(am._cache.current)      

        am.close_application()
        self.assertFalse(am._cache.current)


    def test_open_application_register_sucessful(self):
        am = _ApplicationManagementKeywords()
        #appium.webdriver.Remote = mock.Mock()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        self.assertFalse(am._cache.current)
        am.open_application('remote_url')
        self.assertTrue(am._cache.current)

    def test_switch_application(self):
        am = _ApplicationManagementKeywords()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        self.assertFalse(am._cache.current)
        self.assertEqual(1, am.open_application('remote_url1', alias='app1'))
        self.assertEqual(2, am.open_application('remote_url1', alias='app2'))
        self.assertEqual(2, am._cache.current_index)
        am.switch_application('app1')
        self.assertEqual(1, am._cache.current_index)
        am.switch_application(2)
        self.assertEqual(2, am._cache.current_index)
        self.assertEqual(2, am.switch_application(None))
