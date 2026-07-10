import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from AppiumLibrary.keywords._element import _ElementKeywords
from AppiumLibrary import utils
from appium.webdriver.common.appiumby import AppiumBy

class ElementSecurityTests(unittest.TestCase):
    def setUp(self):
        self.element_keywords = _ElementKeywords()
        self.driver = mock.Mock()
        self.element_keywords._current_application = mock.Mock(return_value=self.driver)
        # Mocking _info to avoid issues with BuiltIn
        self.element_keywords._info = mock.Mock()

    def test_android_exact_match_secure(self):
        self.element_keywords._get_platform = mock.Mock(return_value='android')
        self.element_keywords._element_find = mock.Mock(return_value=mock.Mock())
        malicious_text = '"] | //*[@text="injected'

        self.element_keywords._element_find_by_text(malicious_text, exact_match=True)

        escaped_text = utils.escape_xpath_value(malicious_text)
        # Now it should be //*[@text=concat('"', "'] | //*[@text=", '"', "injected")]
        expected_xpath = u'//*[@text={}]'.format(escaped_text)
        self.element_keywords._element_find.assert_any_call(expected_xpath, True, True)

    def test_android_contains_match_secure(self):
        self.element_keywords._get_platform = mock.Mock(return_value='android')
        self.element_keywords._element_find = mock.Mock(return_value=mock.Mock())
        malicious_text = '")] | //*[@text="injected'

        self.element_keywords._element_find_by_text(malicious_text, exact_match=False)

        escaped_text = utils.escape_xpath_value(malicious_text)
        expected_xpath = u'//*[contains(@text,{})]'.format(escaped_text)
        self.element_keywords._element_find.assert_any_call(expected_xpath, True, True)

    def test_ios_exact_match_secure(self):
        self.element_keywords._get_platform = mock.Mock(return_value='ios')
        # ios first tries to find by text directly (not via xpath)
        self.element_keywords._element_find = mock.Mock(side_effect=[None, mock.Mock()])

        malicious_text = '"] | //*[@label="injected'

        self.element_keywords._element_find_by_text(malicious_text, exact_match=True)

        escaped_text = utils.escape_xpath_value(malicious_text)
        expected_xpath = u'//*[@value={text} or @label={text}]'.format(text=escaped_text)
        self.element_keywords._element_find.assert_any_call(expected_xpath, True, True)

    def test_ios_contains_match_secure(self):
        self.element_keywords._get_platform = mock.Mock(return_value='ios')
        self.element_keywords._element_find = mock.Mock(side_effect=[None, mock.Mock()])

        malicious_text = '")] | //*[@label="injected'

        self.element_keywords._element_find_by_text(malicious_text, exact_match=False)

        escaped_text = utils.escape_xpath_value(malicious_text)
        expected_xpath = u'//*[contains(@label,{text}) or contains(@value, {text})]'.format(text=escaped_text)
        self.element_keywords._element_find.assert_any_call(expected_xpath, True, True)

    def test_mixed_quotes_secure(self):
        self.element_keywords._get_platform = mock.Mock(return_value='android')
        self.element_keywords._element_find = mock.Mock(return_value=mock.Mock())
        malicious_text = 'a\'b"c'

        self.element_keywords._element_find_by_text(malicious_text, exact_match=True)

        escaped_text = utils.escape_xpath_value(malicious_text)
        expected_xpath = u'//*[@text={}]'.format(escaped_text)
        self.element_keywords._element_find.assert_any_call(expected_xpath, True, True)
