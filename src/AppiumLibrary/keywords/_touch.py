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

    def swipe_up_within_element(self,locator,start_offset=8,end_offset=2,duration=1000):
        """
               Swipe inside a view, by default will swipe from 80% to 20% of the view at the center

               Args:
                - locator  - locator of the element view
                - start_offset  - value at which to start(scale of 1 - 10)
                - end_offset  - value at which to end(scale of 1 - 10)
                - duration - (optional) time to take the swipe, in ms.

               Usage:
               | swipe up inside element | locator | start_offset | end_offset | duration |
               | swipe up inside element | locator | 8 | 2 | 1000 |

               """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        element_location = element.location
        element_size = element.size

        start_x = element_location['x'] + element_size['width']*0.5
        offset_x = element_location['x'] + element_size['width']*0.5
        start_y = element_location['y'] + element_size['height']*start_offset / 10
        offset_y = element_location['y'] + element_size['height']*end_offset / 10
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def swipe_down_within_element(self,locator,start_offset=2,end_offset=8,duration=1000):
        """
               Swipe inside a view, by default will swipe from 20% to 80% of the view at the center

               Args:
                - locator  - locator of the element view
                - start_offset  - value at which to start(scale of 1 - 10)
                - end_offset  - value at which to end(scale of 1 - 10)
                - duration - (optional) time to take the swipe, in ms.

               Usage:
               | swipe down within element | locator | start_offset | end_offset | duration |
               | swipe down inside element | locator | 2 | 8 | 1000 |

               """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        element_location = element.location
        element_size = element.size

        start_x = element_location['x'] + element_size['width']*0.5
        offset_x = element_location['x'] + element_size['width']*0.5
        start_y = element_location['y'] + element_size['height']*start_offset / 10
        offset_y = element_location['y'] + element_size['height']*end_offset / 10
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def swipe_right_within_element(self,locator,start_offset=2,end_offset=8,duration=1000):
        """
               Swipe inside a view, by default will swipe from 20% to 80% of the view at the center

               Args:
                - locator  - locator of the element view
                - start_offset  - value at which to start(scale of 1 - 10)
                - end_offset  - value at which to end(scale of 1 - 10)
                - duration - (optional) time to take the swipe, in ms.

               Usage:
               | swipe right within element | locator | start_offset | end_offset | duration |
               | swipe right inside element | locator | 2 | 8 | 1000 |

               """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        element_location = element.location
        element_size = element.size

        start_x = element_location['x'] + element_size['width'] * start_offset / 10
        offset_x = element_location['x'] + element_size['width'] * end_offset / 10
        start_y = element_location['y'] + element_size['height'] * 0.5
        offset_y = element_location['y'] + element_size['height'] * 0.5
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def swipe_left_within_element(self, locator, start_offset=8, end_offset=2, duration=1000):
        """
               Swipe inside a view, by default will swipe from 20% to 80% of the view at the center

               Args:
                - locator  - locator of the element view
                - start_offset  - value at which to start(scale of 1 - 10)
                - end_offset  - value at which to end(scale of 1 - 10)
                - duration - (optional) time to take the swipe, in ms.

               Usage:
               | swipe left within element | locator | start_offset | end_offset | duration |
               | swipe left inside element | locator | 8 | 2 | 1000 |

               """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        element_location = element.location
        element_size = element.size

        start_x = element_location['x'] + element_size['width'] * start_offset / 10
        offset_x = element_location['x'] + element_size['width'] * end_offset / 10
        start_y = element_location['y'] + element_size['height'] * 0.5
        offset_y = element_location['y'] + element_size['height'] * 0.5
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

    def scroll_down_inside_element(self, locator):
        """Scrolls down inside an element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'down', 'element': element.id})

    def scroll_up_inside_element(self, locator):
        """Scrolls up inside an element"""
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        driver.execute_script("mobile: scroll", {"direction": 'up', 'element': element.id})

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

    def tap(self, locator, x_offset=None, y_offset=None, count=1):
        """ Tap element identified by ``locator``.

        Args:
        - ``x_offset`` - (optional) x coordinate to tap, relative to the top left corner of the element.
        - ``y_offset`` - (optional) y coordinate. If y is used, x must also be set, and vice versa
        - ``count`` - can be used for multiple times of tap on that element
        """
        driver = self._current_application()
        el = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.tap(el,x_offset,y_offset, count).perform()

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
