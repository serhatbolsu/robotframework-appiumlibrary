import unittest
import mock

from AppiumLibrary.keywords._keyevent import _KeyeventKeywords


class KeyeventKeywordsTests(unittest.TestCase):
    """Tests for _KeyeventKeywords class."""

    def setUp(self):
        """Set up the test fixture."""
        self.ke = _KeyeventKeywords()
        self.mock_driver = mock.Mock()
        self.ke._current_application = mock.Mock(return_value=self.mock_driver)

    def test_press_keycode(self):
        """Test press_keycode sends keycode to driver."""
        self.ke.press_keycode(66)  # KEYCODE_ENTER
        self.mock_driver.press_keycode.assert_called_once_with(66, None)

    def test_press_keycode_with_metastate(self):
        """Test press_keycode with meta state."""
        self.ke.press_keycode(66, metastate=1)  # Shift pressed
        self.mock_driver.press_keycode.assert_called_once_with(66, 1)

    def test_press_keycode_shift_alt(self):
        """Test press_keycode with Shift+Alt meta state."""
        self.ke.press_keycode(29, metastate=3)  # KEYCODE_A with Shift+Alt
        self.mock_driver.press_keycode.assert_called_once_with(29, 3)

    def test_long_press_keycode(self):
        """Test long_press_keycode sends long press to driver."""
        self.ke.long_press_keycode(66)
        self.mock_driver.long_press_keycode.assert_called_once_with(66, None)

    def test_long_press_keycode_with_metastate(self):
        """Test long_press_keycode with meta state."""
        self.ke.long_press_keycode(66, metastate=2)  # Alt pressed
        self.mock_driver.long_press_keycode.assert_called_once_with(66, 2)

    def test_long_press_keycode_converts_string_to_int(self):
        """Test that long_press_keycode converts string keycode to int."""
        self.ke.long_press_keycode('66')
        self.mock_driver.long_press_keycode.assert_called_once_with(66, None)


if __name__ == '__main__':
    unittest.main()
