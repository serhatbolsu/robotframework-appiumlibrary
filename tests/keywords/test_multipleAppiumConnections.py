import logging
import sys
import unittest

import appium
import mock
from webdriverremotemock import WebdriverRemoteMock

from AppiumLibrary import _ApplicationManagementKeywords

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)
   
class MultipleAppiumConnectionTests(unittest.TestCase):
    import six
    if six.PY2:
        assertRegex = unittest.TestCase.assertRegexpMatches
        assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

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
        appIndex = self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 1)
        self.am.lock()
        # create 2nd application - alias=MyAppB - index=2
        appIndex = self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # switch to 1st application - alias=MyAppA - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        appIndex = self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyAppC', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')

        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch to 2nd application - alias=MyAppB - index=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppB')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
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
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')
        ## open + close + open again with the same alias (different url etc.) - should succeed
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')        
        self.am.close_application()
        self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')        

    def test_MAC_switchWithAlias_successful(self):
        # switch applications with aliases
        self.assertFalse(self.am._cache.current)
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')        
        # switch to 1st application - alias=MyAppA - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyAppC', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')        
        # switch to 2nd application - alias=MyAppB - index=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppB')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch back to 3nd application - alias=MyAppC - index=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application('MyAppC')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 2)
        self.am.lock()

    def test_MAC_switchWithAlias_failed(self):
        ## switch applications with non-existent aliases
        # switch - no connections open
        self.assertRaisesRegex(RuntimeError, "Non-existing.*MyAppA", self.am.switch_application, 'MyAppA')
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02') 
        # switch to non-existent alias
        self.assertRaisesRegex(RuntimeError, "Non-existing.*MyAppXXX", self.am.switch_application, 'MyAppXXX')

    def test_MAC_switchWithIndex_successful(self):
        # switch applications with indices
        self.assertFalse(self.am._cache.current)
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02') 
        # switch to 1st application - index=1 - appIndex=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(1)
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        self.assertEqual(appIndex, 2)
        self.am.lock()
        # create 3rd application - alias=MyAppC - index=3
        self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyAppC', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')        
        # switch to 2nd application - index=2 - appIndex=3 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(2)
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4733')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice02')
        self.assertEqual(appIndex, 3)
        self.am.lock()
        # switch back to 3nd application - index=3 - appIndex=2 (switch_application returns the previous app index)
        appIndex = self.am.switch_application(appIndex)
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        self.assertEqual(appIndex, 2)
        self.am.lock()

    def test_MAC_switchWithIndex_failed(self):
        # switch applications with non-existent index
        # switch - no connections open
        self.assertRaisesRegex(RuntimeError, "Non-existing.*1", self.am.switch_application, 1)
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02') 
        # switch to non-existent alias
        self.assertRaisesRegex(RuntimeError, "Non-existing.*333", self.am.switch_application, 333)

    def test_MAC_closeApplication_successful(self):
        # switch applications with aliases
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02') 
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
        self.assertRaisesRegex(RuntimeError, "No application is open", self.am.close_application)
        ## execute keywords without any open applications
        self.assertRaisesRegex(RuntimeError, "No application is open", self.am.lock)
        ## execute keywords after close, without switch
        # create 1st application - alias=MyAppA - index=1
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        # create 2nd application - alias=MyAppB - index=2
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02') 
        self.am.close_application()
        self.assertRaisesRegex(RuntimeError, "No application is open", self.am.lock)
        self.am.switch_application(1)
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
        #self.assertRaisesRegex(RuntimeError, "Non-existing.*2", self.am.switch_application, 2)
        #self.assertRaisesRegex(RuntimeError, "Non-existing.*MyAppB", self.am.switch_application, 'MyAppA')
        self.am.switch_application(2)
        self.assertRaisesRegex(RuntimeError, "Application has been closed", self.am.lock)
        

    def test_MAC_switchAndClose_successful(self):
        self.assertFalse(self.am._cache.current)
        # create apps
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')
        self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyApp3', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')
        self.am.switch_application(2)
        self.am.close_application()
        self.am.switch_application(3)
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4743')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice03')
        appIndex = self.am.open_application('http://127.0.0.1:4753/wd/hub', alias='MyAppD', platformName='Android', platformVersion='4.4', deviceName='MyDeviDce04')
        self.assertEqual(appIndex, 4)
        appIndex = self.am.switch_application('MyAppA')
        self.assertRegex(self.am._cache.current._appiumUrl, '127.0.0.1:4723')
        self.assertEqual(self.am._cache.current._desCapa.get('deviceName'), 'MyDevice01')
        
    def test_MAC_closeAll_successful(self):
        # create apps
        self.am.open_application('http://127.0.0.1:4723/wd/hub', alias='MyAppA', platformName='Android', platformVersion='4.4', deviceName='MyDevice01')
        self.am.open_application('http://127.0.0.1:4733/wd/hub', alias='MyAppB', platformName='Android', platformVersion='4.4', deviceName='MyDevice02')
        self.am.open_application('http://127.0.0.1:4743/wd/hub', alias='MyApp3', platformName='Android', platformVersion='4.4', deviceName='MyDevice03')
        self.am.close_all_applications()
        self.assertRaisesRegex(RuntimeError, "No application is open", self.am.lock)
        self.assertRaisesRegex(RuntimeError, "Non-existing.*MyAppA", self.am.switch_application, 'MyAppA')

