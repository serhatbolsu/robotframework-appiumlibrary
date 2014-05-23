Appium library for RobotFramework
==================================================

.. image:: https://badge.fury.io/py/robotframework-appiumlibrary.svg
    :target: http://badge.fury.io/py/robotframework-appiumlibrary

.. image:: https://travis-ci.org/jollychang/robotframework-appiumlibrary.svg?branch=master
    :target: https://travis-ci.org/jollychang/robotframework-appiumlibrary

.. image:: https://pypip.in/d/robotframework-appiumlibrary/badge.png
    :target: https://crate.io/packages/robotframework-appiumlibrary/
    :alt: Number of PyPI downloads

.. image:: https://pledgie.com/campaigns/25326.png
    :target: https://pledgie.com/campaigns/25326

Introduction
------------

AppiumLibrary is an appium testing library for `RobotFramework <http://code.google.com/p/robotframework/>`_.

It uses `Appium <http://appium.io/>`_ to communicate with Android application 
similar to how `Selenium WebDriver <http://seleniumhq.org/projects/webdriver/>`_ talks
to web browser.

AppiumLibrary is based on  `appiumandroidlibrary by frankbp <https://github.com/frankbp/robotframework-appiumandroidlibrary>`_.

Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using
`pip <http://pip-installer.org>`__::

    pip install robotframework-appiumlibrary


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
<http://jollychang.github.io/robotframework-appiumlibrary/doc/AppimuLibrary.html>`_
