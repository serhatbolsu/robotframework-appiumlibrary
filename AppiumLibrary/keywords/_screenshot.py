# -*- coding: utf-8 -*-

import os
import robot
from .keywordgroup import KeywordGroup

class _ScreenshotKeywords(KeywordGroup):

    # Public

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot will be
        embedded as Base64 image to the log.html. In this case no file is created in the filesystem.

        Warning: this behavior is new in 1.7. Previously if no filename was given
        the screenshots where stored as separate files named `appium-screenshot-<counter>.png`
        """
        if filename:
            path, link = self._get_screenshot_paths(filename)

            if hasattr(self._current_application(), 'get_screenshot_as_file'):
                self._current_application().get_screenshot_as_file(path)
            else:
                self._current_application().save_screenshot(path)

            # Image is shown on its own row and thus prev row is closed on purpose
            self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                       '<img src="%s" width="800px"></a>' % (link, link))
            return path
        else:
            base64_screenshot = self._current_application().get_screenshot_as_base64()
            self._html('</td></tr><tr><td colspan="3">'
                       '<img src="data:image/png;base64, %s" width="800px">' % base64_screenshot)
            return None

    # Private

    def _get_screenshot_paths(self, filename):
        filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link
