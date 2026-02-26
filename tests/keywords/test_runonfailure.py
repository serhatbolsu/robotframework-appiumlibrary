import unittest
import mock

from AppiumLibrary.keywords._runonfailure import _RunOnFailureKeywords


class RunOnFailureKeywordsTests(unittest.TestCase):
    """Tests for _RunOnFailureKeywords class."""

    def setUp(self):
        """Set up the test fixture."""
        self.rof = _RunOnFailureKeywords()
        self.rof._info = mock.Mock()
        self.rof._warn = mock.Mock()

    def test_initial_state(self):
        """Test that initial state has no keyword registered."""
        self.assertIsNone(self.rof._run_on_failure_keyword)
        self.assertFalse(self.rof._running_on_failure_routine)

    def test_register_keyword_returns_nothing_when_no_previous_keyword(self):
        """Test that registering a keyword returns 'Nothing' when no previous keyword was set."""
        result = self.rof.register_keyword_to_run_on_failure("Log Source")
        self.assertEqual(result, "Nothing")

    def test_register_keyword_sets_new_keyword(self):
        """Test that registering a keyword properly sets the new keyword."""
        self.rof.register_keyword_to_run_on_failure("Log Source")
        self.assertEqual(self.rof._run_on_failure_keyword, "Log Source")

    def test_register_keyword_returns_previous_keyword(self):
        """Test that registering a keyword returns the previously registered keyword."""
        self.rof.register_keyword_to_run_on_failure("Log Source")
        result = self.rof.register_keyword_to_run_on_failure("Capture Page Screenshot")
        self.assertEqual(result, "Log Source")

    def test_register_nothing_disables_run_on_failure(self):
        """Test that registering 'Nothing' disables the run-on-failure functionality."""
        self.rof.register_keyword_to_run_on_failure("Log Source")
        self.rof.register_keyword_to_run_on_failure("Nothing")
        self.assertIsNone(self.rof._run_on_failure_keyword)

    def test_register_nothing_case_insensitive(self):
        """Test that 'nothing' keyword is case insensitive."""
        self.rof.register_keyword_to_run_on_failure("Log Source")
        self.rof.register_keyword_to_run_on_failure("NOTHING")
        self.assertIsNone(self.rof._run_on_failure_keyword)

    def test_register_nothing_with_whitespace(self):
        """Test that 'nothing' keyword handles whitespace."""
        self.rof.register_keyword_to_run_on_failure("Log Source")
        self.rof.register_keyword_to_run_on_failure("  nothing  ")
        self.assertIsNone(self.rof._run_on_failure_keyword)

    def test_run_on_failure_does_nothing_when_no_keyword_registered(self):
        """Test that _run_on_failure does nothing when no keyword is registered."""
        self.rof._run_on_failure()
        # Should not raise and should return early
        self.assertFalse(self.rof._running_on_failure_routine)

    def test_run_on_failure_does_not_run_when_already_running(self):
        """Test that _run_on_failure does not run when already running."""
        self.rof._run_on_failure_keyword = "Some Keyword"
        self.rof._running_on_failure_routine = True
        # Should return early without changing state
        self.rof._run_on_failure()
        self.assertTrue(self.rof._running_on_failure_routine)

    def test_run_on_failure_error_with_warn_method(self):
        """Test that _run_on_failure_error uses _warn when available."""
        self.rof._run_on_failure_keyword = "Test Keyword"
        self.rof._run_on_failure_error("Test error")
        self.rof._warn.assert_called_once()
        call_args = self.rof._warn.call_args[0][0]
        self.assertIn("Test Keyword", call_args)
        self.assertIn("Test error", call_args)

    def test_run_on_failure_error_raises_when_no_warn_method(self):
        """Test that _run_on_failure_error raises exception when _warn not available."""
        # Remove the _warn attribute
        del self.rof._warn
        self.rof._run_on_failure_keyword = "Test Keyword"
        with self.assertRaises(Exception) as context:
            self.rof._run_on_failure_error("Test error")
        self.assertIn("Test Keyword", str(context.exception))
        self.assertIn("Test error", str(context.exception))


if __name__ == '__main__':
    unittest.main()
