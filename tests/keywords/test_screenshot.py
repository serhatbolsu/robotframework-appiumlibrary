import unittest
import mock
import os

from AppiumLibrary.keywords._screenshot import _ScreenshotKeywords


class ScreenshotKeywordsTests(unittest.TestCase):
    """Tests for _ScreenshotKeywords class."""

    def setUp(self):
        """Set up the test fixture."""
        self.ss = _ScreenshotKeywords()
        self.mock_driver = mock.Mock()
        self.ss._current_application = mock.Mock(return_value=self.mock_driver)
        self.ss._html = mock.Mock()
        self.ss._get_log_dir = mock.Mock(return_value='/tmp/logs')

    def test_capture_page_screenshot_without_filename_returns_none(self):
        """Test that capturing screenshot without filename returns None."""
        self.mock_driver.get_screenshot_as_base64.return_value = 'base64data'
        result = self.ss.capture_page_screenshot()
        self.assertIsNone(result)

    def test_capture_page_screenshot_without_filename_embeds_base64(self):
        """Test that capturing screenshot without filename embeds base64 image."""
        self.mock_driver.get_screenshot_as_base64.return_value = 'base64data'
        self.ss.capture_page_screenshot()
        self.ss._html.assert_called_once()
        call_args = self.ss._html.call_args[0][0]
        self.assertIn('base64data', call_args)
        self.assertIn('data:image/png;base64', call_args)

    def test_capture_page_screenshot_with_filename_returns_path(self):
        """Test that capturing screenshot with filename returns the path."""
        result = self.ss.capture_page_screenshot('screenshot.png')
        expected_path = os.path.join('/tmp/logs', 'screenshot.png')
        self.assertEqual(result, expected_path)

    def test_capture_page_screenshot_with_filename_saves_to_file(self):
        """Test that capturing screenshot with filename saves to file."""
        self.ss.capture_page_screenshot('screenshot.png')
        expected_path = os.path.join('/tmp/logs', 'screenshot.png')
        self.mock_driver.get_screenshot_as_file.assert_called_once_with(expected_path)

    def test_capture_page_screenshot_uses_save_screenshot_fallback(self):
        """Test that save_screenshot is used if get_screenshot_as_file not available."""
        del self.mock_driver.get_screenshot_as_file
        self.ss.capture_page_screenshot('screenshot.png')
        expected_path = os.path.join('/tmp/logs', 'screenshot.png')
        self.mock_driver.save_screenshot.assert_called_once_with(expected_path)

    def test_capture_page_screenshot_with_subdirectory(self):
        """Test capturing screenshot to a subdirectory."""
        result = self.ss.capture_page_screenshot('screenshots/test.png')
        expected_path = os.path.join('/tmp/logs', 'screenshots', 'test.png')
        self.assertEqual(result, expected_path)

    def test_capture_page_screenshot_embeds_html_link(self):
        """Test that screenshot with filename embeds HTML link."""
        self.ss.capture_page_screenshot('screenshot.png')
        self.ss._html.assert_called_once()
        call_args = self.ss._html.call_args[0][0]
        self.assertIn('href=', call_args)
        self.assertIn('img src=', call_args)


if __name__ == '__main__':
    unittest.main()
