===================
AppiumLibrary 2.1.0
===================

AppiumLibrary is a mobile testing solution for Robot Framework. This release includes
quite a few changes which are listed below.

Changes
-------
- Relaxed requirement for selenium allowing up to and including 4.16
- Fix selenium to use compatible versions
- updated documentation for ios predicate
    * Updated documentation for predicate type of element
    * Delete .DS_Store
    * Update documentation on ios predicate
- Added optional `first_only` parameter to `Get Text` (#402)
    * Be able to get the text from all elements matching one locator
    * Default behavior not changed
- Fix dependency break  (#417) (#418)
    Python-Appium-Client 4.0.0 has removed certain features installation
    breaks currently as current codebase still uses those removed features
    like TouchAction
- Added method to click iOS Alert button in Appium v2 (#420)
- Update Android element attributes names docs in _element.py (#421)
- Fix: remove appended dot in waitactivity (#383)
   * Remove appending of dot in Android wait_activity
- use capabilities instead of desired_capabilities (#414)
   * ...to support selenium 4.17.2 and above
- Update Server CLI Args link in _applicationmanagement.py (#408)
- Fix contributor link of jollychang in README.rst (#405)
- Fix selenium to use compatible versions
- Add library argument and keyword to set sleep between wait until loop (#313)
    * Make sleep between wait loop configurable via keyword
    * add get sleep_between_wait keyword
    * rename keyword
    * add sleep_between_wait_loop argument in library import
- Enhance README file (#373)
    * Enhance README file
      - Update the project contributors.
      - Add 2 Options for installation
      - Add Apache 2.0 License Badge
    * Set Uniform Size for Contributor's avatars
- GitHub workflows (#357)
    * Create publish.yml
    * Update .github/workflows/publish.yml
    * Removed Install dependencies step
- Implement New Action Keyword Drag And Drop (#371)
- Implement New Action Keyword `Flick` (#370)
    * Implement New Action Keyword `Flick`
    * Revise the location of the flick keyword
    * Update Documentation
- Fix Makefile
    * Typo fix in help
    * Indentation fix in test_requirements
- Update docs


Acknowledgements
----------------

There are many people who helped put together the changes for this release. I
want to thank Guilherme Correa, Liviu Avram, Yoann, Jani Mikkonen, Dor Blayzer,
euphonious28, tkoukkari, Sadik Kuzau, Tanakiat Srisaranyakul, Josh Rivera,
Filipe Henrique Benjamim de Arruda for their contributions to the issues and
changes made in this release.

I personally want to thank Serhat Bolsu for working with me and the larger Robot
Framework community to continue to maintain and support this library. As a community,
we have greatly benefited from his work and look forward to the continued success of
the library.

I also want to thank Gaja, Joshua, Liviu, Aviv, Dor, and an every growing list of community
members who have helped me understanding all aspects of Appium and the mobile testing
space within Robot Framework.    - Ed Manlove