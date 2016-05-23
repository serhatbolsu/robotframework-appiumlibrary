# -*- coding: utf-8 -*-
import base64

from .keywordgroup import KeywordGroup
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
        return theFile

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
        if encode:
            data = base64.b64encode(data)
        driver.push_file(path, data)
