*** Settings ***
Documentation   demo for appium library
Force Tags      demo
Resource        demo/demo_resoure.txt


*** Test Cases ***
test_demo
    [Tags]  regression
    Open Application  http://localhost:4723/wd/hub  platformName=Android  platformVersion=4.2.2  deviceName=192.168.56.101:5555  app=${CURDIR}/demoapp/OrangeDemoApp.apk  automationName=appium  appPackage=com.netease.qa.orangedemo  appActivity=MainActivity