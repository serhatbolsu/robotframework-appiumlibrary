# -*- coding: utf-8 -*-

import os
from AppiumLibrary.keywords import *
from AppiumLibrary.version import VERSION

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
    """AppiumLibrary is a Mobile App testing library for Robot Framework.

    = Locating or specifying elements =

    All keywords in AppiumLibrary that need to find an element on the page
    take an argument, either a ``locator`` or a ``webelement``. ``locator``
    is a string that describes how to locate an element using a syntax
    specifying different location strategies. ``webelement`` is a variable that
    holds a WebElement instance, which is a representation of the element.

    == Using locators ==

    By default, when a locator is provided, it is matched against the key attributes
    of the particular element type. For iOS and Android, key attribute is ``id`` for
    all elements and locating elements is easy using just the ``id``. For example:

    | Click Element    id=my_element

    New in AppiumLibrary 1.4, ``id`` and ``xpath`` are not required to be specified,
    however ``xpath`` should start with ``//`` else just use ``xpath`` locator as explained below.

    For example:

    | Click Element    my_element
    | Wait Until Page Contains Element    //*[@type="android.widget.EditText"]


    Appium additionally supports some of the [https://w3c.github.io/webdriver/webdriver-spec.html|Mobile JSON Wire Protocol] locator strategies.
    It is also possible to specify the approach AppiumLibrary should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy*        | *Example*                                                      | *Description*                     | *Note*                      |
    | identifier        | Click Element `|` identifier=my_element                        | Matches by @id attribute          |                             |
    | id                | Click Element `|` id=my_element                                | Matches by @resource-id attribute |                             |
    | accessibility_id  | Click Element `|` accessibility_id=button3                     | Accessibility options utilize.    |                             |
    | xpath             | Click Element `|` xpath=//UIATableView/UIATableCell/UIAButton  | Matches with arbitrary XPath      |                             |
    | class             | Click Element `|` class=UIAPickerWheel                         | Matches by class                  |                             |
    | android           | Click Element `|` android=UiSelector().description('Apps')     | Matches by Android UI Automator   |                             |
    | ios               | Click Element `|` ios=.buttons().withName('Apps')              | Matches by iOS UI Automation      |                             |
    | css               | Click Element `|` css=.green_button                            | Matches by css in webview         |                             |
    | name              | Click Element `|` name=my_element                              | Matches by @name attribute        | *Only valid* for Selendroid |

    == Using webelements ==

    Starting with version 1.4 of the AppiumLibrary, one can pass an argument
    that contains a WebElement instead of a string locator. To get a WebElement,
    use the new `Get WebElements` or `Get WebElement` keyword.

    For example:
    | @{elements}    Get Webelements    class=UIAButton
    | Click Element    @{elements}[2]

    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5, run_on_failure='Capture Page Screenshot'):
        """AppiumLibrary can be imported with optional arguments.

        ``timeout`` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Appium Timeout`.

        ``run_on_failure`` specifies the name of a keyword (from any available
        libraries) to execute when a AppiumLibrary keyword fails.

        By default `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value `No Operation` will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        Examples:
        | Library | AppiumLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | AppiumLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in AppiumLibrary.__bases__:
            base.__init__(self)
        self.set_appium_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)
