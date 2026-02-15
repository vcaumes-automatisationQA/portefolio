*** Settings ***
Resource    ../pages/Login.resource
Library     SeleniumLibrary

*** Variables ***
${URL}    https://www.saucedemo.com/
&{USERS_LIST}
...    standard_user=secret_sauce
...    locked_out_user=secret_sauce
...    problem_user=secret_sauce
...    performance_glitch_user=secret_sauce
...    error_user=secret_sauce
...    visual_user=secret_sauce

@{VALID_USERS}    standard_user    problem_user    visual_user    performance_glitch_user    error_user
@{LOCKED_USERS}   locked_out_user

*** Test Cases ***
Login Standard User
    [Documentation]     Test de login avec l'utilisateur 'standard_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    standard_user    ${USERS_LIST["standard_user"]}
    Inventory Should Be Visible

Login Locked Out User
    [Documentation]     Test de login avec l'utilisateur 'locked_out_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    locked_out_user    ${USERS_LIST["locked_out_user"]}
    Locked User Error Should Be Visible

Login Problem User
    [Documentation]     Test de login avec l'utilisateur 'problem_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    problem_user    ${USERS_LIST["problem_user"]}
    Inventory Should Be Visible

Login PerformanceGlitch User
    [Documentation]     Test de login avec l'utilisateur 'performance_glitch_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    performance_glitch_user    ${USERS_LIST["performance_glitch_user"]}
    Inventory Should Be Visible

Login Error User
    [Documentation]     Test de login avec l'utilisateur 'error_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    error_user    ${USERS_LIST["error_user"]}
    Inventory Should Be Visible

Login Visual User
    [Documentation]     Test de login avec l'utilisateur 'visual_user'
    [Teardown]    Close Browser If Open
    Open Browser    ${URL}    chrome
    Login With Credentials    visual_user    ${USERS_LIST["visual_user"]}
    Inventory Should Be Visible