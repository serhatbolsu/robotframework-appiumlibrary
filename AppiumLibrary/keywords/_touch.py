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

        _*NOTE: *_
        Android 'Swipe' is not working properly, use ``offset_x`` and ``offset_y`` as if these are destination points.
        """
        driver = self._current_application()
        driver.swipe(start_x, start_y, offset_x, offset_y, duration)

    def swipe_by_percent(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        Swipe from one percent of the screen to another percent, for an optional duration.
        Normal swipe fails to scale for different screen resolutions, this can be avoided using percent.

        Args:
         - start_x - x-percent at which to start
         - start_y - y-percent at which to start
         - end_x - x-percent distance from start_x at which to stop
         - end_y - y-percent distance from start_y at which to stop
         - duration - (optional) time to take the swipe, in ms.

        Usage:
        | Swipe By Percent | 90 | 50 | 10 | 50 | # Swipes screen from right to left. |

        _*NOTE: *_
        This also considers swipe acts different between iOS and Android.

        New in AppiumLibrary 1.4.5
        """
        width = self.get_window_width()
        height = self.get_window_height()
        x_start = float(start_x) / 100 * width
        x_end = float(end_x) / 100 * width
        y_start = float(start_y) / 100 * height
        y_end = float(end_y) / 100 * height
        x_offset = x_end - x_start
        y_offset = y_end - y_start
        platform = self._get_platform()
        if platform == 'android':
            self.swipe(x_start, y_start, x_end, y_end, duration)
        else:
            self.swipe(x_start, y_start, x_offset, y_offset, duration)

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

    def _generate_xpath_for_uiautomator(self, xpathtext):
        print ">>> Generating XPath for UIAutomator... "

        # 1. get class name
        divider = xpathtext.find('[')
        className = xpathtext[:divider]
        className = className.replace('//','')

        # 2. get property name
        divider = xpathtext.find('@')
        propName = xpathtext[divider+1:]
        divider = propName.find(',')
        propName = propName[:divider]

        # 3. get property value
        divider = xpathtext.find("'")
        propValue = xpathtext[divider+1:]
        divider = propValue.find("'")
        propValue = propValue[:divider]

        print ">>> Generating XPath for UIAutomator completed."
        return className, propName, propValue 

    def scroll_by_uiautomator(self, scroll_strategy, scrollTo_xpath_or_text, scrollView_xpath):        
        """ 
        Scroll to element using UIAutomator  |  Author: thekucays
        https://stackoverflow.com/questions/49486263/how-to-scroll-android-app-with-appium-by-python-client

        Args:
         - scroll_strategy - "0" for Quick Mode, "1" for Normal Mode
         - scrollTo_xpath_or_text - element destination's xpath OR text, depending on scroll_strategy chosen
         - scrollView_xpath - xpath for scrollable element 

        Usage Example:
        | Scroll By Uiautomator | 0 | Produk Rekomendasi | //android.widget.ScrollView[contains(@resource-id,'id.co.foo.prod:id/scroll_view')] | # Scroll down and up until element contains text "Produk Rekomendasi" found |
        | Scroll By Uiautomator | 1 | //android.widget.Button[contains(@resource-id,'id.co.foo.prod:id/bt_submit')] | //android.widget.ScrollView[contains(@resource-id,'id.co.foo.prod:id/scroll_view')] | # Scroll down and up until element with that XPath found |
        
        """
        
        # get the webdriver
        driver = self._current_application()

        # convert xpath string to 3 arrays 
        # eg: 
        # from: //android.widget.FrameLayout[contains(@resource-id,'id.co.foo.prod:id/nav_account')]
        # to: android.widget.FrameLayout | resource-id | id.co.foo.prod:id/nav_account
        if scroll_strategy == '1':
            (scrollTo_class, scrollTo_prop, scrollTo_prop_value) = self._generate_xpath_for_uiautomator(scrollTo_xpath_or_text)
        (scrollable_class, scrollable_prop, scrollable_prop_value) = self._generate_xpath_for_uiautomator(scrollView_xpath) 


        # check if scrollable_prop and scrollTo_prop has dash on it. Convert them if any 
        # eg: "resource-id" to "resourceId", "long-clickable" to "longClickable" 
        dashIndexScrollableProp = scrollable_prop.find('-')

        if dashIndexScrollableProp >= 0:
            # convert to Uppercase for character NEXT TO dashIndex
            charToUpper = scrollable_prop[dashIndexScrollableProp+1]
            charToUpper = charToUpper.upper()
            scrollable_prop = scrollable_prop[:dashIndexScrollableProp+1] + charToUpper + scrollable_prop[dashIndexScrollableProp+2:]
            # print text[:3]        # text sebelum index nya
            # print text[3:]        # text sesudah index nya, include dia nya

            # remove dash "-"
            scrollable_prop = scrollable_prop.replace('-','')
        
        if scroll_strategy == '1':
            dashIndexScrollToProp = scrollTo_prop.find('-')
            if dashIndexScrollToProp >= 0:
                # convert to Uppercase for character NEXT TO dashIndex
                charToUpper = scrollTo_prop[dashIndexScrollToProp+1]
                charToUpper = charToUpper.upper()
                scrollTo_prop = scrollTo_prop[:dashIndexScrollToProp+1] + charToUpper + scrollTo_prop[dashIndexScrollToProp+2:]

                # remove dash "-"
                scrollTo_prop = scrollTo_prop.replace('-','')


        # choose strategy and start scrolling
        if scroll_strategy == '0':
            print ">>> Scrolling with Quick Mode"
            driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().className("' + scrollable_class + '").' + scrollable_prop + '("' + scrollable_prop_value + '")).scrollIntoView(new UiSelector().textContains("' + scrollTo_xpath_or_text + '"))')
            print ">>> Scrolling with Quick Mode finished"
        elif scroll_strategy == '1':
            print ">>> Scrolling with Normal Mode"
            driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().className("' + scrollable_class + '").' + scrollable_prop + '("' + scrollable_prop_value + '")).scrollIntoView(new UiSelector().className("' + scrollTo_class +  '").' + scrollTo_prop + '("' + scrollTo_prop_value + '"))')
            print ">>> Scrolling with Normal Mode finished"
        else:
            raise ValueError("Invalid strategy. Valid strategies are 0 or 1. Please read the doc")


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

    def long_press(self, locator, duration=1000):
        """ Long press the element with optional duration """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        action = TouchAction(driver)
        action.press(element).wait(duration).release().perform()

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
