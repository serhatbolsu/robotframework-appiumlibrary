Appium library for RobotFramework
==================================================

Introduction
------------

AppiumLibrary_ is an appium testing library for `Robot Framework`_. Library can be downloaded from PyPI_.

It uses `Appium <http://appium.io/>`_ to communicate with Android and iOS application
similar to how *Selenium WebDriver* talks to web browser.

It is supporting Python 3.9+ and Appium Python Client 5.1.1+

.. image:: https://img.shields.io/pypi/v/robotframework-appiumlibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-appiumlibrary/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/robotframework-appiumlibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-appiumlibrary/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License


.. contents::


Keyword Documentation
---------------------

See `Keyword Documentation`_ for available keywords and more information about the library in general.


Installation
------------

**Option 1**  (recommended)

The recommended installation method is using
`pip <http://pip-installer.org>`__::

    pip install --upgrade robotframework-appiumlibrary


**Option 2**  

It is possible to install directly from GitHub repository. To Install latest source
from the master branch, use this command:
`pip <http://pip-installer.org>`__::

  pip install git+https://github.com/serhatbolsu/robotframework-appiumlibrary.git

Please note that installation will take some time, because ``pip`` will
clone the `AppiumLibrary`_ project to a temporary directory and then
perform the installation.


See `Robot Framework installation instructions`_ for detailed information
about installing Python and Robot Framework itself.

Device Setup
------------
After installing the library, you still need to setup an simulator/emulator or real device to use in tests.
iOS and Android have separate paths to follow, and those steps better explained in `Appium Quickstart Intro`_.
Please follow the **Driver-Specific Setup** according to platform.

[*As we make updates to the AppiumLibrary we want to provide current and helpful documentation with regards
to setting up not only devices but the full development environment. I'll note personally I found this to be
a bit overwhelming and complex - doable but lengthy. Once source which greatly helped me is the*
`RoboCon 2024 workshop notes`_ *provide by the team at Eficode. This information may be incorporated here
in the future.*]

Usage
-----

To write tests with Robot Framework and AppiumLibrary, 
AppiumLibrary must be imported into your RF test suite.
See `Robot Framework User Guide <https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html>`_
for more information.

As it uses Appium make sure your Appium server is up and running.
For how to use Appium please refer to `Appium Quickstart Intro`_.

When using Robot Framework, it is generally recommended to write tests easy to read/modify.
The keywords provided in AppiumLibrary are pretty low level. It is thus typically a good idea to write tests using
Robot Framework's higher level keywords that utilize AppiumLibrary
keywords internally. This is illustrated by the following example
where AppiumLibrary keywords like ``Input Text`` are primarily
used by higher level keywords like ``Input Search Query``.

.. code:: robotframework

    *** Settings ***
    Documentation  Simple example using AppiumLibrary
    Library  AppiumLibrary

    *** Variables ***
    ${ANDROID_AUTOMATION_NAME}    UIAutomator2
    ${ANDROID_APP}                ${CURDIR}/demoapp/ApiDemos-debug.apk
    ${ANDROID_PLATFORM_NAME}      Android
    ${ANDROID_PLATFORM_VERSION}   %{ANDROID_PLATFORM_VERSION=11}

    *** Test Cases ***
    Should send keys to search box and then check the value
      Open Test Application
      Input Search Query  Hello World!
      Submit Search
      Search Query Should Be Matching  Hello World!


    *** Keywords ***
    Open Test Application
      Open Application  http://127.0.0.1:4723/wd/hub  automationName=${ANDROID_AUTOMATION_NAME}
      ...  platformName=${ANDROID_PLATFORM_NAME}  platformVersion=${ANDROID_PLATFORM_VERSION}
      ...  app=${ANDROID_APP}  appPackage=io.appium.android.apis  appActivity=.app.SearchInvoke

    Input Search Query
      [Arguments]  ${query}
      Input Text  txt_query_prefill  ${query}

    Submit Search
      Click Element  btn_start_search

    Search Query Should Be Matching
      [Arguments]  ${text}
      Wait Until Page Contains Element  android:id/search_src_text
      Element Text Should Be  android:id/search_src_text  ${text}

Create a file with the content above (name it: ``test_file.robot``) and execute::

    robot test_file.robot

The above example is single file test case, more examples can be found in a `sample project`_ that illustrates using
Robot Framework and AppiumLibrary. Check the sample project that you can find examples of mobile web & ios & android.

Contributing
-------------
Fork the project, make a change, and send a pull request!

Project Contributors
--------------------

================    ====================   ==================================
William Zhang       akupahkala             Arnaud Ruffin
Serhat Bolsu        soukingang             Junuen Villa
Xie Lieping         Erik Bartalos          Tanakiat Srisaranyakul
Joshua Rivera       Minh Nguyen            Thiago Paiva Brito
js361014            Sadik Kuzu             Jonathan Gayvallet
matthew-dahm        KumarS                 jennyw1
JMcn                Xia Clark              ac-simoes
Ulhas Deshmukh      Leon Guo               Pramod
smaspe              eXtReMaL               Erol Selitektay
Filipe Arruda       Felipe Luiz Tortella   Filipe Henrique Benjamim de Arruda
Gaja                Gabriela Simion        Christoph Singer
Eslam Elmishtawy    Oliver Boehmer         Roman Haladej
Mikko Korpela       Hélio Guilherme        Mark Moberts
Ed Manlove
================    ====================   ==================================


AppiumLibrary is modeled after (and forked from)  `appiumandroidlibrary <https://github.com/frankbp/robotframework-appiumandroidlibrary>`_,  but re-implemented to use appium 1.X technologies.


.. _AppiumLibrary: https://github.com/serhatbolsu/robotframework-appiumlibrary
.. _Robot Framework: https://robotframework.org
.. _Keyword Documentation: http://serhatbolsu.github.io/robotframework-appiumlibrary/AppiumLibrary.html
.. _PyPI: https://pypi.org/project/robotframework-appiumlibrary/
.. _Robot Framework installation instructions: https://github.com/robotframework/robotframework/blob/master/INSTALL.rst
.. _Appium Quickstart Intro: https://appium.io/docs/en/latest/quickstart/
.. _sample project: https://github.com/serhatbolsu/robotframework-appium-sample
.. _RoboCon 2024 workshop notes: https://github.com/eficode-academy/rf-mobile-testing-appium?tab=readme-ov-file#robocon-2024
