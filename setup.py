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
that leverages the appium libraries.
"""[1:-1]

setup(name         = 'robotframework-appiumlibrary',
      version      = VERSION,
      description  = 'app testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Xie Lieping , William Zhang',
      author_email = '<frankbp@gmail.com> ,  <jollychang@gmail.com>',
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
                            'selenium >= 2.32.0',
                            'robotframework >= 2.6.0',
                            'docutils >= 0.8.1'
                         ],
      py_modules=['ez_setup'],
      package_dir  = {'' : 'src'},
      packages     = ['AppiumLibrary','AppiumLibrary.keywords','AppiumLibrary.locators',
                      'AppiumLibrary.utils'],
      include_package_data = True,
      )