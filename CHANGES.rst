History
=======
1.4.5
----------------
- Swipe By Percent - new keyword added
- Element Should Be Visible - new keyword added
- Text Should Be Visible - new keyword added
- Get Window Height - new keyword added
- Get Window Width - new keyword added

1.4.4
----------------
- Get Capability  added for easy access to desired capabilities

1.4.2
----------------
- Wait Until Page Contains / Page should contain text unicode fix

1.4.1.1
----------------
- Fix desiredCapability dict problem for Appium 1.6 compatibility

1.4.1
----------------
- Unicode better support
- Unicode supported now inside xpath text.
- Click Text iOS handling is much better now. Works regardless if text is name, value or label

1.4.0
----------------
- New finding elements strategy now supports directly using WebElement. Check keyword documentation for more information.
- Added default locator strategies. Default is: id and xpath check library introduction for more details.
- Click Text added as keyword in which you can directly click on found texts. Underlying it works on predefined xpath depending on platform.
- Unicode fixes also reflected on Page Should Contain Text and Page Should Not Contain Text
- Getting an element text is added and its helper keywords.

1.3.7
----------------
- ``swipe`` critical bug fix <https://github.com/jollychang/robotframework-appiumlibrary/pull/125>

1.3.6
----------------
- `modify click_a_point() action  <https://github.com/jollychang/robotframework-appiumlibrary/pull/81>`
- `Add 'press_at' in keywords/_touch.py <https://github.com/jollychang/robotframework-appiumlibrary/pull/83>`
- `add duration for click a point keyowrd <https://github.com/jollychang/robotframework-appiumlibrary/pull/88>`
- Bug fix and update document

1.3.5
----------------
- `Update _touch.py  <https://github.com/jollychang/robotframework-appiumlibrary/pull/74>`
- `New Element & Attribute KW's and docstring fixes  <https://github.com/jollychang/robotframework-appiumlibrary/pull/73>`
- `Fix for default value of `Hide Keyboard  <https://github.com/jollychang/robotframework-appiumlibrary/pull/70>`
- `Set Appium Timeout / Get Appium Timeout keywords added  <https://github.com/jollychang/robotframework-appiumlibrary/pull/69>`
1.3.4
----------------
- `hide_keyboard_set_selenium_final  <https://github.com/jollychang/robotframework-appiumlibrary/pull/68>`
1.3.3
----------------
- `'get element attribute' and 'element value should be' keywords added   <https://github.com/jollychang/robotframework-appiumlibrary/pull/61>`
- `Add Screen Orientation change <https://github.com/jollychang/robotframework-appiumlibrary/pull/60>`
1.3.2
----------------
- `support css selector in web view   <https://github.com/jollychang/robotframework-appiumlibrary/pull/59>`
- `Selenium selector fix   <https://github.com/jollychang/robotframework-appiumlibrary/pull/58>`
1.3.1
----------------
- `Remove Application keyword added   <https://github.com/jollychang/robotframework-appiumlibrary/pull/56>`
1.3.0
----------------
- `Add iOS UI Automation and Android UI Automator locator strategies.  <https://github.com/jollychang/robotframework-appiumlibrary/pull/55>`
1.2.7
----------------
- `Update BuiltIn library reference for RF 2.9 compatibility  <https://github.com/jollychang/robotframework-appiumlibrary/pull/52>`
1.2.6
----------------
- limit version of robotframework
- `Adding new wait keywords  <https://github.com/jollychang/robotframework-appiumlibrary/pull/51>`
1.2.5
----------------
- `Droid Utils: new file/folder handling methods <https://github.com/jollychang/robotframework-appiumlibrary/pull/31>`_
- Hide Keyboard for Android
1.2.4
----------------
- fix sauceclient dependence 
- Added keyword "Go To URL"
- update demo for new Open Application argument
1.2.2
----------------
- fix pytest-pythonpath dependence 
1.2.0
----------------
- Open Application support all Appium server, iOS, Android capabilities
- fix switch appication and add testcase

1.1.0
----------------
- `Andoid Keyevents feature <https://github.com/jollychang/robotframework-appiumlibrary/pull/25>`_
- Additional updates to open_application()'s optional parameter handling
- add coverage and mock for unittest
1.0.22
----------------
- `update doc for switch_application <https://github.com/jollychang/robotframework-appiumlibrary/pull/13>`_
1.0.21
----------------
- `Do not support appium version for saucelabs`

1.0.20
----------------
- `send desired capabilities to saucelabs <https://github.com/jollychang/robotframework-appiumlibrary/issues/20>`_
_ `Added desired Capability newCommandTimeout <https://github.com/jollychang/robotframework-appiumlibrary/pull/19>`_

1.0.19
----------------
- `Open Application Keyword udid argument issues <https://github.com/jollychang/robotframework-appiumlibrary/pull/17>`_
- `Update Wait Until Page Contains Element Keyword documentation <https://github.com/jollychang/robotframework-appiumlibrary/pull/16>`_

1.0.18
----------------
- `added tap functionality to keyword by shadeimi <https://github.com/jollychang/robotframework-appiumlibrary/pull/14>`_
- `Support for multiple appium connections by yahman72 <https://github.com/jollychang/robotframework-appiumlibrary/pull/13>`_

1.0.17
----------------
- support app_wait_package and app_wait_activity

1.0.16
----------------
- add udid and bundleid
- add background_app
- fix Resetting an application

1.0.15
----------------
- replace _is_id by _is_index, id is keep same as `find_elements_by_id <http://selenium-python.readthedocs.org/en/latest/api.html#selenium.webdriver.remote.webdriver.WebDriver.find_elements_by_id>`_.
- Change Location Strategy of "Input text" and "Input Password", not only index and name.
- update demo demo/test_android_contacts.txt

1.0.14
----------------
fix "Locating elements by accessibility_id"

1.0.13
----------------
add keywords as below:

- Get current context
- Get contexts
- Switch to context

1.0.12
----------------
fix swipe

1.0.11
----------------
add keywords as below:

- Zoom
- Pinch
- Swipe
- Scroll
- Lock
- Shake
- Hide Keyword(iOS only)

1.0.10
----------------

add keywords as below:

- Element Name Should Be
- Element Should Be Disabled
- Element Should Be Enabled
- Page Should Contain Element
- Page Should Not Contain Element
- Page Should Contain Text
- Page Should Not Contain Text

No notes on earlier releases.