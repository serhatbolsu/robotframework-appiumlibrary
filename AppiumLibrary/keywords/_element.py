# -*- coding: utf-8 -*-

from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn
import ast
from unicodedata import normalize
from selenium.webdriver.remote.webelement import WebElement

try:
    basestring  # attempt to evaluate basestring


    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)


class _ElementKeywords(KeywordGroup):
    def __init__(self):
        self._element_finder = ElementFinder()
        self._bi = BuiltIn()

    # Public, element lookups
    def clear_text(self, locator):
        """Clears the text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Clear text field '%s'" % locator)
        self._element_clear_text_by_locator(locator)

    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `index` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    def click_button(self, index_or_name):
        """ Click button """
        _platform_class_dict = {'ios': 'UIAButton',
                                'android': 'android.widget.Button'}
        if self._is_support_platform(_platform_class_dict):
            class_name = self._get_class(_platform_class_dict)
            self._click_element_by_class_name(class_name, index_or_name)

    def click_text(self, text, exact_match=False):
        """Click text identified by ``text``.

        By default tries to click first text involves given ``text``, if you would
        like to click exactly matching text, then set ``exact_match`` to `True`.

        If there are multiple use  of ``text`` and you do not want first one,
        use `locator` with `Get Web Elements` instead.

        """
        self._element_find_by_text(text,exact_match).click()

    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._element_input_text_by_locator(locator, text)

    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        self._element_input_text_by_locator(locator, text)

    def input_value(self, locator, text):
        """Sets the given value into text field identified by `locator`. This is an IOS only keyword, input value makes use of set_value

        See `introduction` for details about locating elements.
        """
        self._info("Setting text '%s' into text field '%s'" % (text, locator))
        self._element_input_value_by_locator(locator, text)

    def hide_keyboard(self, key_name=None):
        """Hides the software keyboard on the device. (optional) In iOS, use `key_name` to press
        a particular key, ex. `Done`. In Android, no parameters are used.
        """
        driver = self._current_application()
        driver.hide_keyboard(key_name)

    def page_should_contain_text(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if not self._is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain_text(self, text, loglevel='INFO'):
        """Verifies that current page not contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if self._is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'" % text)
        self._info("Current page does not contains text '%s'." % text)

    def page_should_contain_element(self, locator, loglevel='INFO'):
        """Verifies that current page contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if not self._is_element_present(locator):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained element '%s' "
                                 "but did not" % locator)
        self._info("Current page contains element '%s'." % locator)

    def page_should_not_contain_element(self, locator, loglevel='INFO'):
        """Verifies that current page not contains `locator` element.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if self._is_element_present(locator):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained element '%s'" % locator)
        self._info("Current page not contains element '%s'." % locator)

    def element_should_be_disabled(self, locator, loglevel='INFO'):
        """Verifies that element identified with locator is disabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if self._element_find(locator, True, True).is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be disabled "
                                 "but did not" % locator)
        self._info("Element '%s' is disabled ." % locator)

    def element_should_be_enabled(self, locator, loglevel='INFO'):
        """Verifies that element identified with locator is enabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if not self._element_find(locator, True, True).is_enabled():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be enabled "
                                 "but did not" % locator)
        self._info("Element '%s' is enabled ." % locator)

    def element_should_be_visible(self, locator, loglevel='INFO'):
        """Verifies that element identified with locator is visible.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        
        New in AppiumLibrary 1.4.5
        """
        if not self._element_find(locator, True, True).is_displayed():
            self.log_source(loglevel)
            raise AssertionError("Element '%s' should be visible "
                                 "but did not" % locator)

    def element_name_should_be(self, locator, expected):
        element = self._element_find(locator, True, True)
        if str(expected) != str(element.get_attribute('name')):
            raise AssertionError("Element '%s' name should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('name')))
        self._info("Element '%s' name is '%s' " % (locator, expected))

    def element_value_should_be(self, locator, expected):
        element = self._element_find(locator, True, True)
        if str(expected) != str(element.get_attribute('value')):
            raise AssertionError("Element '%s' value should be '%s' "
                                 "but it is '%s'." % (locator, expected, element.get_attribute('value')))
        self._info("Element '%s' value is '%s' " % (locator, expected))

    def element_attribute_should_match(self, locator, attr_name, match_pattern, regexp=False):
        """Verify that an attribute of an element matches the expected criteria.

        The element is identified by _locator_. See `introduction` for details
        about locating elements. If more than one element matches, the first element is selected.

        The _attr_name_ is the name of the attribute within the selected element.

        The _match_pattern_ is used for the matching, if the match_pattern is
        - boolean or 'True'/'true'/'False'/'false' String then a boolean match is applied
        - any other string is cause a string match

        The _regexp_ defines whether the string match is done using regular expressions (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match%20Regexp|Should
        Match Regexp] or string pattern match (i.e. BuiltIn Library's
        [http://robotframework.org/robotframework/latest/libraries/BuiltIn.html#Should%20Match|Should
        Match])


        Examples:

        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | *foobar |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | text | f.*ar | regexp = True |
        | Element Attribute Should Match | xpath = //*[contains(@text,'foo')] | enabled | True |

        | 1. is a string pattern match i.e. the 'text' attribute should end with the string 'foobar'
        | 2. is a regular expression match i.e. the regexp 'f.*ar' should be within the 'text' attribute
        | 3. is a boolead match i.e. the 'enabled' attribute should be True


        _*NOTE: *_
        On Android the supported attribute names are hard-coded in the
        [https://github.com/appium/appium/blob/master/lib/devices/android/bootstrap/src/io/appium/android/bootstrap/AndroidElement.java|AndroidElement]
        Class's getBoolAttribute() and getStringAttribute() methods.
        Currently supported (appium v1.4.11):
        _contentDescription, text, className, resourceId, enabled, checkable, checked, clickable, focusable, focused, longClickable, scrollable, selected, displayed_


        _*NOTE: *_
        Some attributes can be evaluated in two different ways e.g. these evaluate the same thing:

        | Element Attribute Should Match | xpath = //*[contains(@text,'example text')] | name | txt_field_name |
        | Element Name Should Be         | xpath = //*[contains(@text,'example text')] | txt_field_name |      |

        """
        elements = self._element_find(locator, False, True)
        if len(elements) > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        attr_value = elements[0].get_attribute(attr_name)

        # ignore regexp argument if matching boolean
        if isinstance(match_pattern, bool) or match_pattern.lower() == 'true' or match_pattern.lower() == 'false':
            if isinstance(match_pattern, bool):
                match_b = match_pattern
            else:
                match_b = ast.literal_eval(match_pattern.title())

            if isinstance(attr_value, bool):
                attr_b = attr_value
            else:
                attr_b = ast.literal_eval(attr_value.title())

            self._bi.should_be_equal(match_b, attr_b)

        elif regexp:
            self._bi.should_match_regexp(attr_value, match_pattern,
                                         msg="Element '%s' attribute '%s' should have been '%s' "
                                             "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                         values=False)
        else:
            self._bi.should_match(attr_value, match_pattern,
                                  msg="Element '%s' attribute '%s' should have been '%s' "
                                      "but it was '%s'." % (locator, attr_name, match_pattern, attr_value),
                                  values=False)
        # if expected != elements[0].get_attribute(attr_name):
        #    raise AssertionError("Element '%s' attribute '%s' should have been '%s' "
        #                         "but it was '%s'." % (locator, attr_name, expected, element.get_attribute(attr_name)))
        self._info("Element '%s' attribute '%s' is '%s' " % (locator, attr_name, match_pattern))

    def element_should_contain_text(self, locator, expected, message=''):
        """Verifies element identified by ``locator`` contains text ``expected``.

        If you wish to assert an exact (not a substring) match on the text
        of the element, use `Element Text Should Be`.

        Key attributes for arbitrary elements are ``id`` and ``xpath``. ``message`` can be used to override the default error message.

        New in AppiumLibrary 1.4.
        """
        self._info("Verifying element '%s' contains text '%s'."
                    % (locator, expected))
        actual = self._get_text(locator)
        if not expected in actual:
            if not message:
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def element_should_not_contain_text(self, locator, expected, message=''):
        """Verifies element identified by ``locator`` does not contain text ``expected``.

        ``message`` can be used to override the default error message.
        See `Element Should Contain Text` for more details.
        """
        self._info("Verifying element '%s' does not contain text '%s'."
                   % (locator, expected))
        actual = self._get_text(locator)
        if expected in actual:
            if not message:
                message = "Element '%s' should not contain text '%s' but " \
                          "it did." % (locator, expected)
            raise AssertionError(message)

    def element_text_should_be(self, locator, expected, message=''):
        """Verifies element identified by ``locator`` exactly contains text ``expected``.

        In contrast to `Element Should Contain Text`, this keyword does not try
        a substring match but an exact match on the element identified by ``locator``.

        ``message`` can be used to override the default error message.

        New in AppiumLibrary 1.4.
        """
        self._info("Verifying element '%s' contains exactly text '%s'."
                    % (locator, expected))
        element = self._element_find(locator, True, True)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def get_webelement(self, locator):
        """Returns the first [http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement|WebElement] object matching ``locator``.

        Example:
        | ${element}     | Get Webelement | id=my_element |
        | Click Element  | ${element}     |               |

        New in AppiumLibrary 1.4.
        """
        return self._element_find(locator, True, True)

    def get_webelements(self, locator):
        """Returns list of [http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webelement|WebElement] objects matching ``locator``.

        Example:
        | @{elements}    | Get Webelements | id=my_element |
        | Click Element  | @{elements}[2]  |               |

        This keyword was changed in AppiumLibrary 1.4 in following ways:
        - Name is changed from `Get Elements` to current one.
        - Deprecated argument ``fail_on_error``, use `Run Keyword and Ignore Error` if necessary.

        New in AppiumLibrary 1.4.
        """
        return self._element_find(locator, False, True)

    def get_element_attribute(self, locator, attribute):
        """Get element attribute using given attribute: name, value,...

        Examples:

        | Get Element Attribute | locator | name |
        | Get Element Attribute | locator | value |
        """
        elements = self._element_find(locator, False, True)
        ele_len = len(elements)
        if ele_len == 0:
            raise AssertionError("Element '%s' could not be found" % locator)
        elif ele_len > 1:
            self._info("CAUTION: '%s' matched %s elements - using the first element only" % (locator, len(elements)))

        try:
            attr_val = elements[0].get_attribute(attribute)
            self._info("Element '%s' attribute '%s' value '%s' " % (locator, attribute, attr_val))
            return attr_val
        except:
            raise AssertionError("Attribute '%s' is not valid for element '%s'" % (attribute, locator))

    def get_element_location(self, locator):
        """Get element location

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
        element_location = element.location
        self._info("Element '%s' location: %s " % (locator, element_location))
        return element_location

    def get_element_size(self, locator):
        """Get element size

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
        element_size = element.size
        self._info("Element '%s' size: %s " % (locator, element_size))
        return element_size

    def get_text(self, locator):
        """Get element text (for hybrid and mobile browser use `xpath` locator, others might cause problem)

        Example:

        | ${text} | Get Text | //*[contains(@text,'foo')] |

        New in AppiumLibrary 1.4.
        """
        text = self._get_text(locator)
        self._info("Element '%s' text is '%s' " % (locator, text))
        return text

    def get_matching_xpath_count(self, xpath):
        """Returns number of elements matching ``xpath``

        One should not use the `xpath=` prefix for 'xpath'. XPath is assumed.

        | *Correct:* |
        | ${count}  | Get Matching Xpath Count | //android.view.View[@text='Test'] |
        | Incorrect:  |
        | ${count}  | Get Matching Xpath Count | xpath=//android.view.View[@text='Test'] |

        If you wish to assert the number of matching elements, use
        `Xpath Should Match X Times`.

        New in AppiumLibrary 1.4.
        """
        count = len(self._element_find("xpath=" + xpath, False, False))
        return str(count)

    def text_should_be_visible(self, text, exact_match=False, loglevel='INFO'):
        """Verifies that element identified with text is visible.

        New in AppiumLibrary 1.4.5
        """
        if not self._element_find_by_text(text, exact_match).is_displayed():
            self.log_source(loglevel)
            raise AssertionError("Text '%s' should be visible "
                                 "but did not" % text)

    def xpath_should_match_x_times(self, xpath, count, error=None, loglevel='INFO'):
        """Verifies that the page contains the given number of elements located by the given ``xpath``.

        One should not use the `xpath=` prefix for 'xpath'. XPath is assumed.

        | *Correct:* |
        | Xpath Should Match X Times | //android.view.View[@text='Test'] | 1 |
        | Incorrect: |
        | Xpath Should Match X Times | xpath=//android.view.View[@text='Test'] | 1 |

        ``error`` can be used to override the default error message.

        See `Log Source` for explanation about ``loglevel`` argument.

        New in AppiumLibrary 1.4.
        """
        actual_xpath_count = len(self._element_find("xpath=" + xpath, False, False))
        if int(actual_xpath_count) != int(count):
            if not error:
                error = "Xpath %s should have matched %s times but matched %s times"\
                            %(xpath, count, actual_xpath_count)
            self.log_source(loglevel)
            raise AssertionError(error)
        self._info("Current page contains %s elements matching '%s'."
                   % (actual_xpath_count, xpath))

    # Private

    def _is_index(self, index_or_name):
        if index_or_name.startswith('index='):
            return True
        else:
            return False

    def _click_element_by_name(self, name):
        driver = self._current_application()
        try:
            element = driver.find_element_by_name(name)
        except Exception as e:
            raise e

        try:
            element.click()
        except Exception as e:
            raise 'Cannot click the element with name "%s"' % name

    def _find_elements_by_class_name(self, class_name):
        driver = self._current_application()
        elements = driver.find_elements_by_class_name(class_name)
        return elements

    def _find_element_by_class_name(self, class_name, index_or_name):
        elements = self._find_elements_by_class_name(class_name)

        if self._is_index(index_or_name):
            try:
                index = int(index_or_name.split('=')[-1])
                element = elements[index]
            except (IndexError, TypeError):
                raise 'Cannot find the element with index "%s"' % index_or_name
        else:
            found = False
            for element in elements:
                self._info("'%s'." % element.text)
                if element.text == index_or_name:
                    found = True
                    break
            if not found:
                raise 'Cannot find the element with name "%s"' % index_or_name

        return element

    def _get_class(self, platform_class_dict):
        return platform_class_dict.get(self._get_platform())

    def _is_support_platform(self, platform_class_dict):
        return platform_class_dict.has_key(self._get_platform())

    def _click_element_by_class_name(self, class_name, index_or_name):
        element = self._find_element_by_class_name(class_name, index_or_name)
        self._info("Clicking element '%s'." % element.text)
        try:
            element.click()
        except Exception as e:
            raise 'Cannot click the %s element "%s"' % (class_name, index_or_name)

    def _element_clear_text_by_locator(self, locator):
        try:
            element = self._element_find(locator, True, True)
            element.clear()
        except Exception as e:
            raise e

    def _element_input_text_by_locator(self, locator, text):
        try:
            element = self._element_find(locator, True, True)
            element.send_keys(text)
        except Exception as e:
            raise e

    def _element_input_text_by_class_name(self, class_name, index_or_name, text):
        try:
            element = self._find_element_by_class_name(class_name, index_or_name)
        except Exception as e:
            raise e

        self._info("input text in element as '%s'." % element.text)
        try:
            element.send_keys(text)
        except Exception as e:
            raise 'Cannot input text "%s" for the %s element "%s"' % (text, class_name, index_or_name)

    def _element_input_value_by_locator(self, locator, text):
        try:
            element = self._element_find(locator, True, True)
            element.set_value(text)
        except Exception as e:
            raise e

    def _element_find(self, locator, first_only, required, tag=None):
        application = self._current_application()
        if isstr(locator):
            _locator = locator
            elements = self._element_finder.find(application, _locator, tag)
            if required and len(elements) == 0:
                raise ValueError("Element locator '" + locator + "' did not match any elements.")
            if first_only:
                if len(elements) == 0: return None
                return elements[0]
        elif isinstance(locator, WebElement):
            elements = locator
        # do some other stuff here like deal with list of webelements
        # ... or raise locator/element specific error if required
        return elements

    def _element_find_by_text(self, text, exact_match=False):
        if self._get_platform() == 'ios':
            element = self._element_find(text, True, False)
            if element:
                return element
            else:
                if exact_match:
                    _xpath = u'//*[@value="{}" or @label="{}"]'.format(text, text)
                else:
                    _xpath = u'//*[contains(@label,"{}") or contains(@value, "{}")]'.format(text, text)
                return self._element_find(_xpath, True, True)
        elif self._get_platform() == 'android':
            if exact_match:
                _xpath = u'//*[@{}="{}"]'.format('text', text)
            else:
                _xpath = u'//*[contains(@{},"{}")]'.format('text', text)
            return self._element_find(_xpath, True, True)

    def _get_text(self, locator):
        element = self._element_find(locator, True, True)
        if element is not None:
            return element.text
        return None

    def _is_text_present(self, text):
        text_norm = normalize('NFD', text)
        source_norm = normalize('NFD', self.get_source())
        return text_norm in source_norm

    def _is_element_present(self, locator):
        application = self._current_application()
        elements = self._element_finder.find(application, locator, None)
        return len(elements) > 0
        
    def _is_visible(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            return element.is_displayed()
        return None

