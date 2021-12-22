# -*- coding: utf-8 -*-
import base64

from .keywordgroup import KeywordGroup
from selenium.common.exceptions import TimeoutException
from kitchen.text.converters import to_bytes

class _AndroidUtilsKeywords(KeywordGroup):

    # Public
    def open_notifications(self):
        """Opens and expands an Android device's notification drawer.

        Android only.
        """
        driver = self._current_application()
        driver.open_notifications()
        
    def get_network_connection_status(self):
        """Returns an integer bitmask specifying the network connection type.

        Android only.

        See `set network connection status` for more details.
        """
        driver = self._current_application()
        return driver.network_connection

    def set_network_connection_status(self, connectionStatus):
        """Sets the network connection Status.

        Android only.

        Possible values:
            | =Value= | =Alias=          | =Data= | =Wifi= | =Airplane Mode=  |
            |  0      | (None)           | 0      |   0    | 0                |
            |  1      | (Airplane Mode)  | 0      |   0    | 1                |
            |  2      | (Wifi only)      | 0      |   1    | 0                |
            |  4      | (Data only)      | 1      |   0    | 0                |
            |  6      | (All network on) | 1      |   1    | 0                |
        """
        driver = self._current_application()
        return driver.set_network_connection(int(connectionStatus))

    def pull_file(self, path, decode=False):
        """Retrieves the file at `path` and return it's content.

        Android only.

         - _path_ - the path to the file on the device
         - _decode_ - True/False decode the data (base64) before returning it (default=False)
         """
        driver = self._current_application()
        theFile = driver.pull_file(path)
        if decode:
            theFile = base64.b64decode(theFile)
        return str(theFile)

    def pull_folder(self, path, decode=False):
        """Retrieves a folder at `path`. Returns the folder's contents zipped.

        Android only.

         - _path_ - the path to the folder on the device
         - _decode_ - True/False decode the data (base64) before returning it (default=False)
        """
        driver = self._current_application()
        theFolder = driver.pull_folder(path)
        if decode:
            theFolder = base64.b64decode(theFolder)
        return theFolder

    def push_file(self, path, data, encode=False):
        """Puts the data in the file specified as `path`.

        Android only.

         - _path_ - the path on the device
         - _data_ - data to be written to the file
         - _encode_ - True/False encode the data as base64 before writing it to the file (default=False)
        """
        driver = self._current_application()
        data = to_bytes(data)
        if encode:
            data = base64.b64encode(data)
        driver.push_file(path, data)

    def get_activity(self):
        """Retrieves the current activity on the device.

        Android only.

        """
        driver = self._current_application()
        return driver.current_activity

    def start_activity(self, appPackage, appActivity, **opts):
        """Opens an arbitrary activity during a test. If the activity belongs to
        another application, that application is started and the activity is opened.

        Android only.

        - _appPackage_ - The package containing the activity to start.
        - _appActivity_ - The activity to start.
        - _appWaitPackage_ - Begin automation after this package starts (optional).
        - _appWaitActivity_ - Begin automation after this activity starts (optional).
        - _intentAction_ - Intent to start (opt_ional).
        - _intentCategory_ - Intent category to start (optional).
        - _intentFlags_ - Flags to send to the intent (optional).
        - _optionalIntentArguments_ - Optional arguments to the intent (optional).
        - _dontStopAppOnReset_ - Should the app be stopped on reset (optional)?

        """


        # Almost the same code as in appium's start activity,
        # just to keep the same keyword names as in open application

        arguments = {
            'app_wait_package': 'appWaitPackage',
            'app_wait_activity': 'appWaitActivity',
            'intent_action': 'intentAction',
            'intent_category': 'intentCategory',
            'intent_flags': 'intentFlags',
            'optional_intent_arguments': 'optionalIntentArguments',
            'dont_stop_app_on_reset': 'dontStopAppOnReset'
        }

        data = {}

        for key, value in arguments.items():
            if value in opts:
                data[key] = opts[value]

        driver = self._current_application()
        driver.start_activity(app_package=appPackage, app_activity=appActivity, **data)

    def wait_activity(self, activity, timeout, interval=1):
        """Wait for an activity: block until target activity presents
        or time out.

        Android only.

         - _activity_ - target activity
         - _timeout_ - max wait time, in seconds
         - _interval_ - sleep interval between retries, in seconds
        """

        if not activity.startswith('.'):
            activity = ".%s" % activity

        driver = self._current_application()
        if not driver.wait_activity(activity=activity, timeout=float(timeout), interval=float(interval)):
            raise TimeoutException(msg="Activity %s never presented, current activity: %s" % (activity, self.get_activity()))

    def install_app(self, app_path, app_package):
        """ Install App via Appium
        
        Android only.

        - app_path - path to app
        - app_package - package of install app to verify
        """
        driver = self._current_application()
        driver.install_app(app_path)
        return driver.is_app_installed(app_package)
    
    def set_location(self, latitude, longitude, altitude=10):
        """ Set location

        - _latitute_
        - _longitude_
        - _altitude_ = 10 [optional]
        
        Android only.
        New in AppiumLibrary 1.5
        """
        driver = self._current_application()
        driver.set_location(latitude,longitude,altitude)
