*** Settings ***
Documentation   demo for appium library
Force Tags      demo
Resource        demo/demo_resoure.txt


*** Test Cases ***
test_demo
    [Tags]  regression
    TestStart
    Reset Application