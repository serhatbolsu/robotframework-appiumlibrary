*** Settings ***
#Library  ../AppiumLibrary/
Library  AppiumLibrary
Library  BuiltIn


*** Variables ***
${ANDROID_AUTOMATION_NAME}    UIAutomator2
${ANDROID_APP}                ${CURDIR}/demoapp/ApiDemos-debug.apk
${ANDROID_PLATFORM_NAME}      Android
${ANDROID_PLATFORM_VERSION}   %{ANDROID_PLATFORM_VERSION=11}
${ANDROID_APP_PACKAGE}        io.appium.android.apis

${IOS_AUTOMATION_NAME}        XCUITest
${IOS_APP}                    ${CURDIR}/demoapp/TestApp.app.zip
${IOS_PLATFORM_NAME}          iOS
${IOS_PLATFORM_VERSION}       %{IOS_PLATFORM_VERSION=13.6}
${IOS_DEVICE_NAME}            iPhone 8


*** Keywords ***
Open Android Test App
  [Arguments]    ${appActivity}=${EMPTY}
  open application  http://127.0.0.1:4723/wd/hub  automationName=${ANDROID_AUTOMATION_NAME}
  ...  app=${ANDROID_APP}  platformName=${ANDROID_PLATFORM_NAME}  platformVersion=${ANDROID_PLATFORM_VERSION}
  ...  appPackage=${ANDROID_APP_PACKAGE}  appActivity=${appActivity}


Open iOS Test App
  open application  http://127.0.0.1:4723/wd/hub  automationName=${IOS_AUTOMATION_NAME}
  ...  app=${IOS_APP}  platformName=${IOS_PLATFORM_NAME}  platformVersion=${IOS_PLATFORM_VERSION}
  ...  deviceName=${IOS_DEVICE_NAME}