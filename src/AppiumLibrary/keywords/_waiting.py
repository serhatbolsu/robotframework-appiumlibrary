import time
import robot
from keywordgroup import KeywordGroup


class _WaitingKeywords(KeywordGroup):
    def wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until `text` appears on current page.

        Fails if `timeout` expires before the text appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Does Not Contain`,
        `Wait Until Page Contains Element`,
        `Wait Until Page Does Not Contain Element` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Text '%s' did not appear in <TIMEOUT>" % text
        self._wait_until(timeout, error, self._is_text_present, text)

    def wait_until_page_does_not_contain(self, text, timeout=None, error=None):
        """Waits until `text` disappears from current page.

        Fails if `timeout` expires before the `text` disappears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

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
        """Waits until element specified with `locator` appears on current page.

        Fails if `timeout` expires before the element appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`,
        `Wait Until Page Does Not Contain`
        `Wait Until Page Does Not Contain Element`
        and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)

    def wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` disappears from current page.

        Fails if `timeout` expires before the element disappears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

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
            time.sleep(0.2)

    def _format_timeout(self, timeout):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        return robot.utils.secs_to_timestr(timeout)
