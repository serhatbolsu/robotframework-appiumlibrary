# -*- coding: utf-8 -*-
import base64

from .keywordgroup import KeywordGroup
from selenium.common.exceptions import TimeoutException
from kitchen.text.converters import to_bytes
from robot.api import logger


class _AndroidUtilsKeywords(KeywordGroup):
    def open_notifications(self):
        """Opens and expands an Android device's notification drawer.

        *Android only.*
        """
        driver = self._current_application()
        driver.open_notifications()

    def get_network_connection_status(self):
        """Returns an integer bitmask specifying the network connection type.\n

        *Android only.*

        See `set network connection status` for more details.
        """
        driver = self._current_application()
        return driver.network_connection

    def set_network_connection_status(self, connectionStatus):
        """Sets the network connection status.\n

        *Android only.*

        Args:
         - ``connectionStatus``: depending on what the network connection should be set to,
         choose one of the values below.

        Possible values:
            | =Value= | =Alias=          | =Data= | =Wifi= | =Airplane Mode=  |
            |  0      | (None)           | 0      |   0    | 0                |
            |  1      | (Airplane Mode)  | 0      |   0    | 1                |
            |  2      | (Wifi only)      | 0      |   1    | 0                |
            |  4      | (Data only)      | 1      |   0    | 0                |
            |  6      | (All network on) | 1      |   1    | 0                |

        Example:
        | Set Network Connection Status | 1 |
        """
        driver = self._current_application()
        return driver.set_network_connection(int(connectionStatus))

    def pull_file(self, path, decode=False):
        """Retrieves the file at ``path`` and returns its content.\n

        *Android only.*

        Args:
         - ``path`` - the path to the file on the device
         - ``decode`` - should be set to True/False to decode the data (base64) before returning it (default=False)

        Example:
        | ${file_content} | Pull File | /sdcard/downloads/file.extension |
         """
        driver = self._current_application()
        theFile = driver.pull_file(path)
        if decode:
            theFile = base64.b64decode(theFile)
        return str(theFile)

    def pull_folder(self, path, decode=False):
        """Retrieves a folder at ``path`` and returns its zipped content.\n

        *Android only.*

        Args:
         - ``path`` - the path to the folder on the device
         - ``decode`` - True/False decode the data (base64) before returning it (default=False)
        
        Example:
        | ${folder_content} | Pull Folder | /sdcard/downloads/files |
        """
        driver = self._current_application()
        theFolder = driver.pull_folder(path)
        if decode:
            theFolder = base64.b64decode(theFolder)
        return theFolder

    def push_file(self, path, data, encode=False):
        """Puts the data in the file specified as ``path``.\n

        *Android only.*
    
        Args:
         - ``path`` - the path on the device
         - ``data`` - data to be written to the file
         - ``encode`` - should be set to True/False to encode the data as base64 before writing it to the file (default=False)
        
        Example:
        | Push File | /sdcard/downloads/file.extension | ${data} |
        """
        driver = self._current_application()
        data = to_bytes(data)
        if encode:
            data = base64.b64encode(data).decode('utf-8')
        driver.push_file(path, data)

    def delete_file(self, path, timeout=5000, include_stderr=True):
        """Deletes the file specified as ``path``.\n

        *Android only.*

        Args:
         - ``path`` - the path on the device
         - ``timeout`` - delete command timeout
         - ``includeStderr`` - whether exception will be thrown if the command's
                            return code is not zero
        Example:
        | Delete File | /sdcard/downloads/file.extension |
        """
        driver = self._current_application()
        driver.execute_script('mobile: shell', {
            'command': 'rm',
            'args': [path],
            'includeStderr': include_stderr,
            'timeout': timeout
        })

    def get_activity(self):
        """Retrieves the current activity on the device.\n

        *Android only.*
        """
        driver = self._current_application()
        return driver.current_activity

    def wait_activity(self, activity, timeout, interval=1):
        """Waits for an activity: blocks until target activity presents or until the timeout is reached.\n

        *Android only.*

        Args:
         - ``activity`` - target activity
         - ``timeout`` - max wait time, in seconds
         - ``interval`` - sleep interval between retries, in seconds
        """
        driver = self._current_application()
        if not driver.wait_activity(activity=activity, timeout=float(timeout), interval=float(interval)):
            raise TimeoutException(msg="Activity %s never presented, current activity: %s" % (activity, self.get_activity()))

    def install_app(self, app_path, app_package):
        """ Installs the app via appium.\n

        *Android only.*
    
        Args:
        - ``app_path`` - path to app
        - ``app_package`` - package of install app to verify
        """
        driver = self._current_application()
        driver.install_app(app_path)
        return driver.is_app_installed(app_package)

    def set_location(self, latitude, longitude, altitude=10):
        """ Sets the location.\n

        *Android only.*
    
        Args:
        - ``latitute``
        - ``longitude``
        - ``altitude`` = 10 [optional]
        """
        driver = self._current_application()
        driver.set_location(latitude,longitude,altitude)

    def start_activity(self, appPackage, appActivity, **opts):
        """ Starts the given activity intent. It invokes the `am start/ am start-activity` command under the hood.
        This keyword extends the functionality of the Start Activity app management API.
        The intent is built with the ``appPackage`` and ``appActivity``.

        *Android only.*

        Args:
         - ``appPackage`` - package of install app to verify
         - ``appActivity`` - activity that should be launched
         - ``user`` - the user ID for which the service is started (the current user is used by default)
         - ``wait`` - set to true if you want to block the method call until the Activity Manager's process returns the control to the system
         - ``stop`` - set to true to force stop the target app before starting the activity
         - ``windowingMode`` - the windowing mode to launch the activity into
         - ``activityType`` - the activity type to launch the activity as
         - ``action`` - action name (actual value for the Activity Manager's `-a` argument)
         - ``uri`` - unified resource identifier (actual value for the Activity Manager's `-d` argument)
         - ``mimeType`` - the actual value for the Activity Manager's `-t` argument
         - ``identifier`` - optional identifier (actual value for the Activity Manager's `-i` argument)
         - ``categories`` - one or more category names (actual value for the Activity Manager's `-c` argument)
         - ``component`` - component name (actual value for the Activity Manager's `-n` argument)
         - ``package`` - package name (actual value for the Activity Manager's `-p` argument)
         - ``extras`` - optional intent arguments, must be represented as an array of arrays, where each subarray item contains two or three string items: value type, key and the value itself
         - ``flags`` - intent startup-specific flags as a hexadecimal string

        For more information please refer to https://github.com/appium/appium-uiautomator2-driver/blob/master/README.md#mobile-startactivity.

        Example:
        | Start Activity | com.google.android.deskclock | com.android.deskclock.DeskClock |
        """
        
        arguments = {
            'user':'user',
            'wait': 'wait',
            'stop' : 'stop',
            'windowingMode': 'windowingMode',
            'activityType': 'activityType',
            'action': 'action',
            'uri': 'uri',
            'mimeType': 'mimeType',
            'identifier': 'identifier',
            'categories': 'categories',
            'component' : 'component',
            'package': 'package',
            'extras': 'extras',
            'flags':'flags'
        }

        data = {}

        data['intent'] = f"{appPackage}/{appActivity}"

        invalid_args = [key for key in opts.keys() if key not in arguments]
        if invalid_args:
            logger.warn(f"Invalid optional arguments passed: {', '.join(invalid_args)}. These will be ignored. ")

        for key, value in arguments.items():
            if value in opts:
                data[key] = opts[value]
    
        driver = self._current_application()
        driver.execute_script('mobile: startActivity', data)
