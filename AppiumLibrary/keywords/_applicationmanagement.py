# -*- coding: utf-8 -*-

import os
import robot
import inspect
from appium import webdriver
from AppiumLibrary.utils import ApplicationCache
from .keywordgroup import KeywordGroup

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class _ApplicationManagementKeywords(KeywordGroup):
    def __init__(self):
        self._cache = ApplicationCache()
        self._timeout_in_secs = float(5)

    # Public, open and close

    def close_application(self):
        """Closes the current application and also close webdriver session."""
        self._debug('Closing application with session id %s' % self._current_application().session_id)
        self._cache.close()

    def close_all_applications(self):
        """Closes all open applications.

        This keyword is meant to be used in test or suite teardown to
        make sure all the applications are closed before the test execution
        finishes.

        After this keyword, the application indices returned by `Open Application`
        are reset and start from `1`.
        """

        self._debug('Closing all applications')
        self._cache.close_all()

    def open_application(self, remote_url, alias=None, **kwargs):
        """Opens a new application to given Appium server.
        Capabilities of appium server, Android and iOS,
        Please check https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/server-args.md
        | *Option*            | *Man.* | *Description*     |
        | remote_url          | Yes    | Appium server url |
        | alias               | no     | alias             |

        Examples:
        | Open Application | http://localhost:4723/wd/hub | alias=Myapp1         | platformName=iOS      | platformVersion=7.0            | deviceName='iPhone Simulator'           | app=your.app                         |
        | Open Application | http://localhost:4723/wd/hub | platformName=Android | platformVersion=4.2.2 | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk | appPackage=com.netease.qa.orangedemo | appActivity=MainActivity |
        """
        desired_caps = kwargs
        application = webdriver.Remote(str(remote_url), desired_caps)

        self._debug('Opened application with session id %s' % application.session_id)

        return self._cache.register(application, alias)

    def switch_application(self, index_or_alias):
        """Switches the active application by index or alias.

        `index_or_alias` is either application index (an integer) or alias
        (a string). Index is got as the return value of `Open Application`.

        This keyword returns the index of the previous active application,
        which can be used to switch back to that application later.

        Example:
        | ${appium1}=              | Open Application  | http://localhost:4723/wd/hub                   | alias=MyApp1 | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | app=your.app |
        | ${appium2}=              | Open Application  | http://localhost:4755/wd/hub                   | alias=MyApp2 | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | app=your.app |
        | Click Element            | sendHello         | # Executed on appium running at localhost:4755 |
        | Switch Application       | ${appium1}        | # Switch using index                           |
        | Click Element            | ackHello          | # Executed on appium running at localhost:4723 |
        | Switch Application       | MyApp2            | # Switch using alias                           |
        | Page Should Contain Text | ackHello Received | # Executed on appium running at localhost:4755 |

        """
        old_index = self._cache.current_index
        if index_or_alias is None:
            self._cache.close()
        else:
            self._cache.switch(index_or_alias)
        return old_index

    def launch_application(self):
        """ Launch application. Application can be launched while Appium session running.
        This keyword can be used to launch application during test case or between test cases.

        This keyword works while `Open Application` has a test running. This is good practice to `Launch Application`
        and `Quit Application` between test cases. As Suite Setup is `Open Application`, `Test Setup` can be used to `Launch Application`

        Example (syntax is just a representation, refer to RF Guide for usage of Setup/Teardown):
        | [Setup Suite] |
        |  | Open Application | http://localhost:4723/wd/hub | platformName=Android | deviceName=192.168.56.101:5555 | app=${CURDIR}/demoapp/OrangeDemoApp.apk |
        | [Test Setup] |
        |  | Launch Application |
        |  |  | <<<test execution>>> |
        |  |  | <<<test execution>>> |
        | [Test Teardown] |
        |  | Quit Application |
        | [Suite Teardown] |
        |  | Close Application |

        See `Quit Application` for quiting application but keeping Appium sesion running.

        New in AppiumLibrary 1.4.6
        """
        driver = self._current_application()
        driver.launch_app()

    def quit_application(self):
        """ Quit application. Application can be quit while Appium session is kept alive.
        This keyword can be used to close application during test case or between test cases.

        See `Launch Application` for an explanation.

        New in AppiumLibrary 1.4.6
        """
        driver = self._current_application()
        driver.close_app()

    def reset_application(self):
        """ Reset application. Open Application can be reset while Appium session is kept alive.
        """
        driver = self._current_application()
        driver.reset()

    def remove_application(self, application_id):
        """ Removes the application that is identified with an application id

        Example:
        | Remove Application |  com.netease.qa.orangedemo |

        """
        driver = self._current_application()
        driver.remove_app(application_id)

    def get_appium_timeout(self):
        """Gets the timeout in seconds that is used by various keywords.

        See `Set Appium Timeout` for an explanation."""
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_appium_timeout(self, seconds):
        """Sets the timeout in seconds used by various keywords.

        There are several `Wait ...` keywords that take timeout as an
        argument. All of these timeout arguments are optional. The timeout
        used by all of them can be set globally using this keyword.

        The previous timeout value is returned by this keyword and can
        be used to set the old value back later. The default timeout
        is 5 seconds, but it can be altered in `importing`.

        Example:
        | ${orig timeout} = | Set Appium Timeout | 15 seconds |
        | Open page that loads slowly |
        | Set Appium Timeout | ${orig timeout} |
        """
        old_timeout = self.get_appium_timeout()
        self._timeout_in_secs = robot.utils.timestr_to_secs(seconds)
        return old_timeout

    def get_appium_sessionId(self):
        """Returns the current session ID as a reference"""
        self._info("Appium Session ID: " + self._current_application().session_id)
        return self._current_application().session_id

    def get_source(self):
        """Returns the entire source of the current page."""
        return self._current_application().page_source

    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        ll = loglevel.upper()
        if ll == 'NONE':
            return ''
        else:
            if  "run_keyword_and_ignore_error" not in [check_error_ignored[3] for check_error_ignored in inspect.stack()]:
                source = self._current_application().page_source
                self._log(source, ll)
                return source
            else:
                return ''

    def execute_script(self, script):
        """
        Inject a snippet of JavaScript into the page for execution in the
        context of the currently selected frame (Web context only).

        The executed script is assumed to be synchronous and the result
        of evaluating the script is returned to the client.

        New in AppiumLibrary 1.5
        """
        return self._current_application().execute_script(script)

    def execute_async_script(self, script):
        """
        Inject a snippet of Async-JavaScript into the page for execution in the
        context of the currently selected frame (Web context only).

        The executed script is assumed to be asynchronous and must signal that is done by
        invoking the provided callback, which is always provided as the final argument to the
        function.

        The value to this callback will be returned to the client.


        New in AppiumLibrary 1.5
        """
        return self._current_application().execute_async_script(script)

    def go_back(self):
        """Goes one step backward in the browser history."""
        self._current_application().back()

    def lock(self, seconds=5):
        """
        Lock the device for a certain period of time. iOS only.
        """
        self._current_application().lock(robot.utils.timestr_to_secs(seconds))

    def background_app(self, seconds=5):
        """
        Puts the application in the background on the device for a certain
        duration.
        """
        self._current_application().background_app(seconds)

    def touch_id(self, match=True):
        """
        Simulate Touch ID on iOS Simulator

        `match` (boolean) whether the simulated fingerprint is valid (default true)

        New in AppiumLibrary 1.5
        """
        self._current_application().touch_id(match)

    def toggle_touch_id_enrollment(self):
        """
        Toggle Touch ID enrolled state on iOS Simulator

        New in AppiumLibrary 1.5
        """
        self._current_application().toggle_touch_id_enrollment()

    def shake(self):
        """
        Shake the device
        """
        self._current_application().shake()

    def portrait(self):
        """
        Set the device orientation to PORTRAIT
        """
        self._rotate('PORTRAIT')

    def landscape(self):
        """
        Set the device orientation to LANDSCAPE
        """
        self._rotate('LANDSCAPE')

    def get_current_context(self):
        """Get current context."""
        return self._current_application().current_context

    def get_contexts(self):
        """Get available contexts."""
        print(self._current_application().contexts)
        return self._current_application().contexts

    def get_window_height(self):
        """Get current device height.

        Example:
        | ${width}       | Get Window Height |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width           | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['height']

    def get_window_width(self):
        """Get current device width.

        Example:
        | ${width}       | Get Window Height |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width           | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['width']

    def switch_to_context(self, context_name):
        """Switch to a new context"""
        self._current_application().switch_to.context(context_name)

    def go_to_url(self, url):
        """
        Opens URL in default web browser.

        Example:
        | Open Application  | http://localhost:4755/wd/hub | platformName=iOS | platformVersion=7.0 | deviceName='iPhone Simulator' | browserName=Safari |
        | Go To URL         | http://m.webapp.com          |
        """
        self._current_application().get(url)

    def get_capability(self, capability_name):
        """
        Return the desired capability value by desired capability name
        """
        try:
            capability = self._current_application().capabilities[capability_name]
        except Exception as e:
            raise e
        return capability

    # Private

    def _current_application(self):
        if not self._cache.current:
            raise RuntimeError('No application is open')
        return self._cache.current

    def _get_platform(self):
        try:
            platform_name = self._current_application().desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()

    def _is_platform(self, platform):
        platform_name = self._get_platform()
        return platform.lower() == platform_name

    def _is_ios(self):
        return self._is_platform('ios')

    def _is_android(self):
        return self._is_platform('android')

    def _rotate(self, orientation):
        driver = self._current_application()
        driver.orientation = orientation
