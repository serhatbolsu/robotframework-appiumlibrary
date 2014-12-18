# -*- coding: utf-8 -*-

from keywordgroup import KeywordGroup
from appium.webdriver.connectiontype import ConnectionType

class _AndroidUtilsKeywords(KeywordGroup):

    # Public
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
            Value |(Alias)          | Data | Wifi | Airplane Mode
            -------------------------------------------------
            0     |(None)           | 0    | 0    | 0
            1     |(Airplane Mode)  | 0    | 0    | 1
            2     |(Wifi only)      | 0    | 1    | 0
            4     |(Data only)      | 1    | 0    | 0
            6     |(All network on) | 1    | 1    | 0
        """
        driver = self._current_application()
        connType = ConnectionType(int(connectionStatus))
        return driver.set_network_connection(connType)

    def pull_file(self, path):
        """Retrieves the file at `path`. Returns the file's content encoded as
        Base64.
		Android only.

        :Args:
         - path - the path to the file on the device
        """
        driver = self._current_application()
        return driver.pull_file(path)

    def pull_folder(self, path):
        """Retrieves a folder at `path`. Returns the folder's contents zipped
        and encoded as Base64.
		Android only.

        :Args:
         - path - the path to the folder on the device
        """
        driver = self._current_application()
        return driver.pull_folder(path)

    def push_file(self, path, base64data):
        """Puts the data, encoded as Base64, in the file specified as `path`.
		Android only.

        :Args:
         - path - the path on the device
         - base64data - data, encoded as Base64, to be written to the file
        """
        driver = self._current_application()
        driver.push_file(path, base64data)
