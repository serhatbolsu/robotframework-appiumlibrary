import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

__version__ = VERSION

class AppiumLibrary(
    _LoggingKeywords, 
    _RunOnFailureKeywords, 
    _ElementKeywords, 
    _ScreenshotKeywords,
    _ApplicationManagementKeywords,
):
    """AppiumLibrary is a App testing library for Robot Framework.

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, run_on_failure='Capture Page Screenshot'):
        """AppiumLibrary can be imported with optional arguments.

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a Selenium2Library keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value "Nothing" will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        Examples:
        | Library | AppiumLibrary | run_on_failure=Nothing | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in AppiumLibrary.__bases__:
            base.__init__(self)
        self.register_keyword_to_run_on_failure(run_on_failure)
