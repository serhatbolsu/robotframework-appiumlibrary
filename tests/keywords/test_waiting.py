import unittest
import mock
import robot.utils

from AppiumLibrary.keywords._waiting import _WaitingKeywords


class WaitingKeywordsTests(unittest.TestCase):
    """Tests for _WaitingKeywords class."""

    def setUp(self):
        """Set up the test fixture."""
        self.wk = _WaitingKeywords()
        # Set a default timeout for tests
        self.wk._timeout_in_secs = 5
        self.wk._info = mock.Mock()
        self.wk.log_source = mock.Mock()

    def test_initial_sleep_between_wait_value(self):
        """Test that initial sleep between wait is 0.2 seconds."""
        self.assertEqual(self.wk._sleep_between_wait, 0.2)

    def test_set_sleep_between_wait_loop(self):
        """Test setting the sleep interval."""
        old_value = self.wk.set_sleep_between_wait_loop(0.5)
        self.assertEqual(old_value, 0.2)
        self.assertEqual(self.wk._sleep_between_wait, 0.5)

    def test_set_sleep_between_wait_loop_with_string(self):
        """Test setting the sleep interval with a string value."""
        self.wk.set_sleep_between_wait_loop(robot.utils.timestr_to_secs('1s'))
        self.assertEqual(self.wk._sleep_between_wait, 1.0)

    def test_get_sleep_between_wait_loop(self):
        """Test getting the sleep interval."""
        result = self.wk.get_sleep_between_wait_loop()
        self.assertEqual(result, '200 milliseconds')

    def test_get_sleep_between_wait_loop_after_set(self):
        """Test getting the sleep interval after setting it."""
        self.wk.set_sleep_between_wait_loop(1.0)
        result = self.wk.get_sleep_between_wait_loop()
        self.assertEqual(result, '1 second')

    def test_format_timeout_with_string(self):
        """Test formatting timeout with string input."""
        result = self.wk._format_timeout('10s')
        self.assertEqual(result, '10 seconds')

    def test_format_timeout_with_none_uses_default(self):
        """Test formatting timeout with None uses default timeout."""
        result = self.wk._format_timeout(None)
        self.assertEqual(result, '5 seconds')

    def test_wait_until_element_is_visible_success(self):
        """Test wait_until_element_is_visible succeeds when element is visible."""
        self.wk._is_visible = mock.Mock(return_value=True)
        # Should not raise
        self.wk.wait_until_element_is_visible('locator', timeout='1s')
        self.wk._is_visible.assert_called_with('locator')

    def test_wait_until_element_is_visible_failure(self):
        """Test wait_until_element_is_visible fails when element is not visible."""
        self.wk._is_visible = mock.Mock(return_value=False)
        self.wk._sleep_between_wait = 0.01  # Speed up test
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_element_is_visible('locator', timeout='0.05s')
        self.assertIn('locator', str(context.exception))
        self.assertIn('not visible', str(context.exception))

    def test_wait_until_element_is_visible_element_not_found(self):
        """Test wait_until_element_is_visible fails when element is not found."""
        self.wk._is_visible = mock.Mock(return_value=None)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_element_is_visible('locator', timeout='0.05s')
        self.assertIn('locator', str(context.exception))
        self.assertIn('did not match', str(context.exception))

    def test_wait_until_page_contains_success(self):
        """Test wait_until_page_contains succeeds when text is present."""
        self.wk._is_text_present = mock.Mock(return_value=True)
        self.wk.wait_until_page_contains('expected text', timeout='1s')
        self.wk._is_text_present.assert_called_with('expected text')

    def test_wait_until_page_contains_failure(self):
        """Test wait_until_page_contains fails when text is not present."""
        self.wk._is_text_present = mock.Mock(return_value=False)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_page_contains('expected text', timeout='0.05s')
        self.assertIn('expected text', str(context.exception))
        self.assertIn('did not appear', str(context.exception))

    def test_wait_until_page_does_not_contain_success(self):
        """Test wait_until_page_does_not_contain succeeds when text disappears."""
        self.wk._is_text_present = mock.Mock(return_value=False)
        self.wk.wait_until_page_does_not_contain('text to disappear', timeout='1s')
        self.wk._is_text_present.assert_called_with('text to disappear')

    def test_wait_until_page_does_not_contain_failure(self):
        """Test wait_until_page_does_not_contain fails when text remains."""
        self.wk._is_text_present = mock.Mock(return_value=True)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_page_does_not_contain('persistent text', timeout='0.05s')
        self.assertIn('persistent text', str(context.exception))
        self.assertIn('did not disappear', str(context.exception))

    def test_wait_until_page_contains_element_success(self):
        """Test wait_until_page_contains_element succeeds when element appears."""
        self.wk._is_element_present = mock.Mock(return_value=True)
        self.wk.wait_until_page_contains_element('//button', timeout='1s')
        self.wk._is_element_present.assert_called_with('//button')

    def test_wait_until_page_contains_element_failure(self):
        """Test wait_until_page_contains_element fails when element does not appear."""
        self.wk._is_element_present = mock.Mock(return_value=False)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_page_contains_element('//button', timeout='0.05s')
        self.assertIn('//button', str(context.exception))
        self.assertIn('did not appear', str(context.exception))

    def test_wait_until_page_does_not_contain_element_success(self):
        """Test wait_until_page_does_not_contain_element succeeds when element disappears."""
        self.wk._is_element_present = mock.Mock(return_value=False)
        self.wk.wait_until_page_does_not_contain_element('//spinner', timeout='1s')
        self.wk._is_element_present.assert_called_with('//spinner')

    def test_wait_until_page_does_not_contain_element_failure(self):
        """Test wait_until_page_does_not_contain_element fails when element remains."""
        self.wk._is_element_present = mock.Mock(return_value=True)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_page_does_not_contain_element('//spinner', timeout='0.05s')
        self.assertIn('//spinner', str(context.exception))
        self.assertIn('did not disappear', str(context.exception))

    def test_wait_until_custom_error_message(self):
        """Test that custom error message is used."""
        self.wk._is_text_present = mock.Mock(return_value=False)
        self.wk._sleep_between_wait = 0.01
        with self.assertRaises(AssertionError) as context:
            self.wk.wait_until_page_contains('text', timeout='0.05s', error='Custom error message')
        self.assertIn('Custom error message', str(context.exception))


if __name__ == '__main__':
    unittest.main()
