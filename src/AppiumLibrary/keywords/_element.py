# -*- coding: utf-8 -*-

from appium.webdriver.common.touch_action import TouchAction
from AppiumLibrary import utils
from AppiumLibrary.locators import ElementFinder
from keywordgroup import KeywordGroup

class _ElementKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, element lookups
    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()        

    def click_button(self, id_or_name):
        """ Click button """
        if self._is_ios():
            self._click_element_by_class_name('UIAButton', id_or_name)

    def input_text(self, id_or_name, text):
        """ Input text identified by `locator`.
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        Examples:
        | Input text | id=0            | my_id |
        | Input text | login_textfiled | my_id |
        """
        if self._is_ios():
            self._element_input_text_by_class_name("UIATextField", id_or_name, text)

    def input_password(self, id_or_name, text):
        """ Input secure text """
        if self._is_ios():
            self._element_input_text_by_class_name("UIASecureTextField", id_or_name, text)

    def long_press(self, locator):
        """ Long press the element """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        long_press = TouchAction(driver).long_press(element)
        long_press.perform()

    def reset_application(self):
        """ Reset application """
        driver = self._current_application()
        driver.execute_script('mobile: reset')

    def scroll_screen(self, endX, endY, duration='1',
                      tap_count= '1', startX='0.5', startY='0.5'):
        """ Scroll screen """
        driver = self._current_application()
        args = {'startX':float(startX), 'startY':float(startY),
                'startX':float(endX), 'startY':float(endY),
                'tapCount':int(tap_count), 'duration':int(duration)}
        driver.execute_script('mobile: swipe', args)

    def scroll_element(self, locator, endX, endY, 
                    duration='1', tap_count= '1', startX='0.5', startY='0.5'):
        """ Scroll element """
        driver = self._current_application()
        element = self._element_find(locator, True, True)
        args = {'startX':float(startX), 'startY':float(startY),
                'startX':float(endX), 'startY':float(endY),
                'tapCount':int(tap_count), 'duration':int(duration),
                'element':element.ref}
        driver.execute_script('mobile: swipe', args)

    # def slide_rating_bar(self, locator, endX, endY,
    #                  tap_count='1', startX='0.0', startY='0.0'):
    #     """ Slide rating bar """
    #     driver = self._current_application()
    #     element = self._find_element_by_tag_name('ratingBar', id_or_name)
    #     args = {'startX':float(startX), 'startY':float(startY),
    #             'endX':float(endX), 'endY':float(endY),
    #             'tapCount':int(tap_count), 'element':element.id, 'duration':1}
    #     driver.execute_script('mobile: flick', args)

    # def slide_seek_bar(self, id_or_name, endX, endY,
    #                    tap_count='1', startX='0.0', startY='0.0'):
    #     """ Slide seek bar """
    #     driver = self._current_application()
    #     element = self._find_element_by_tag_name('seekBar', id_or_name)
    #     args = {'startX':float(startX), 'startY':float(startY),
    #             'endX':float(endX), 'endY':float(endY),
    #             'tapCount':int(tap_count), 'element':element.id, 'duration':1}
    #     driver.execute_script('mobile: flick', args)

    def page_should_contain(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if not text in self.log_source(loglevel):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain(self, text, loglevel='INFO'):
        """Verifies that current page not contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.
        """
        if text in self.log_source(loglevel):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page does not contains text '%s'." % text)

    # Private
    
    def _is_id(self, id_or_name):
        if id_or_name.startswith('id='):
            return True
        else:
            return False

    def _click_element_by_name(self, name):
        driver = self._current_application()
        try:
            element = driver.find_element_by_name(name)
        except Exception, e:
            raise Exception, e
    
        try:
            element.click()
        except Exception, e:
            raise Exception, 'Cannot click the element with name "%s"' % name

    def _find_elements_by_class_name(self, class_name):
        driver = self._current_application()
        elements = driver.find_elements_by_class_name(class_name)
        return elements

    def _find_element_by_class_name(self, class_name, id_or_name):
        elements = self._find_elements_by_class_name(class_name)
    
        if self._is_id(id_or_name):
            try:
                index = int(id_or_name.split('=')[-1])
                element = elements[index]
            except IndexError, TypeError:
                raise Exception, 'Cannot find the element with index "%s"' % id_or_name
        else:
            found = False
            for element in elements:
                self._info("'%s'." % element.text)
                if element.text == id_or_name:
                    found = True
                    break
            if not found:
                raise Exception, 'Cannot find the element with name "%s"' % id_or_name

        return element

    def _click_element_by_class_name(self, class_name, id_or_name):
        element = self._find_element_by_class_name(class_name, id_or_name)
        self._info("Clicking element '%s'." % element.text)
        try:
            element.click()
        except Exception, e:
            raise Exception, 'Cannot click the %s element "%s"' % (class_name, id_or_name)

    def _element_input_text_by_class_name(self, class_name, id_or_name, text):
        try:
            element = self._find_element_by_class_name(class_name, id_or_name)
        except Exception, e:
            raise Exception, e

        self._info("input text in element as '%s'." % element.text)
        try:
            element.send_keys(text)
        except Exception, e:
            raise Exception, 'Cannot input text "%s" for the %s element "%s"' % (text, class_name, id_or_name)


    def _element_find(self, locator, first_only, required, tag=None):
        application = self._current_application()
        elements = self._element_finder.find(application, locator, tag)
        if required and len(elements) == 0:
            raise ValueError("Element locator '" + locator + "' did not match any elements.")
        if first_only:
            if len(elements) == 0: return None
            return elements[0]
        return elements