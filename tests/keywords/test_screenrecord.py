import unittest
import mock

from AppiumLibrary.keywords._screenrecord import _ScreenrecordKeywords


class ScreenrecordKeywordsTests(unittest.TestCase):
    """Tests for _ScreenrecordKeywords class."""

    def setUp(self):
        """Set up the test fixture."""
        self.sr = _ScreenrecordKeywords()
        self.mock_driver = mock.Mock()
        self.sr._current_application = mock.Mock(return_value=self.mock_driver)
        self.sr._html = mock.Mock()
        self.sr._get_log_dir = mock.Mock(return_value='/tmp/logs')
        # Mock platform detection
        self.sr._set_output_format = mock.Mock(return_value='mp4')

    def test_initial_state(self):
        """Test initial state of screen recorder."""
        sr = _ScreenrecordKeywords()
        self.assertEqual(sr._screenrecord_index, 0)
        self.assertIsNone(sr._recording)
        self.assertIsNone(sr._output_format)

    def test_start_screen_recording(self):
        """Test starting screen recording."""
        self.sr.start_screen_recording()
        self.mock_driver.start_recording_screen.assert_called_once()

    def test_start_screen_recording_with_time_limit(self):
        """Test starting screen recording with time limit."""
        self.sr.start_screen_recording(timeLimit='60s')
        call_kwargs = self.mock_driver.start_recording_screen.call_args[1]
        self.assertEqual(call_kwargs['timeLimit'], 60)

    def test_start_screen_recording_with_options(self):
        """Test starting screen recording with additional options."""
        self.sr.start_screen_recording(timeLimit='60s', bitRate=4000000)
        call_kwargs = self.mock_driver.start_recording_screen.call_args[1]
        self.assertEqual(call_kwargs['timeLimit'], 60)
        self.assertEqual(call_kwargs['bitRate'], 4000000)

    def test_start_screen_recording_does_not_restart_if_already_recording(self):
        """Test that starting screen recording doesn't restart if already recording."""
        self.sr._recording = 'existing_recording'
        self.sr.start_screen_recording()
        self.mock_driver.start_recording_screen.assert_not_called()

    def test_stop_screen_recording_without_active_session_raises(self):
        """Test stopping screen recording without active session raises error."""
        with self.assertRaises(RuntimeError) as context:
            self.sr.stop_screen_recording()
        self.assertIn('no Active Screen Record Session', str(context.exception))

    def test_stop_screen_recording_with_active_session(self):
        """Test stopping screen recording with active session."""
        self.sr._recording = 'active_recording'
        self.sr._output_format = 'mp4'
        self.mock_driver.stop_recording_screen.return_value = 'base64videodata'
        self.sr._save_recording = mock.Mock(return_value='/tmp/logs/recording.mp4')
        
        result = self.sr.stop_screen_recording(filename='recording')
        
        self.mock_driver.stop_recording_screen.assert_called_once()
        self.sr._save_recording.assert_called_once()

    def test_stop_screen_recording_with_options(self):
        """Test stopping screen recording with upload options."""
        self.sr._recording = 'active_recording'
        self.sr._output_format = 'mp4'
        self.mock_driver.stop_recording_screen.return_value = 'base64videodata'
        self.sr._save_recording = mock.Mock(return_value='/tmp/logs/recording.mp4')
        
        self.sr.stop_screen_recording(filename='recording', remotePath='http://server/upload')
        
        call_kwargs = self.mock_driver.stop_recording_screen.call_args[1]
        self.assertEqual(call_kwargs['remotePath'], 'http://server/upload')


if __name__ == '__main__':
    unittest.main()
