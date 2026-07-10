import unittest

import mock
from appium.webdriver.common.appiumby import AppiumBy

from AppiumLibrary.locators import ElementFinder


class ElementFinderTests(unittest.TestCase):
    """ElementFinder keyword test class."""

    def setUp(self):
        """Instantiate the element finder class."""
        self.browser = mock.Mock()
        self.finder = ElementFinder()

    def test_should_have_strategies(self):
        """Element Finder instance should contain expected strategies."""
        self.assertTrue('android' in self.finder._strategies)
        self.assertTrue('ios' in self.finder._strategies)

    def test_should_use_android_finder(self):
        """android strategy should use android finder."""
        self.finder.find(self.browser, 'android=UI Automator', tag=None)
        self.browser.find_elements.assert_called_with(by=AppiumBy.ANDROID_UIAUTOMATOR, value="UI Automator")

    def test_should_use_ios_predicate_finder(self):
        """predicate strategy should use ios predicate finder."""
        self.finder.find(self.browser, 'predicate=type == "XCUIElementTypeButton"', tag=None)
        self.browser.find_elements.assert_called_with(by=AppiumBy.IOS_PREDICATE, value='type == "XCUIElementTypeButton"')

    def test_should_use_sizzle_selector_parameterized(self):
        """jquery strategy should use parameterized script to prevent injection."""
        self.finder.find(self.browser, 'jquery=div.test', tag=None)
        self.browser.execute_script.assert_called_with("return jQuery(arguments[0]).get();", "div.test")
