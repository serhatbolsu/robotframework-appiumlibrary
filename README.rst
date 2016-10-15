Appium library for RobotFramework
==================================================

Introduction
------------

AppiumLibrary is an appium testing library for `RobotFramework <http://code.google.com/p/robotframework/>`_.

It uses `Appium <http://appium.io/>`_ (version 1.x) to communicate with Android and iOS application 
similar to how `Selenium WebDriver <http://seleniumhq.org/projects/webdriver/>`_ talks
to web browser.

AppiumLibrary is modeled after (and forked from)  `appiumandroidlibrary <https://github.com/frankbp/robotframework-appiumandroidlibrary>`_,  but re-implemented to use appium 1.X technologies.   

It support Python 2.x only.


Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using
`pip <http://pip-installer.org>`__::

    pip install robotframework-appiumlibrary

Using ``setup.py``
''''''''''''''''''

setup.py

::

    git clone https://github.com/jollychang/robotframework-appiumlibrary.git
    cd robotframework-appiumlibrary
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
<http://serhatbolsu.github.io/robotframework-appiumlibrary/AppiumLibrary.html>`_

Contributing
-------------
Fork the project, make a change, and send a pull request!

Project Contributors
--------------------
* `William Zhang <https://github.com/jollychang>`_
* `Xie Lieping <https://github.com/frankbp>`_
* `Jari Nurminen <https://github.com/yahman72>`_
* `Serhat Bolsu <https://github.com/serhatbolsu>`_


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