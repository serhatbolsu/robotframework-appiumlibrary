import os
import robot
from robot.errors import DataError
from selenium import webdriver
from AppiumLibrary.utils import ApplicationCache
from keywordgroup import KeywordGroup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class _ApplicationManagementKeywords(KeywordGroup):

    def __init__(self):
        self._cache = ApplicationCache()

    # Public, open and close

    def close_application(self):
        """Closes the current application."""
        if self._cache.current:
            self._debug('Closing application with session id %s'
                        % self._cache.current.session_id)
            self._cache.close()

    def open_application(self, remote_url, device, version, app, app_package=None, app_activity=None, alias=None):
        """Opens a new application to given Appium server.

        | Option     | Man. | Description |
        | remote_url | Yes  | Appium server url |
        | device     | Yes  | Device id |
        | version    | Yes  | sdk version |
        | app        | Yes  | Android/iOS application |
        | app_package | no | Android application package name |
        | app_activity | no | Android application activity name |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | emulator:5554 | OrangeDemoApp.apk | com.test.orangedemo | .MainActivity |
        """
        desired_caps = {}
        desired_caps['browserName'] = ''
        #TODO get platform
        desired_caps['platform'] = 'Mac'
        desired_caps['device'] = device
        desired_caps['version'] = version
        desired_caps['app'] = app
        desired_caps['app-package'] = app_package
        desired_caps['app-activity'] = app_activity
        desired_caps['takesScreenshot'] = 'true'
    
        application = webdriver.Remote(str(remote_url), desired_caps)
        
        self._debug('Opened application with session id %s' % application.session_id)
        
        return self._cache.register(application, alias)

    def _go_back(self):
        """Simulates the user clicking the "back" button on their browser."""
        self._current_application().back()

    def _current_application(self):
        if not self._cache.current:
            raise RuntimeError('No application is open')
        return self._cache.current

    def _parse_capabilities_string(self, capabilities_string):
        '''parses the string based desired_capabilities which should be in the form
        key1:val1,key2:val2
        '''
        desired_capabilities = {}

        if not capabilities_string:
            return desired_capabilities

        for cap in capabilities_string.split(","):
            (key, value) = cap.split(":")
            desired_capabilities[key.strip()] = value.strip()

        return desired_capabilities
    
