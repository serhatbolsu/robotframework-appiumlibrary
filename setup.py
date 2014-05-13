#!/usr/bin/env python

import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'src'))
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

execfile(join(dirname(__file__), 'src', 'AppiumLibrary', 'version.py'))

DESCRIPTION = """
appiumlibrary is a app testing library for Robot Framework
that leverages the appium(https://github.com/appium/appium) libraries.
Appium is an open source, cross-platform test automation tool for native, hybrid and mobile web apps,
tested on simulators (iOS, FirefoxOS), emulators (Android), and real devices (iOS, Android, FirefoxOS).
"""[1:-1]

setup(name         = 'robotframework-appiumlibrary',
      version      = VERSION,
      description  = 'app testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'William Zhang, Xie Lieping',
      author_email = '<jollychang@gmail.com>, <frankbp@gmail.com>',
      url          = 'https://github.com/jollychang/robotframework-appiumlibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation mobile appium webdriver app',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = [
                            'decorator >= 3.3.2',
                            'robotframework >= 2.6.0',
                            'docutils >= 0.8.1',
                            'Appium-Python-Client >= 0.5'
                         ],
      py_modules=['ez_setup'],
      package_dir  = {'' : 'src'},
      packages     = ['AppiumLibrary','AppiumLibrary.keywords','AppiumLibrary.locators',
                      'AppiumLibrary.utils'],
      include_package_data = True,
      )