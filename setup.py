#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup, find_packages

ROOT = dirname(abspath(__file__))

version_file = join(ROOT, 'AppiumLibrary', 'version.py')
exec (compile(open(version_file).read(), version_file, 'exec'))

with open(join(ROOT, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()



setup(
    name='robotframework-appiumlibrary',
    version=VERSION,
    description='Robot Framework Mobile app testing library for Appium Client Android & iOS & Mobile Web',
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
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation',
      'Programming Language :: Python :: Implementation :: CPython',
      'Framework :: Robot Framework',
      'Framework :: Robot Framework :: Library'
    ],
    setup_requires=[
      "pytest-runner"
    ],
    install_requires=REQUIREMENTS,
    tests_require=[
      'mock >= 2.0.0',
      'pytest-cov >= 2.5.1',
      'pytest-xdist >= 1.16.0',
      'pytest-pythonpath >= 0.7.1',
      'pytest >= 3.1.0',
      'six >= 1.10.0'
    ],
    packages=find_packages(exclude=["docs", "tests", ]),
    include_package_data=True,
)
