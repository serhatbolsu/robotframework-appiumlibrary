# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction
from AppiumLibrary.locators import ElementFinder
from .keywordgroup import KeywordGroup


class _TouchKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def zoom(self, locator, percent="200%", steps=1):
        """
        Zooms in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.zoom(element=element, percent=percent, steps=steps)

    def pinch(self, locator, percent="200%", steps=1):
        """
        Pinch in on an element a certain amount.
        """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.pinch(element=element, percent=percent, steps=steps)

    def swipe(self, start_x, start_y, offset_x, offset_y, duration=1000):
        """
        Swipe from one point to another point, for an optional duration.

        Args:
         - start_x - x-coordinate at which to start
         - start_y - y-coordinate at which to start
         - offset_x - x-coordinate distance from start_x at which to stop
         - offset_y - y-coordinate distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe | 500 | 100 | 100 | 0 | 1000 |

        *!Important Note:* Android `Swipe` is not working properly, use ``offset_x`` and ``offset_y``
        as if these are destination points.
        """
        driver = self._current_application()
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def scroll(self, start_locator, end_locator):
        """
        Scrolls from one element to another
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        el1 = self._element_find(start_locator, True, True)
        el2 = self._element_find(end_locator, True, True)
        driver = self._current_application()
        driver.scroll(el1, el2)

    def scroll_down(self, locator):
        """Scrolls down to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'down', 'element': element.id})

    def scroll_up(self, locator):
        """Scrolls up to element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'up', 'element': element.id})

    def long_press(self, locator):
        """ Long press the element """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        long_press = TouchAction(driver).long_press(element)
        long_press.perform()

    def tap(self, locator):
        """ Tap on element """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el).perform()

    def click_a_point(self, x=0, y=0, duration=100):
        """ Click on a point"""
        self._info("Clicking on a point (%s,%s)." % (x,y))
        driver = self._current_application()
        action = TouchAction(driver)
        try:
            action.press(x=float(x), y=float(y)).wait(float(duration)).release().perform()
        except:
            assert False, "Can't click on a point at (%s,%s)" % (x,y)

    def click_element_at_coordinates(self, coordinate_X, coordinate_Y):
        """ click element at a certain coordinate """
        self._info("Pressing at (%s, %s)." % (coordinate_X, coordinate_Y))
        driver = self._current_application()
        action = TouchAction(driver)
        action.press(x=coordinate_X, y=coordinate_Y).release().perform()
