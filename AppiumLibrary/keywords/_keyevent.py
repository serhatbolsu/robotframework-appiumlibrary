# -*- coding: utf-8 -*-

from .keywordgroup import KeywordGroup


class _KeyeventKeywords(KeywordGroup):

    # Public
    def press_keycode(self, keycode, metastate=None):
        """Sends a press of keycode to the device.

        Android only.

        Possible keycodes & meta states can be found in
        http://developer.android.com/reference/android/view/KeyEvent.html

        Meta state describe the pressed state of key modifiers such as
        Shift, Ctrl & Alt keys. The Meta State is an integer in which each
        bit set to 1 represents a pressed meta key.

        For example
        - META_SHIFT_ON = 1
        - META_ALT_ON = 2

        | metastate=1 --> Shift is pressed
        | metastate=2 --> Alt is pressed
        | metastate=3 --> Shift+Alt is pressed

         - _keycode- - the keycode to be sent to the device
         - _metastate- - status of the meta keys
        """
        driver = self._current_application()
        driver.press_keycode(keycode, metastate)

    def long_press_keycode(self, keycode, metastate=None):
        """Sends a long press of keycode to the device.

        Android only.

        See `press keycode` for more details.
        """
        driver = self._current_application()
        driver.long_press_keycode(int(keycode), metastate)
