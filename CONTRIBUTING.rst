======================== 

**Contribution Guidelines**

======================== 
  

Our Philosoph
-----------------
AppiumLibrary is a community-driven project. We believe in open collaboration, 

quality over quantity, and maintaining a library that is easy to use for both 

beginners and experts. Our goal is to provide reliable, well-documented keywords 

that work seamlessly across iOS and Android platforms. 

  

**Ways to Contribute** 
======================== 

  

1. Help Answer Questions 
~~~~~~~~~~~~~~~~~~~~~~~~

Participate in discussions and help users with any issues they are encountering: 

- Join the `Robot Framework Slack`_ and help in the ``#appiumlibrary`` channel 

- Answer questions in the `Robot Framework Forum`_ 

- Share your knowledge and experience with the community 

  

2. Report Issues 
~~~~~~~~~~~~~~~~~

**Submitting Bug Reports:** 
  

If you find any bugs or unexpected behavior, we encourage you to submit an issue. 

Please follow the `Bug Report Guideline`_ below. 
  

**Feature Requests:** 

If you have an idea for a feature you'd like to see, feel free to submit a 

feature request as a GitHub issue. Please describe your use case and how the 

feature would benefit the community. We'll discuss it with you before any 

work begins. 


**Reproducing Existing Issues:** 

If an issue has already been reported, try to reproduce it and provide 

additional information if possible. Your help in confirming issues is valuable! 

  

3. Contribute Code 
~~~~~~~~~~~~~~~~~

Fork the project, make a change, and send a pull request! See the 

`Development Setup`_ and `Submitting Changes`_ sections below. 

  

4. Improve Documentation 
~~~~~~~~~~~~~~~~~~~~~~~~

  

Help us improve the documentation by fixing typos, adding examples, or 

clarifying existing content. Documentation contributions are just as 

valuable as code contributions! 


Submitting Issues 
======================== 
 

  

**How to Create Issues**
  

**Is it a bug?** 

  

- If you think you've encountered a bug, check the `existing issues`_ to see 

  if it's already reported. If you can't find it, feel free to create a new issue. 

- If you're unsure whether it is a bug, you can ask in Slack or Forum first 

  to see if others are encountering the same issue or if it's something we 

  are already working on. 

  

**Feature requests:** 

  

If you have an idea for a new feature or enhancement: 

  

1. Check the `existing issues`_ to see if someone has already suggested it 

2. If not, create a new issue with the label "enhancement" 

3. Describe the feature, your use case, and how it would benefit users 

4. Be prepared to discuss the implementation approach with maintainers 

  

We appreciate well-thought-out feature requests that include example usage 

and consider both iOS and Android platforms where applicable. 

  

Bug Report Guideline 
======================== 
  

When submitting a bug report, please include as much information as possible 

to help us reproduce and fix the issue. This includes: 

  

- **Python version** (e.g., 3.11.4) 

- **Appium version** (e.g., 2.5.1) 

- **Appium Python Client version** (e.g., 5.1.1) 

- **AppiumLibrary version** (e.g., 3.1) 

- **Platform** (iOS or Android) and version (e.g., Android 14, iOS 17.2) 

- **Driver and its version** (e.g., UIAutomator2 2.34.1, XCUITest 5.12.0) 

- **Simulator or real device** 

- **Device information** (model of the device you're testing on) 

- **Steps to reproduce** (minimal test case if possible) 

- **Error messages** (full stack trace) 

- **Expected vs. actual behavior** 

  

Example bug report:: 

  

    **Environment:** 

    - Python: 3.11.4 

    - Appium Server: 2.5.1 

    - Appium Python Client: 5.1.1 

    - AppiumLibrary: 3.1 

    - Platform: Android 14 

    - Driver: UIAutomator2 2.34.1 

    - Device: Pixel 7 (emulator) 

  

    **Keyword:** 

    `Open Application` 

  

    **Description:** 

    The keyword does not correctly process capabilities with the `appium:` 

    prefix. When passing capabilities like `appium:automationName`, they 

    are not properly forwarded to the Appium server. 

  

    **Steps to Reproduce:** 

    1. Call `Open Application` with W3C-style capabilities using the 

       `appium:` prefix 

    2. Observe that the capability is either ignored or causes an error 

  

    **Expected Result:** 

    Capabilities with `appium:` prefix should be correctly passed to the 

    Appium server and the session should start successfully. 

  

    **Actual Result:** 

    The capability is not recognized, resulting in a session creation failure. 

  

    **Error Message:** 

    ``` 

    WebDriverException: Could not create session.  

    Required capability 'automationName' not found. 

    ``` 

  

    **Minimal Example:** 

    ```robotframework 

    *** Test Cases *** 

    Example 

        Open Application    http://127.0.0.1:4723 

        ...    platformName=Android 

        ...    appium:automationName=UIAutomator2 

        ...    appium:app=/path/to/app.apk 

    ``` 

  

.. warning:: 

  

   Please remember that all information you submit will be **public**. 
   Do **NOT** include any private or confidential information as this is a public repository. 

  

Contributing Code 
================= 


Keyword Documentation 
~~~~~~~~~~~~~~~~~~~~~ 

  

All public keywords must have docstrings. When adding new keywords: 

  

- First paragraph is a brief description 

- Document all arguments with their types and default values 

- Add examples showing common usage 

- Note any platform-specific behavior (iOS vs Android) 

  

Example:: 

  

    def click_element(self, locator, modifier=False): 

        """Click element identified by ``locator``. 

  

        Key attributes for arbitrary elements are ``id`` and ``name``. 

  

        If ``modifier`` is set to ``True``, the element will be 

        clicked with a long press gesture. 

  

        Examples: 

        | Click Element | id=button_submit | 

        | Click Element | xpath=//android.widget.Button[@text='OK'] | 

  

        See also `Click Button`, `Click Text`, and `Long Press`. 

        """ 

        pass 

  

Generating Documentation 
~~~~~~~~~~~~~~~~~

  

To regenerate the keyword documentation:: 

  

    python -m robot.libdoc ./AppiumLibrary/ ./docs/AppiumLibrary.html 

  

Submitting Changes 
~~~~~~~~~~~~~~~~~

  

1. **Create a new branch** for your feature or bugfix:: 

  

       git checkout -b my-feature-branch 

  

2. **Make your changes** and commit them with clear messages 

  

3. **Push your branch** to your fork:: 

  

       git push origin my-feature-branch 

  

4. **Open a pull request** against the main repository 

  

5. **Ensure CI checks pass** and address any review feedback 

  

For questions or discussions, feel free to open an issue on GitHub or 

reach out on Slack. 

  

Project Contributors 
~~~~~~~~~~~~~~~~~

  

See the `README`_ for the full list of project contributors. 

  

We appreciate all contributions, big and small! Contributors will be 

acknowledged in the release notes. 

  

Thank you for helping make AppiumLibrary better! 
