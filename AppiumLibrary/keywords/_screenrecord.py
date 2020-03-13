# -*- coding: utf-8 -*-

import os
import robot
import base64
from .keywordgroup import KeywordGroup


class _ScreenrecordKeywords(KeywordGroup):

    def __init__(self):
        self._screenrecord_index = 0
        self._recording = None
        self._output_format = None

    def start_screen_recording(self,
                               timeLimit='180s',
                               **options):
        """Starts a asynchronous Screen Recording for the current open      \
            application.

        ``timeLimit`` sets the actual time limit of the recorded video.
          - The default value for both iOS and Android is 180 seconds (3 minutes).
          - The maximum value for Android is 3 minutes.
          - The maximum value for iOS is 10 minutes.

        `Start Screen Recording` is used hand in hand with `Stop Screen Recording`.
        See `Stop Screen Recording` for more details.
        Example:
            | `Start Screen Recording`  |                   | # starts a screen record session  |
            | ....     keyword actions  |                   |                                   |
            | `Stop Screen Recording`   | filename=output   | # saves the recorded session      |
        """
        timeLimit = robot.utils.timestr_to_secs(timeLimit)
        options['timeLimit'] = timeLimit
        self._output_format = self._set_output_format() \
            if self._output_format is None else self._output_format
        if self._recording is None:
            self._recording = self._current_application().start_recording_screen(**options)

    def stop_screen_recording(self, filename=None, **options):
        """Gathers the output from the previously started screen recording  \
            to a media file, then embeds it to the log.html(only on Android).

        Requires an active or exhausted Screen Recording Session.
        See `Start Screen Recording` for more details.

        Example:
            | `Start Screen Recording`  |                   | # starts a screen record session  |
            | ....     keyword actions  |                   |                                   |
            | `Stop Screen Recording`   | filename=output   | # saves the recorded session      |
        """
        if self._recording is not None:
            self._recording = self._current_application().stop_recording_screen(**options)
            return self._save_recording(filename)
        else:
            raise RuntimeError("There is no Active Screen Record Session.")

    def _save_recording(self, filename):
        path, link = self._get_screenrecord_paths(filename)
        decoded = base64.b64decode(self._recording)
        with open(path, 'wb') as screenrecording:
            screenrecording.write(decoded)
        # Embed the Screen Recording to the log file
        # if the current platform is Android.
        if self._is_android():
            self._html('</td></tr><tr><td colspan="3"><a href="{vid}">'
                       '<video width="800px" controls>'
                       '<source src="{vid}" type="video/mp4">'
                       '</video></a>'.format(vid=link)
                       )
        self._recording = None
        return path

    def _set_output_format(self):
        return '.ffmpeg' if self._is_ios() else '.mp4'

    def _get_screenrecord_paths(self, filename=None):
        if filename is None:
            self._screenrecord_index += 1
            filename = 'appium-screenrecord-{index}{ext}'.format(index=self._screenrecord_index,
                                                                  ext=self._output_format
                                                                  )
        else:
            filename = (filename.replace('/', os.sep)) + self._output_format
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link
