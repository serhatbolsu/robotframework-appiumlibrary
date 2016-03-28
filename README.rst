SofrecomAppium library for RobotFramework
==================================================

Introduction
------------

SofrecomAppiumLibrary is an appium testing library for `RobotFramework <http://code.google.com/p/robotframework/>`_.

It uses `Appium <http://appium.io/>`_ (version 1.x) to communicate with Android and iOS application 
similar to how `Selenium WebDriver <http://seleniumhq.org/projects/webdriver/>`_ talks
to web browser.

SofrecomAppiumLibrary is modeled after (and forked from)  `AppiumLibrary <https://github.com/jollychang/robotframework-appiumlibrary>`.   

It support Python 2.x only.


Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using
`pip <http://pip-installer.org>`__::

    pip install robotframework-sofrecomappiumlibrary

Using ``setup.py``
''''''''''''''''''

setup.py

::

    git clone https://github.com/DhiaEddineSaidi/robotframework-sofrecomappiumlibrary
    cd robotframework-sofrecomappiumlibrary
    python setup.py install


Directory Layout
----------------

demo/
    A simple demonstration, with an Android application and RF test suite

doc/
    Keyword documentation

src/
    Python source code


Usage
-----

To write tests with Robot Framework and AppiumLibrary, 
AppiumLibrary must be imported into your RF test suite.
See `Robot Framework User Guide <https://code.google.com/p/robotframework/wiki/UserGuide>`_ 
for more information.

As it uses Appium make sure your Appium server is up and running.
For how to use Appium please refer to `Appium Documentation <http://appium.io/getting-started.html>`_

Documentation
-------------

The keyword documentation could be found at `Keyword Documentation 
<http://DhiaEddineSaidi.github.io/robotframework-appiumlibrary/doc/AppiumLibrary.html>`_

Contributing
-------------
Fork the project, make a change, and send a pull request!

Project Contributors
--------------------
* `Saidi Dhia Eddine <https://github.com/DhiaEddineSaidi>`_



.. image:: https://img.shields.io/pypi/v/robotframework-appiumlibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-appiumlibrary/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/jollychang/robotframework-appiumlibrary.svg?branch=master
    :target: https://travis-ci.org/jollychang/robotframework-appiumlibrary

.. image:: https://img.shields.io/pypi/dm/robotframework-appiumlibrary.svg
    :target: https://pypi.python.org/pypi/robotframework-appiumlibrary/
    :alt: Number of PyPI downloads

.. image:: https://pledgie.com/campaigns/25326.png
    :target: https://pledgie.com/campaigns/25326
