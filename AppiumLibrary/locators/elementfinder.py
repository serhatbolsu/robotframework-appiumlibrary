# -*- coding: utf-8 -*-

from AppiumLibrary import utils
from appium.webdriver.common.appiumby import AppiumBy
from robot.api import logger


class ElementFinder(object):

    def __init__(self):
        self._strategies = {
            'identifier': self._find_by_identifier,
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'class': self._find_by_class_name,
            'accessibility_id': self._find_element_by_accessibility_id,
            'android': self._find_by_android,
            'viewtag': self._find_by_android_viewtag,
            'data_matcher': self._find_by_android_data_matcher,
            'view_matcher': self._find_by_android_view_matcher,
            'ios': self._find_by_ios,
            'css': self._find_by_css_selector,
            'jquery': self._find_by_sizzle_selector,
            'predicate': self._find_by_ios_predicate,
            'chain': self._find_by_chain,
            'default': self._find_by_default
        }

    def find(self, application, locator, tag=None):
        assert application is not None
        assert locator is not None and len(locator) > 0

        (prefix, criteria) = self._parse_locator(locator)
        prefix = 'default' if prefix is None else prefix
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        (tag, constraints) = self._get_tag_and_constraints(tag)
        return strategy(application, criteria, tag, constraints)

    # Strategy routines, private

    def _find_by_identifier(self, application, criteria, tag, constraints):
        elements = self._normalize_result(application.find_elements(by=AppiumBy.ID, value=criteria))
        elements.extend(self._normalize_result(application.find_elements(by=AppiumBy.NAME, value=criteria)))
        return self._filter_elements(elements, tag, constraints)

    def _find_by_id(self, application, criteria, tag, constraints):
        print(f"criteria is {criteria}")
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ID, value=criteria),
            tag, constraints)

    def _find_by_name(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.NAME, value=criteria),
            tag, constraints)

    def _find_by_xpath(self, application, criteria, tag, constraints):
        print(f"xpath criteria: {criteria}")
        return self._filter_elements(
            application.find_elements(by=AppiumBy.XPATH, value=criteria),
            tag, constraints)

    def _find_by_dom(self, application, criteria, tag, constraints):
        result = application.execute_script("return %s;" % criteria)
        if result is None:
            return []
        if not isinstance(result, list):
            result = [result]
        return self._filter_elements(result, tag, constraints)

    def _find_by_sizzle_selector(self, application, criteria, tag, constraints):
        js = "return jQuery('%s').get();" % criteria.replace("'", "\\'")
        return self._filter_elements(
            application.execute_script(js),
            tag, constraints)

    def _find_by_link_text(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.LINK_TEXT, value=criteria),
            tag, constraints)

    def _find_by_css_selector(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.CSS_SELECTOR, value=criteria),
            tag, constraints)

    def _find_by_tag_name(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.TAG_NAME, value=criteria),
            tag, constraints)

    def _find_by_class_name(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.CLASS_NAME, value=criteria),
            tag, constraints)

    def _find_element_by_accessibility_id(self, application, criteria, tag, constraints):
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value=criteria),
            tag, constraints)

    def _find_by_android(self, application, criteria, tag, constraints):
        """Find element matches by UI Automator."""
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value=criteria),
            tag, constraints)

    def _find_by_android_viewtag(self, application, criteria, tag, constraints):
        """Find element matches by its view tag
        Espresso only
        """
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ANDROID_VIEWTAG, value=criteria),
            tag, constraints)

    def _find_by_android_data_matcher(self, application, criteria, tag, constraints):
        """Find element matches by Android Data Matcher
        Espresso only
        """
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ANDROID_DATA_MATCHER, value=criteria),
            tag, constraints)

    def _find_by_android_view_matcher(self, application, criteria, tag, constraints):
        """Find element matches by  Android View Matcher
        Espresso only
        """
        return self._filter_elements(
            application.find_elements(by=AppiumBy.ANDROID_VIEW_MATCHER, value=criteria),
            tag, constraints)

    def _find_by_ios(self, application, criteria, tag, constraints):
        """Find element matches by UI Automation."""
        return self._filter_elements(
            application.find_elements(by=AppiumBy.IOS_UIAUTOMATION, value=criteria),
            tag, constraints)

    def _find_by_ios_predicate(self, application, criteria, tag, constraints):
        """Find element matches by  iOSNsPredicateString."""
        return self._filter_elements(
            application.find_elements(by=AppiumBy.IOS_PREDICATE, value=criteria),
            tag, constraints)

    def _find_by_chain(self, application, criteria, tag, constraints):
        """Find element matches by  iOSChainString."""
        return self._filter_elements(
            application.find_elements(by=AppiumBy.IOS_CLASS_CHAIN, value=criteria),
            tag, constraints)

    def _find_by_default(self, application, criteria, tag, constraints):
        if criteria.startswith('//'):
            return self._find_by_xpath(application, criteria, tag, constraints)
        # Used `id` instead of _find_by_key_attrs since iOS and Android internal `id` alternatives are
        # different and inside appium python client. Need to expose these and improve in order to make
        # _find_by_key_attrs useful.
        return self._find_by_id(application, criteria, tag, constraints)

    # TODO: Not in use after conversion from Selenium2Library need to make more use of multiple auto selector strategy
    def _find_by_key_attrs(self, application, criteria, tag, constraints):
        key_attrs = self._key_attrs.get(None)
        if tag is not None:
            key_attrs = self._key_attrs.get(tag, key_attrs)

        xpath_criteria = utils.escape_xpath_value(criteria)
        xpath_tag = tag if tag is not None else '*'
        xpath_constraints = ["@%s='%s'" % (name, constraints[name]) for name in constraints]
        xpath_searchers = ["%s=%s" % (attr, xpath_criteria) for attr in key_attrs]
        xpath_searchers.extend(
            self._get_attrs_with_url(key_attrs, criteria, application))
        xpath = "//%s[%s(%s)]" % (
            xpath_tag,
            ' and '.join(xpath_constraints) + ' and ' if len(xpath_constraints) > 0 else '',
            ' or '.join(xpath_searchers))
        return self._normalize_result(application.find_elements(by=AppiumBy.XPATH, value=xpath))

    # Private
    _key_attrs = {
        None: ['@id', '@name'],
        'a': ['@id', '@name', '@href', 'normalize-space(descendant-or-self::text())'],
        'img': ['@id', '@name', '@src', '@alt'],
        'input': ['@id', '@name', '@value', '@src'],
        'button': ['@id', '@name', '@value', 'normalize-space(descendant-or-self::text())']
    }

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}

        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = 'text'
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        return tag, constraints

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if not element.get_attribute(name) == constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None:
            return elements
        return filter(
            lambda element: self._element_matches(element, tag, constraints),
            elements)

    def _get_attrs_with_url(self, key_attrs, criteria, browser):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url(browser) + "/" + criteria
                    xpath_url = utils.escape_xpath_value(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self, browser):
        url = browser.get_current_url()
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return (prefix, criteria)

    def _normalize_result(self, elements):
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements
