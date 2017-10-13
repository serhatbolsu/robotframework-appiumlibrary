#!/usr/bin/env python

from os.path import dirname, join, realpath
from setuptools import setup, find_packages

ROOT = realpath(dirname(__file__))

version_file = join(ROOT, 'AppiumLibrary', 'version.py')
exec (compile(open(version_file).read(), version_file, 'exec'))

with open(join(ROOT, 'test_require.txt'), "rt") as f:
    tests_require = f.readlines()

setup(name='robotframework-appiumlibrary',
      version=VERSION,
      description='Robot Framework Mobile app testing library for Appium Client Android & iOS & Web',
      long_description=open(join(ROOT, 'README.rst')).read(),
      author='Serhat Bolsu, William Zhang, Xie Lieping, Jari Nurminen',
      author_email='serhatbolsu@gmail.com,jollychang@gmail.com,frankbp@gmail.com',
      url='https://github.com/serhatbolsu/robotframework-appiumlibrary',
      license='Apache License 2.0',
      keywords='robotframework testing testautomation mobile appium webdriver app android ios',
      platforms='any',
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: Apache Software License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Testing",
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      setup_requires=[
          "pytest-runner"
      ],
      install_requires=[
          'decorator >= 3.3.2',
          'robotframework >= 2.6.0',
          'docutils >= 0.8.1',
          'Appium-Python-Client >= 0.20',
          'selenium >= 2.47.1',
          'kitchen >= 1.2.4',
      ],
      tests_require=tests_require,
      packages=find_packages(exclude=["demo", "docs", "tests", ]),
      include_package_data=True,
      )
