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

    def test_go_to_url_without_timeout(self):
        am = _ApplicationManagementKeywords()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        am.open_application('remote_url')
        
        # Mock the methods
        driver = am._current_application()
        driver.get = mock.Mock()
        driver.set_page_load_timeout = mock.Mock()
        
        # Call go_to_url without timeout
        am.go_to_url('http://example.com')
        
        # Verify get was called with the URL
        driver.get.assert_called_once_with('http://example.com')
        
        # Verify set_page_load_timeout was NOT called when timeout is None
        driver.set_page_load_timeout.assert_not_called()

    def test_go_to_url_with_timeout_seconds(self):
        am = _ApplicationManagementKeywords()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        am.open_application('remote_url')
        
        # Mock necessary methods
        driver = am._current_application()
        driver.get = mock.Mock()
        driver.set_page_load_timeout = mock.Mock()
        
        # Create a mock timeouts object
        mock_timeouts = mock.Mock()
        mock_timeouts.page_load = 30000  # 30 seconds in milliseconds
        driver.timeouts = mock_timeouts
        
        # Call go_to_url with timeout in seconds
        am.go_to_url('http://example.com', timeout=10)
        
        # Verify set_page_load_timeout was called with 10 seconds
        self.assertEqual(driver.set_page_load_timeout.call_count, 2)  # Once to set, once to restore
        driver.set_page_load_timeout.assert_any_call(10)
        
        # Verify get was called
        driver.get.assert_called_once_with('http://example.com')

    def test_go_to_url_with_timeout_timestr(self):
        am = _ApplicationManagementKeywords()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        am.open_application('remote_url')
        
        # Mock necessary methods
        driver = am._current_application()
        driver.get = mock.Mock()
        driver.set_page_load_timeout = mock.Mock()
        
        # Create a mock timeouts object
        mock_timeouts = mock.Mock()
        mock_timeouts.page_load = 30000  # 30 seconds in milliseconds
        driver.timeouts = mock_timeouts
        
        # Call go_to_url with timeout as time string
        am.go_to_url('http://example.com', timeout='1 minute')
        
        # Verify set_page_load_timeout was called with 60 seconds
        driver.set_page_load_timeout.assert_any_call(60)
        
        # Verify get was called
        driver.get.assert_called_once_with('http://example.com')

    def test_go_to_url_restores_timeout_on_error(self):
        am = _ApplicationManagementKeywords()
        appium.webdriver.Remote = WebdriverRemoteMock
        am._debug = mock.Mock()
        am.open_application('remote_url')
        
        # Mock necessary methods
        driver = am._current_application()
        driver.get = mock.Mock(side_effect=Exception("Navigation failed"))
        driver.set_page_load_timeout = mock.Mock()
        
        # Create a mock timeouts object
        mock_timeouts = mock.Mock()
        mock_timeouts.page_load = 30000  # 30 seconds in milliseconds
        driver.timeouts = mock_timeouts
        
        # Call go_to_url with timeout - should raise exception but still restore timeout
        with self.assertRaises(Exception):
            am.go_to_url('http://example.com', timeout=10)
        
        # Verify timeout was restored even after error
        self.assertEqual(driver.set_page_load_timeout.call_count, 2)  # Once to set, once to restore
        driver.set_page_load_timeout.assert_any_call(10)  # Initial set
        driver.set_page_load_timeout.assert_any_call(30)  # Restore (30000ms / 1000 = 30s)
