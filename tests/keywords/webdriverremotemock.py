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
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub', options=None, client_config=None, **kwargs):
        super(WebdriverRemoteMock, self).__init__()
        self._appiumUrl = command_executor
        self._options = options
        self._client_config = client_config
        self._dead = False
        self._myData = ''
        # Extract capabilities from options for backward compatibility with tests
        self._desCapa = {}
        if options is not None:
            caps = options.to_capabilities() if hasattr(options, 'to_capabilities') else {}
            self._desCapa = caps
            for key, value in caps.items():
                self.assertNotEqual(value, None, 'Null value in capabilities')
      
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

    
