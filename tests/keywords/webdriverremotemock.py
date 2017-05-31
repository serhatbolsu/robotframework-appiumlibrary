import logging
import sys
import unittest
import mock
import base64

logger = logging.getLogger()
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
stream_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(stream_handler)

class WebdriverRemoteMock(mock.Mock, unittest.TestCase):
    #def __init__(self, *args, **kwargs):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):
        super(WebdriverRemoteMock, self).__init__()
        self._appiumUrl = command_executor
        self._desCapa = desired_capabilities
        self._dead = False
        self._myData = ''
        #logger.debug(desired_capabilities)
        for key in desired_capabilities:
            self.assertNotEqual(desired_capabilities[key], None, 'Null value in desired capabilities')
      
    def _get_child_mock(self, **kwargs):
        return mock.Mock(**kwargs)
    
    # quit() and lock() methods for simulating the situations where applications
    # are called after they have been closed.
    # Needed because of a robot.utils.ConnectionCache manages the closed connections in a weird way
    # - see comments in test_MAC_closeApplication_failed() below
    def quit(self, **kwargs):
        self._dead = True

    def lock(self, seconds=5):
        if self._dead:
            raise RuntimeError('Application has been closed')

    def pull_file(self, path, decode=False):
        theFile = self._myData
        if decode:
            theFile = base64.b64decode(theFile)
        return theFile

    def push_file(self, path, data, encode=False):
        if encode:
            self._myData = base64.b64decode(data)
        else:
            self._myData = data

    
