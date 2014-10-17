import inspect
import logging
import os
import re 
import sys
import unittest
import appium
import mock

from AppiumLibrary.keywords import _ApplicationManagementKeywords

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)

class WebdriverRemoteMock(mock.Mock):
    #def __init__(self, *args, **kwargs):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):
        super(WebdriverRemoteMock, self).__init__()
        self._appiumUrl = command_executor
        self._desCapa = desired_capabilities
        self._dead = False
    
    def _get_child_mock(self, **kwargs):
        return mock.Mock(**kwargs)
    
    # quit() and lock() methods for simulating the situations where applications
    # are called after they have been closed.
    # Needed because of a robot.utils.ConnectionCache manages the closed connections in a weird way
    # - see comments in test_MAC_closeApplication_failed() below
    def quit(self, **kwargs):
        self._dead = True

    def lock(self):
        if self._dead:
            raise RuntimeError('Application has been closed')



    
class MultipleAppiumConnectionTests(unittest.TestCase):
    am=None

    def setUp(self):
        #appium.webdriver.Remote = mock.Mock()
        appium.webdriver.Remote = WebdriverRemoteMock
        self.am = _ApplicationManagementKeywords()
        self.am._debug = mock.Mock()
        # log debug from _ApplicationManagementKeywords to console
        #am._debug = logger.debug
       
    def test_MAC_openApplication_successful(self):
        self.assertFalse(self.am._cache.current)
        #am.open_application(remote_url, platform_name, platform_version, device_name, app, automation_name, app_package, app_activity, app_wait_package, app_wait_activity, alias, bundleid, udid)
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 1)
        self.am.lock()
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # switch to 1st application - alias=MyAppA - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppC')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch to 2nd application - alias=MyAppB - index=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppB')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 3)
        self.am.lock()

    def test_MAC_openApplicationDuplAlias_successful(self):
        self.assertFalse(self.am._cache.current)
        ## open with duplicate alias - should Fail
        # bug/Feature in ConnectionCache? It's possible to add duplicate alias
        # --> old alias is overwritten with the new, however old connection remains open and 
        # is still accessible with the connection index 
        # see https://github.com/robotframework/SSHLibrary/issues/121 
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppA')
        ## open + close + open again with the same alias (different url etc.) - should succeed
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        self.am.close_application()
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppB')

    def test_MAC_switchWithAlias_successful(self):
        # switch applications with aliases
        self.assertFalse(self.am._cache.current)
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        # switch to 1st application - alias=MyAppA - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppC')
        # switch to 2nd application - alias=MyAppB - index=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppB')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch back to 3nd application - alias=MyAppC - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppC')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 2)
        self.am.lock()

    def test_MAC_switchWithAlias_failed(self):
        ## switch applications with non-existent aliases
        # switch - no connections open
        self.assertRaisesRegexp(RuntimeError, "Non-existing.*MyAppA", self.am.switch_application, 'MyAppA')
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        # switch to non-existent alias
        self.assertRaisesRegexp(RuntimeError, "Non-existing.*MyAppXXX", self.am.switch_application, 'MyAppXXX')

    def test_MAC_switchWithIndex_successful(self):
        # switch applications with indices
        self.assertFalse(self.am._cache.current)
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        # switch to 1st application - index=1 - appIndex=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(1)
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppC')
        # switch to 2nd application - index=2 - appIndex=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(2)
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch back to 3nd application - index=3 - appIndex=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(appIndex)
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 2)
        self.am.lock()

    def test_MAC_switchWithIndex_failed(self):
        # switch applications with non-existent index
        # switch - no connections open
        self.assertRaisesRegexp(RuntimeError, "Non-existing.*1", self.am.switch_application, 1)
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        # switch to non-existent alias
        self.assertRaisesRegexp(RuntimeError, "Non-existing.*333", self.am.switch_application, 333)

    def test_MAC_closeApplication_successful(self):
        # switch applications with aliases
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        # close and switch to MyAppA
        self.assertTrue(self.am._cache.current)
        self.am.close_application()
        self.assertFalse(self.am._cache.current)
        appIndex = self.am.switch_application(1)
        self.assertTrue(self.am._cache.current)
        self.assertEqual(appIndex, None)
        
    def test_MAC_closeApplication_failed(self):
        # switch applications with aliases
        ## close application without any open applications
        self.assertRaisesRegexp(RuntimeError, "No application is open", self.am.close_application)
        ## execute keywords without any open applications
        self.assertRaisesRegexp(RuntimeError, "No application is open", self.am.lock)
        ## execute keywords after close, without switch
        # create 1st application - alias=MyAppA - index=1
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        self.am.close_application()
        self.assertRaisesRegexp(RuntimeError, "No application is open", self.am.lock)
        appIndex = self.am.switch_application(1)
        self.am.lock()
        self.am.close_application()
        # verify that the applications are really closed
        # These fail because of ConnectionCache, it has no mechanism for removing a single entry from the cache
        # --> switching to a closed connection does not produce an error, the error comes only when you try to do 
        #     something with the connection
        # BUG: https://github.com/robotframework/SSHLibrary/issues/120
        # Now the WebdriverRemoteMock object, simulates the current situation i.e. it implements 
        #  - the "quit()" method that is used to close the application
        #  - the "lock()" method (=keyword) to simulate a call to a dead connection
        # When fixed, this test should look something like this: 
        #self.assertRaisesRegexp(RuntimeError, "Non-existing.*2", self.am.switch_application, 2)
        #self.assertRaisesRegexp(RuntimeError, "Non-existing.*MyAppB", self.am.switch_application, 'MyAppA')
        appIndex = self.am.switch_application(2)
        self.assertRaisesRegexp(RuntimeError, "Application has been closed", self.am.lock)
        

    def test_MAC_switchAndClose_successful(self):
        self.assertFalse(self.am._cache.current)
        # create apps
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppC')
        appIndex = self.am.switch_application(2)
        self.am.close_application()
        appIndex = self.am.switch_application(3)
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        appIndex = self.am.open_application('http://127.0.0.1:4753/wd/hub', 'Android', '4.4', 'MyDevice04', '', '', alias='MyAppD')
        self.assertEqual(appIndex, 4)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegexpMatches(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        
    def test_MAC_closeAll_successful(self):
        # create apps
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', 'Android', '4.4', 'MyDevice01', '', '', alias='MyAppA')
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', 'Android', '4.4', 'MyDevice02', '', '', alias='MyAppB')
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', 'Android', '4.4', 'MyDevice03', '', '', alias='MyAppC')
        self.am.close_all_applications()
        self.assertRaisesRegexp(RuntimeError, "No application is open", self.am.lock)
        self.assertRaisesRegexp(RuntimeError, "Non-existing.*MyAppA", self.am.switch_application, 'MyAppA')

