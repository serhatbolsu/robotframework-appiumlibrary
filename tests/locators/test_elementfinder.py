import unittest

import mock

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
        self.browser.find_elements_by_android_uiautomator.assert_called_with("UI Automator")

    def test_should_use_ios_finder(self):
        """ios strategy should use ios finder."""
        self.finder.find(self.browser, 'ios=UI Automation', tag=None)
        self.browser.find_elements_by_ios_uiautomation.assert_called_with("UI Automation")
