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
        """Starts an asynchronous Screen Recording for the current open application.

        ``timeLimit`` sets the actual time limit of the recorded video.
          - The default value for both iOS and Android is 180 seconds (3 minutes).
          - The maximum value for Android is 3 minutes.
          - The maximum value for iOS is 10 minutes.

        === Optional Args ===

         - ``bitRate`` (Android Only) The video bit rate for the video, in megabits per second.
            4 Mbp/s(4000000) is by default for Android API level below 27.                      \
              20 Mb/s(20000000) for API level 27 and above.

         - ``videoSize`` (Android Only) The format is widthxheight. The default value is the    \
            device's native display resolution (if supported), 1280x720 if not. For best        \
                results, use a size supported by your device's Advanced Video Coding (AVC)      \
                    encoder. For example, "1280x720"

         - ``bugReport`` (Android Only) Set it to true in order to display additional           \
            information on the video overlay, such as a timestamp, that is helpful in           \
                videos captured to illustrate bugs. This option is only supported since         \
                    API level 27 (Android O).

         - ``videoQuality`` (iOS Only) The video encoding quality (low, medium, high,           \
            photo - defaults to medium).

         - ``videoFps`` 	(iOS Only) The Frames Per Second rate of the recorded video.        \
            Change this value if the resulting video is too slow or too fast. Defaults to 10.   \
                This can decrease the resulting file size.

         - ``videoScale`` (iOS Only) The scaling value to apply. Read                           \
            https://trac.ffmpeg.org/wiki/Scaling for possible values. Example value of 720p     \
                scaling is '1280:720'. This can decrease/increase the resulting file size.      \
                    No scale is applied by default.

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
            to a media file, then embeds it to the log.html(Android Only).

        Requires an active or exhausted Screen Recording Session.
        See `Start Screen Recording` for more details.

        === Optional Args ===

         - ``remotePath`` The path to the remote location, where the resulting video should be  \
            uploaded. The following protocols are supported _http/https_, ftp. Null or empty  \
                string value (the default setting) means the content of resulting file should   \
                    be encoded as Base64 and passed as the endpoint response value. An          \
                        exception will be thrown if the generated media file is too big to fit  \
                            into the available process memory.

         - ``username`` The name of the user for the remote authentication.

         - ``password`` The password for the remote authentication.

         - ``method`` The http multipart upload method name. The _PUT_ one is used by default.

        Example:
            | `Start Screen Recording`  |                   | # starts a screen record session  |
            | ....     keyword actions  |                   |                                   |
            | `Stop Screen Recording`   | filename=output   | # saves the recorded session      |
        """
        if self._recording is not None:
            self._recording = self._current_application().stop_recording_screen(**options)
            return self._save_recording(filename, options)
        else:
            raise RuntimeError("There is no Active Screen Record Session.")

    def _save_recording(self, filename, options):
        path, link = self._get_screenrecord_paths(options, filename)
        decoded = base64.b64decode(self._recording)
        with open(path, 'wb') as screenrecording:
            screenrecording.write(decoded)
        # Embed the Screen Recording to the log file
        # if the current platform is Android and no remotePath is set.
        if self._is_android() and not self._is_remotepath_set(options):
            self._html('</td></tr><tr><td colspan="3"><a href="{vid}">'
                       '<video width="800px" controls>'
                       '<source src="{vid}" type="video/mp4">'
                       '</video></a>'.format(vid=link)
                       )
        # Empty Screen Record Variable
        self._recording = None
        return path

    def _set_output_format(self):
        return '.ffmpeg' if self._is_ios() else '.mp4'

    def _get_screenrecord_paths(self, options, filename=None):
        if filename is None:
            self._screenrecord_index += 1
            filename = 'appium-screenrecord-{index}{ext}'.format(index=self._screenrecord_index,
                                                                 ext=self._output_format
                                                                 )
        else:
            filename = (filename.replace('/', os.sep)) + self._output_format
        logdir = options['remotePath'] if self._is_remotepath_set(options) \
            else self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _is_remotepath_set(self, options):
        return True if 'remotePath' in options else False
