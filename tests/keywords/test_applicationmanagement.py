import unittest
import mock
import appium
from AppiumLibrary.keywords import _ApplicationManagementKeywords
from webdriverremotemock import WebdriverRemoteMock

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
        am.open_application('remote_url', '', '', '', '', '')
        self.assertTrue(am._cache.current)
