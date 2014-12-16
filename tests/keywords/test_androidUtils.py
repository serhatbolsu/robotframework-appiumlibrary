import logging
import sys
import unittest
import appium
import mock

from AppiumLibrary.keywords import _ApplicationManagementKeywords
from webdriverremotemock import WebdriverRemoteMock
from AppiumLibrary.keywords import _AndroidUtilsKeywords


logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)
   
class AndroidUtilsTests(unittest.TestCase):
    am=None
    au=None

    def tearDown(self):
        self.am.close_all_applications()

    def setUp(self):
        self.am = _ApplicationManagementKeywords()
        self.am._debug = mock.Mock()
        # Uncomment to use Mock / Comment to test against real appium instance
        #appium.webdriver.Remote = WebdriverRemoteMock
        # log debug from _ApplicationManagementKeywords to console
        self.am._debug = logger.debug
        self.am.open_application('http://10.1.160.124:4724/wd/hub', alias='MsB1', deviceName='MsB1', udid='d81e91ba', platformVersion='4.4', appPackage='com.android.contacts', platformName='Android', appActivity='.activities.DialtactsActivity')    
        self.au = _AndroidUtilsKeywords()
        self.au._current_application = self.am._current_application

    def test_set_network_connection_status(self):
        self.au.set_network_connection_status(4)

    def test_get_network_connection_status(self):
        self.au.get_network_connection_status()

