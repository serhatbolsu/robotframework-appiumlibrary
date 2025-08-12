import time
import robot
from .keywordgroup import KeywordGroup


class _WaitingKeywords(KeywordGroup):
    
    def __init__(self):
        self._sleep_between_wait = 0.2
        
    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        """Waits until the element specified by the ``locator`` is visible.

        Fails if the ``timeout`` expires before the element becomes visible. See the
        `introduction` for more information about the ``timeout`` and its
        default value.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`, `Wait Until Page Contains 
        Element`, `Wait For Condition` and BuiltIn keyword `Wait Until Keyword
        Succeeds`.
        """
        def check_visibility():
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))
        self._wait_until_no_error(timeout, check_visibility)

    def wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until the ``text`` appears on the current page.

        Fails if the ``timeout`` expires before the text appears. See the
        `introduction` for more information about the ``timeout`` and its
        default value.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Does Not Contain`,
        `Wait Until Page Contains Element`,
        `Wait Until Page Does Not Contain Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Text '%s' did not appear in <TIMEOUT>" % text
        self._wait_until(timeout, error, self._is_text_present, text)

    def wait_until_page_does_not_contain(self, text, timeout=None, error=None):
        """Waits until the ``text`` disappears from the current page.

        Fails if the ``timeout`` expires before the ``text`` disappears. See the
        `introduction` for more information about ``timeout`` and its
        default value.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Contains Element`,
        `Wait Until Page Does Not Contain Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """

        def check_present():
            present = self._is_text_present(text)
            if not present:
                return
            else:
                return error or "Text '%s' did not disappear in %s" % (text, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_present)

    def wait_until_page_contains_element(self, locator, timeout=None, error=None):
        """Waits until the element specified by the ``locator`` appears on the current page.

        Fails if the ``timeout`` expires before the element appears. See the
        `introduction` for more information about the ``timeout`` and its
        default value.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)

    def wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
        """Waits until the element specified by the ``locator`` disappears from the current page.

        Fails if the ``timeout`` expires before the element disappears. See the
        `introduction` for more information about ``timeout`` and its
        default value.

        ``error`` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`,
        `Wait Until Page Contains Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """

        def check_present():
            present = self._is_element_present(locator)
            if not present:
                return
            else:
                return error or "Element '%s' did not disappear in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_present)

    def set_sleep_between_wait_loop(self, seconds=0.2):
        """Sets the sleep interval in ``seconds`` used by the `wait until` loop.
        
        If you use the remote appium server, the default value is not recommended because 
        it is another 200ms overhead to the network latency and will slow down your test
        execution.
        """
        old_sleep = self._sleep_between_wait
        self._sleep_between_wait = robot.utils.timestr_to_secs(seconds)
        return old_sleep
    
    def get_sleep_between_wait_loop(self):
        """Returns the sleep interval in seconds between the wait loops used by the `Wait Until ...` keywords.
        """
        return robot.utils.secs_to_timestr(self._sleep_between_wait)
    
    # Private

    def _wait_until(self, timeout, error, function, *args):
        error = error.replace('<TIMEOUT>', self._format_timeout(timeout))

        def wait_func():
            return None if function(*args) else error

        self._wait_until_no_error(timeout, wait_func)

    def _wait_until_no_error(self, timeout, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        maxtime = time.time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error:
                return
            if time.time() > maxtime:
                self.log_source()
                raise AssertionError(timeout_error)
            time.sleep(self._sleep_between_wait)

    def _format_timeout(self, timeout):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        return robot.utils.secs_to_timestr(timeout)
