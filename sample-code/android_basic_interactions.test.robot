*** Settings ***
Resource  ./resource.robot
Test Teardown  Close Application

*** Test Cases ***
Should send keys to search box and then check the value
  Open Android Test App  .app.SearchInvoke
  input text  txt_query_prefill  Hello world!
  click element  btn_start_search
  wait until page contains element  android:id/search_src_text
  ${elem_text}  get text  id=android:id/search_src_text
  should be equal  Hello world!  ${elem_text}


Should click a button that opens an alert and then dismisses it
  Open Android Test App  .app.AlertDialogSamples
  click element  two_buttons
  wait until page contains element  android:id/alertTitle
  ${alert_text}  get text  android:id/alertTitle
  should contain  ${alert_text}  Lorem ipsum dolor sit aie consectetur adipiscing
  ${close_dialog_button}  get webelement  android:id/button1
  click element  ${close_dialog_button}
