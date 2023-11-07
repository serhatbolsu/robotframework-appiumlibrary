Appium library for RobotFramework
==================================================

Introduction
------------

AppiumLibrary_ is an appium testing library for `Robot Framework`_. Library can be downloaded from PyPI_.

It uses `Appium <http://appium.io/>`_ to communicate with Android and iOS application
similar to how *Selenium WebDriver* talks to web browser.

It is supporting Python 3.7+ (since Appium Python Client doesn't support Python 2.7 anymore)

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
iOS and Android have separate paths to follow, and those steps better explained in `Appium Driver Setup Guide`_.
Please follow the **Driver-Specific Setup** according to platform.


Usage
-----

To write tests with Robot Framework and AppiumLibrary, 
AppiumLibrary must be imported into your RF test suite.
See `Robot Framework User Guide <https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html>`_
for more information.

As it uses Appium make sure your Appium server is up and running.
For how to use Appium please refer to `Appium Documentation <http://appium.io/docs/en/about-appium/getting-started/>`_

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
.. raw:: html

    <table>
      <tbody>
        <tr>
          <td align="center"><a href="https://github.com/jollychang"><img src="https://avatars.githubusercontent.com/u/64213?s=64&v=4&s=100" width="100px;" alt="William Zhang"/><br /><sub><b>William Zhang</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=jollychang" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/serhatbolsu"><img src="https://avatars.githubusercontent.com/u/7917050?v=4&s=100" width="100px;" alt="Serhat Bolsu"/><br /><sub><b>Serhat Bolsu</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=serhatbolsu" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/yahman72"><img src="https://avatars.githubusercontent.com/u/8724383?s=64&v=4&s=100" width="100px;" alt="Jari Nurminen"/><br /><sub><b>Jari Nurminen</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=yahman72" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/frankbp"><img src="https://avatars.githubusercontent.com/u/1422799?v=4&s=100" width="100px;" alt="Xie Lieping"/><br /><sub><b>Xie Lieping</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=frankbp" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/joshuariveramnltech"><img src="https://avatars.githubusercontent.com/u/51564452?v=4&s=100" width="100px;" alt="Joshua Rivera"/><br /><sub><b>Joshua Rivera</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=joshuariveramnltech" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/js361014"><img src="https://avatars.githubusercontent.com/u/37348338?v=4&s=100" width="100px;" alt="js361014"/><br /><sub><b>js361014</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=js361014" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/matthew-dahm"><img src="https://avatars.githubusercontent.com/u/91557334?v=4&s=100" width="100px;" alt="matthew-dahm"/><br /><sub><b>matthew-dahm</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=matthew-dahm" title="Code">💻</a></td>
        </tr>
        <tr>
          <td align="center"><a href="https://github.com/akupahkala"><img src="https://avatars.githubusercontent.com/u/54975226?v=4&s=100" width="100px;" alt="akupahkala"/><br /><sub><b>akupahkala</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=akupahkala" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/soukingang"><img src="https://avatars.githubusercontent.com/u/2391550?v=4&s=100" width="100px;" alt="soukingang"/><br /><sub><b>soukingang</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=soukingang" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/erik1510"><img src="https://avatars.githubusercontent.com/u/32835295?v=4&s=100" width="100px;" alt="erik1510"/><br /><sub><b>Erik Bartalos</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=erik1510" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/minhnguyenphuonghoang"><img src="https://avatars.githubusercontent.com/u/9115912?v=4&s=100" width="100px;" alt="minhnguyenphuonghoang"/><br /><sub><b>Minh Nguyen</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=minhnguyenphuonghoang" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/sadikkuzu"><img src="https://avatars.githubusercontent.com/u/23168063?v=4&s=100" width="100px;" alt="sadikkuzu"/><br /><sub><b>Sadik Kuzu</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=sadikkuzu" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/kshrestha99"><img src="https://avatars.githubusercontent.com/u/29582193?v=4&s=100" width="100px;" alt="kshrestha99"/><br /><sub><b>KumarS</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=kshrestha99" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/lucyking"><img src="https://avatars.githubusercontent.com/u/4670642?v=4&s=100" width="100px;" alt="lucyking"/><br /><sub><b>Xia Clark</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=lucyking" title="Code">💻</a></td>
        </tr>
        <tr>
          <td align="center"><a href="https://github.com/arnaudruffin"><img src="https://avatars.githubusercontent.com/u/2727108?v=4&s=100" width="100px;" alt="arnaudruffin"/><br /><sub><b>Arnaud Ruffin</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=arnaudruffin" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/jvilla17"><img src="https://avatars.githubusercontent.com/u/51178608?v=4&s=100" width="100px;" alt="jvilla17"/><br /><sub><b>Junuen Villa</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=jvilla17" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/idxn"><img src="https://avatars.githubusercontent.com/u/2438992?v=4&s=100" width="100px;" alt="idxn"/><br /><sub><b>Tanakiat Srisaranyakul</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=idxn" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/tbrito-daitan"><img src="https://avatars.githubusercontent.com/u/36163426?v=4&s=100" width="100px;" alt="tbrito-daitan"/><br /><sub><b>Thiago Paiva Brito</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=tbrito-daitan" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/Meallia"><img src="https://avatars.githubusercontent.com/u/7398724?v=4&s=100" width="100px;" alt="Meallia"/><br /><sub><b>Jonathan Gayvallet</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=Meallia" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/jennyw1"><img src="https://avatars.githubusercontent.com/u/28263065?v=4&s=100" width="100px;" alt="jennyw1"/><br /><sub><b>jennyw1</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=jennyw1" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/ac-simoes"><img src="https://avatars.githubusercontent.com/u/71258806?v=4&s=100" width="100px;" alt="ac-simoes"/><br /><sub><b>ac-simoes</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=ac-simoes" title="Code">💻</a></td>
        </tr>
        <tr>
          <td align="center"><a href="https://github.com/JMcn"><img src="https://avatars.githubusercontent.com/u/6111307?v=4&s=100" width="100px;" alt="JMcn"/><br /><sub><b>JMcn</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=JMcn" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/UlhasDeshmukh"><img src="https://avatars.githubusercontent.com/u/1731041?v=4&s=100" width="100px;" alt="UlhasDeshmukh"/><br /><sub><b>Ulhas Deshmukh</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=UlhasDeshmukh" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/smaspe"><img src="https://avatars.githubusercontent.com/u/4571256?v=4&s=100" width="100px;" alt="smaspe"/><br /><sub><b>smaspe</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=smaspe" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/leongxf"><img src="https://avatars.githubusercontent.com/u/9819586?v=4&s=100" width="100px;" alt="leongxf"/><br /><sub><b>Leon Guo</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=leongxf" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/extr3mal"><img src="https://avatars.githubusercontent.com/u/4517549?v=4&s=100" width="100px;" alt="extr3mal"/><br /><sub><b>eXtReMaL</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=extr3mal" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/babarpramod"><img src="https://avatars.githubusercontent.com/u/10119811?v=4&s=100" width="100px;" alt="babarpramod"/><br /><sub><b>Pramod</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=babarpramod" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/erolstt"><img src="https://avatars.githubusercontent.com/u/5057444?v=4&s=100" width="100px;" alt="erolstt"/><br /><sub><b>Erol Selitektay</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=erolstt" title="Code">💻</a></td>
        </tr>
        <tr>
          <td align="center"><a href="https://github.com/filipehb"><img src="https://avatars.githubusercontent.com/u/869359?v=4&s=100" width="100px;" alt="filipehb"/><br /><sub><b>Filipe Henrique Benjamim de Arruda</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=filipehb" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/filipehba"><img src="https://avatars.githubusercontent.com/u/101719544?v=4&s=100" width="100px;" alt="filipehba"/><br /><sub><b>Filipe Arruda</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=filipehba" title="Code">💻</a></td>
          <td align="center"><a href="https://github.com/felipetortella"><img src="https://avatars.githubusercontent.com/u/8898257?v=4&s=100" width="100px;" alt="felipetortella"/><br /><sub><b>Felipe Luiz Tortella</b></sub></a><br /><a href="https://github.com/serhatbolsu/robotframework-appiumlibrary/commits?author=felipetortella" title="Code">💻</a></td>
        </tr>
      </tbody>
    </table>


AppiumLibrary is modeled after (and forked from)  `appiumandroidlibrary <https://github.com/frankbp/robotframework-appiumandroidlibrary>`_,  but re-implemented to use appium 1.X technologies.


.. _AppiumLibrary: https://github.com/serhatbolsu/robotframework-appiumlibrary
.. _Robot Framework: https://robotframework.org
.. _Keyword Documentation: http://serhatbolsu.github.io/robotframework-appiumlibrary/AppiumLibrary.html
.. _PyPI: https://pypi.org/project/robotframework-appiumlibrary/
.. _Robot Framework installation instructions: https://github.com/robotframework/robotframework/blob/master/INSTALL.rst
.. _Appium Driver Setup Guide: http://appium.io/docs/en/about-appium/getting-started/?lang=en
.. _sample project: https://github.com/serhatbolsu/robotframework-appium-sample
