# -*- coding: utf-8 -*-

import time

from appium.webdriver.extensions.action_helpers import ActionHelpers

from datetime import timedelta
from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup

from robot.api import logger
from typing import Union


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """*DEPRECATED!!*
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def swipe(self, *, start_x: Union[int, float], start_y: Union[int, float], end_x: Union[int, float], end_y: Union[int, float], duration: Union[int, timedelta] = timedelta(seconds=1)):
        """
        Swipes from one point to another point, for an optional ``duration``.

        Args:
        - ``start_x`` - x-coordinate at which to start
        - ``start_y`` - y-coordinate at which to start
        - ``end_x`` - x-coordinate at which to stop
        - ``end_y`` - y-coordinate at which to stop
        - ``duration`` - defines the swipe speed as time taken to swipe from point a to point b.


        Examples:
        | Swipe | start_x=500 | start_y=100 | end_x=100 | end_y=0 | duration=1s |
        | Swipe | start_x=500 | start_y=100 | end_x=100 | end_y=0 | duration=100ms |
        """

        if isinstance(duration, int):
            logger.warn(
                "Keyword 'Swipe' will not support int in ms for 'duration' in the future. "
                "Use timedelta with units ('ms' or 's') instead."
            )
            duration = timedelta(milliseconds=duration)

        args = [start_x, start_y, end_x, end_y]

        for i, arg in enumerate(args):
            if isinstance(arg, float):
                logger.warn(
                    "Keyword 'Swipe' converts the values of 'start_x', 'start_y', 'end_x', 'end_y' to integer."
                )
                args[i] = int(arg)

        start_x, start_y, end_x, end_y = args

        driver = self._current_application()
        driver.swipe(start_x, start_y, end_x, end_y, duration.total_seconds() * 1000)

    def swipe_by_percent(self, start_x: Union[int, float], start_y: Union[int, float], end_x: Union[int, float], end_y: Union[int, float], duration: Union[int, timedelta] = timedelta(seconds=1)):
        """
        Swipes from one percent of the screen to another percent, for an optional ``duration``.
        Normal swipe fails to scale for different screen resolutions, this can be avoided by using this keyword.

        Args:
         - ``start_x`` - x-percent at which to start
         - ``start_y`` - y-percent at which to start
         - ``end_x`` - x-percent distance from start_x at which to stop
         - ``end_y`` - y-percent distance from start_y at which to stop
         - ``duration`` - (optional) time to take the swipe

        Examples:
        | Swipe By Percent | 90 | 50 | 10 | 50 | # Swipes screen from right to left. |

        _*NOTE: *_
        This also considers swipe acts different between iOS and Android.

        """

        if isinstance(duration, int):
            logger.warn(
                "Keyword 'Swipe By Percent' will not support int in ms for 'duration' in the future. "
                "Use timedelta with units ('ms' or 's') instead."
            )
            duration = timedelta(milliseconds=duration)

        args = [start_x, start_y, end_x, end_y]

        for i, arg in enumerate(args):
            if isinstance(arg, float):
                logger.warn(
                    "Keyword 'Swipe' converts the values of 'start_x', 'start_y', 'end_x', 'end_y' to integer."
                )
                args[i] = int(arg)

        start_x, start_y, end_x, end_y = args

        width = self.get_window_width()
        height = self.get_window_height()
        x_start = int(start_x / 100 * width)
        x_end = int(end_x / 100 * width)
        y_start = int(start_y / 100 * height)
        y_end = int(end_y / 100 * height)
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        platform = self._get_platform()
        if platform == 'android':
            self.swipe(start_x=x_start, start_y=y_start, end_x=x_end, end_y=y_end, duration=duration)
        else:
            self.swipe(start_x=x_start, start_y=y_start, end_x=x_offset, end_y=y_offset, duration=duration)

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from the element identified by ``start_locator`` to the element identified by ``end_locator``.
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)

    def scroll_down(self, locator, timeout=10, retry_interval=1):
        """Scrolls down until the element identified by ``locator`` is found or until the ``timeout`` (Android only) is reached.
        
        Args:
        - ``locator`` - (mandatory) locator of the element to scroll down to
        - ``timeout`` - (optional, Android only) timeout in seconds (default=10s)
        - ``retry_interval`` - (optional) interval between scroll attempts in seconds (default=1s)
        """
        driver = self._current_application()
        platform = self._get_platform()
        if platform == 'android':
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    element = self._element_find(locator, True, True)
                    return True
                except ValueError:
                    print('Element not visible, scrolling...')
                    width = self.get_window_width()
                    height = self.get_window_height()

                    x = width / 2
                    start_y = height * 0.8 # 80% of the screen
                    end_y = height * 0.2 # 20% of the screen

                    driver.swipe(start_x=int(x), start_y=int(start_y), end_x=int(x), end_y=int(end_y), duration=1000)
                time.sleep(retry_interval)
        else:
            element = self._element_find(locator, True, True)
            driver.execute_script("mobile: scroll", {"direction": 'down', 'elementid': element.id})
            return True

        raise AssertionError(f"Element '{locator}' not found within {timeout} seconds.")

    def scroll_up(self, locator, timeout=10, retry_interval=1):
        """Scrolls up until the element identified by the ``locator`` is found or the ``timeout`` (Android only) is reached.
        
        Args:
        - ``locator`` - (mandatory)  locator of the element to scroll up to
        - ``timeout`` - (optional, Android only) timeout in seconds (default=10s)
        - ``retry_interval`` - (optional) interval between scroll attempts in seconds (default=1s)
        """
        driver = self._current_application()
        platform = self._get_platform()
        if platform == 'android':
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    element = self._element_find(locator, True, True)
                    return True
                except ValueError:
                    print('Element not visible, scrolling...')
                    width = self.get_window_width()
                    height = self.get_window_height()

                    x = width / 2
                    start_y = height * 0.2
                    end_y = height * 0.8

                    driver.swipe(start_x=int(x), start_y=int(start_y), end_x=int(x), end_y=int(end_y), duration=1000)
                time.sleep(retry_interval)
        else:
            element = self._element_find(locator, True, True)
            driver.execute_script("mobile: scroll", {"direction": 'up', 'elementid': element.id})
            return True

        raise AssertionError(f"Element '{locator}' not found within {timeout} seconds.")


    def long_press(self, locator, duration=1000):
        """
        *DEPRECATED!!*  Use `Tap` instead.

        Long presses the element identified by the ``locator`` with an optional ``duration``.

        Args:
        - ``locator`` - locator of the element to be long pressed
        - ``duration`` - duration of the time to tap, in ms (default=1000ms)

        Examples:
        | Long Press | xpath=//*[@resource-id='login_button'] |
        | Long Press | xpath=//*[@name='link'] | duration=3000 |
        """
        element = self._element_find(locator, True, True)
        location = element.location
        size = element.size
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 2
        driver = self._current_application()
        driver.tap([(center_x, center_y)], duration)

    def tap_with_positions(self, duration:Union[int, timedelta] = timedelta(seconds=1), *locations):
        """Taps on a particular place with up to five fingers, holding for a
        certain time.

        Args:
        - ``locations`` - an array of tuples representing the x/y coordinates of
                the fingers to tap. Length can be up to five.
        - ``duration`` - length of time to tap (default=1s)

        Example:
        |  @{firstFinger}   |  create list  |  ${100}  |  ${500}  |
        |  @{secondFinger}  |  create list  |${700}    |  ${500}  |
        |  @{fingerPositions}  |  create list  |  ${firstFinger}  |  ${secondFinger}  |
        |  Sleep  |  1  |
        |  Tap with Positions  |  ${1000}  |  @{fingerPositions}  |
        """
        if isinstance(duration, int):
            logger.warn(
                "Keyword 'Tap With Positions' will not support int in ms for 'duration' in the future. "
                "Use timedelta with units ('ms' or 's') instead."
            )
            duration = timedelta(milliseconds=duration)
        
        driver = self._current_application()
        driver.tap(positions=list(locations), duration=duration.total_seconds() * 1000)

    def tap_with_number_of_taps(self, locator, number_of_taps, number_of_touches):
        """ Sends one or more taps with one or more touch points.

        *iOS only.*

        Args:
        - ``number_of_taps`` - the number of taps
        - ``number_of_touches`` - the number of touch points
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        params = {'element': element, 'numberOfTaps': number_of_taps, 'numberOfTouches': number_of_touches}
        driver.execute_script("mobile: tapWithNumberOfTaps", params)

    def click_alert_button(self, button_name):
        """ Clicks on the alert button identified by ``button_name``.\n
        *iOS only.*

        Args:
        - ``button_name`` - the text on the iOS alert button

        Example:
        |  Click Alert Button  |  Allow  |
        """
        driver = self._current_application()
        params={'action': 'accept', 'buttonLabel': button_name}
        driver.execute_script("mobile: alert", params)

    def drag_and_drop(self, locator: str, target: str):
        """Drags the element identified by the ``locator`` into the ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target. See the
        `Locating elements` section for details about the locator syntax.

        Args:
        - ``locator`` - the element to drag
        - ``target`` - the element to drag to

        Example:
        | `Drag And Drop` | id=div#element | id=div.target |
        """
        element = self._element_find(locator, True, True)
        target = self._element_find(target, True, True)
        driver = self._current_application()
        driver.drag_and_drop(element, target)

    def flick(self, start_x:int, start_y:int, end_x:int, end_y:int):
        """Flicks from one point to another point.

        Args:
        - ``start_x`` - x-coordinate at which to start
        - ``start_y`` - y-coordinate at which to start
        - ``end_x``   - x-coordinate at which to stop
        - ``end_y``   - y-coordinate at which to stop

        Example:
        | Flick | 100 | 100 | 100 | 400 | # Flicks the screen up. |
        """
        driver = self._current_application()
        driver.flick(start_x, start_y, end_x, end_y)

    def tap(self, element: Union[str, list], count:int = 1, duration=timedelta(seconds=1)):
        """Taps the ``element`` for ``count`` times over the ``duration``. 

        Args:
        - ``element`` - locator or coordinates of the element to be tapped
        - ``count`` - number of times the element should be tapped
        - ``duration`` - duration of time to tap (default=1s)


        Examples:
        | Tap | xpath=//*[@resource-id='login_button'] |
        | Tap | xpath=//*[@name='picture'] | duration=3s |
        | Tap | xpath=//*[@name='picture'] | count=2 | duration=1s |

        | VAR | @{coordinates} | 100 | 270 |

        | Tap | ${coordinates} | count=3 |
        """
        driver = self._current_application()

        if isinstance(element, list):
            if len(element) == 2:
                x = int(element[0])
                y = int(element[1])
                for _ in range(count):
                    driver.tap([(x, y)], duration.total_seconds() * 1000)
            else:
                raise ValueError(f"Invalid coordinates format: {element}. Expected a list like [x, y]")
            
        elif isinstance(element, str):
            for _ in range(count):
                el = self._element_find(element, True, True)
                location = el.location
                size = el.size
                center_x = location['x'] + size['width'] // 2
                center_y = location['y'] + size['height'] // 2
                driver.tap([(center_x, center_y)], duration.total_seconds() * 1000)

        else:
            raise ValueError(f"Invalid argument type. Expected xpath (str) or coordinates (list), but got {type(element)}")
