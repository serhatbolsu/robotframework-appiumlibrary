# -*- coding: utf-8 -*-

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
    _WaitingKeywords,
    _TouchKeywords,
    _KeyeventKeywords,
	_AndroidUtilsKeywords,
):
    """AppiumLibrary is a App testing library for Robot Framework.

    *Locating elements*

    All keywords in AppiumLibrary that need to find an element on the app
    take an argument, `locator`. By default, when a locator value is provided,
    it is matched against the key attributes of the particular element type.
    For example, `id` and `name` are key attributes to all elements, and
    locating elements is easy using just the `id` as a `locator`. For example::

    Click Element  my_element

    Appium additionally supports some of the _Mobile JSON Wire Protocol_
    (https://code.google.com/p/selenium/source/browse/spec-draft.md?repo=mobile) locator strategies
    It is also possible to specify the approach AppiumLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id or @name attribute |
    | id                | Click Element `|` id=my_element                                | Matches by @id attribute          |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |
    | accessibility_id  | Click Element `|` accessibility_id=t                           |  Accessibility options utilize.   |




    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, run_on_failure='Capture Page Screenshot'):
        """AppiumLibrary can be imported with optional arguments.

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a AppiumLibrary keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        Examples:
        | Library | AppiumLibrary | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in AppiumLibrary.__bases__:
            base.__init__(self)
        self.register_keyword_to_run_on_failure(run_on_failure)
