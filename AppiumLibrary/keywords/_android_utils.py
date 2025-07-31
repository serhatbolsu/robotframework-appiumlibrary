# -*- coding: utf-8 -*-
import base64

from .keywordgroup import KeywordGroup
from selenium.common.exceptions import TimeoutException
from kitchen.text.converters import to_bytes

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
         - connectionStatus: depending on what the network connection should be set to,
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
        """Retrieves the file at `path` and returns its content.\n

        *Android only.*

        Args:
         - _path_ - the path to the file on the device
         - _decode_ - should be set to True/False to decode the data (base64) before returning it (default=False)

        Example:
        | ${file_content} | Pull File | /sdcard/downloads/file.extension |
         """
        driver = self._current_application()
        theFile = driver.pull_file(path)
        if decode:
            theFile = base64.b64decode(theFile)
        return str(theFile)

    def pull_folder(self, path, decode=False):
        """Retrieves a folder at `path` and returns its zipped content.\n

        *Android only.*

        Args:
         - _path_ - the path to the folder on the device
         - _decode_ - True/False decode the data (base64) before returning it (default=False)
        
        Example:
        | ${folder_content} | Pull Folder | /sdcard/downloads/files |
        """
        driver = self._current_application()
        theFolder = driver.pull_folder(path)
        if decode:
            theFolder = base64.b64decode(theFolder)
        return theFolder

    def push_file(self, path, data, encode=False):
        """Puts the data in the file specified as `path`.\n

        *Android only.*
    
        Args:
         - _path_ - the path on the device
         - _data_ - data to be written to the file
         - _encode_ - should be set to True/False to encode the data as base64 before writing it to the file (default=False)
        
        Example:
        | Push File | /sdcard/downloads/file.extension | ${data}
        """
        driver = self._current_application()
        data = to_bytes(data)
        if encode:
            data = base64.b64encode(data).decode('utf-8')
        driver.push_file(path, data)

    def delete_file(self, path, timeout=5000, include_stderr=True):
        """Deletes the file specified as `path`.\n

        *Android only.*

        Args:
         - _path_ - the path on the device
         - _timeout_ - delete command timeout
         - _includeStderr_ - whether exception will be thrown if the command's
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
         - _activity_ - target activity
         - _timeout_ - max wait time, in seconds
         - _interval_ - sleep interval between retries, in seconds
        """
        driver = self._current_application()
        if not driver.wait_activity(activity=activity, timeout=float(timeout), interval=float(interval)):
            raise TimeoutException(msg="Activity %s never presented, current activity: %s" % (activity, self.get_activity()))

    def install_app(self, app_path, app_package):
        """ Installs the app via appium.\n

        *Android only.*
    
        Args:
        - app_path - path to app
        - app_package - package of install app to verify
        """
        driver = self._current_application()
        driver.install_app(app_path)
        return driver.is_app_installed(app_package)

    def set_location(self, latitude, longitude, altitude=10):
        """ Sets the location.\n

        *Android only.*
    
        Args:
        - _latitute_
        - _longitude_
        - _altitude_ = 10 [optional]
        """
        driver = self._current_application()
        driver.set_location(latitude,longitude,altitude)
