# -*- coding: utf-8 -*-

import os
import robot
from robot.errors import DataError
from appium import webdriver
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

    def open_application(self, remote_url, platform_name, platform_version, device_name, app, automation_name=None, app_package=None, app_activity=None, alias=None):
        """Opens a new application to given Appium server.

        | *Option*          | *Man.* | *Description* |
        | remote_url        | Yes    | Appium server url |
        | platform_name     | Yes    | platform name, either "iOS" or "Android" |
        | platform_version  | Yes    | platform version, the mobile OS version you want |
        | device_name       | Yes    | Device name, the kind of device you want, like "iPhone Simulator" |        
        | app               | Yes    | Android/iOS application path |
        | automation_name   | no     | "Selendroid" if you want to use Selendroid, otherwise, this can be omitted |
        | app_package       | no     | Android application package name |
        | app_activity      | no     | Android application activity name |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | iOS | 7.0 | iPhone Simulator | your.app |
        | Open Application | http://localhost:4723/wd/hub | Android | 4.2 | emulator:5554 | OrangeDemoApp.apk | Selendroid | com.test.orangedemo | .MainActivity |
        """
        desired_caps = {}
        desired_caps['platformName'] = platform_name
        desired_caps['platformVersion'] = platform_version
        desired_caps['deviceName'] = device_name
        desired_caps['app'] = app
        desired_caps['automationName'] = automation_name
        # desired_caps['browserName'] = ''
        desired_caps['appPackage'] = app_package
        desired_caps['androidActivity'] = app_activity
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

    def _get_platform(self):
        try:
            platformName = self._current_application().desired_capabilities['desired']['platformName']
        except Exception, e:
            raise Exception, e
        return platformName.lower()

    def _is_platform(self, platform):
        platformName = self._get_platform()
        return platform.lower() == platformName

    def _is_ios(self):
        return self._is_platform('ios')

    def _is_andriod(self):
        return self._is_platform('android')

    def get_source(self):
        """Returns the entire source of the current page."""
        return self._current_application().page_source
    

    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        source = self.get_source()
        self._log(source, loglevel.upper())
        return source