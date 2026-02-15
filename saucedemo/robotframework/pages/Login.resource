*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${USERNAME_INPUT}    id=user-name
${PASSWORD_INPUT}    id=password
${LOGIN_BUTTON}      id=login-button
${ERROR_MESSAGE}     css=h3[data-test='error']

*** Keywords ***
Enter Username
    [Documentation]     Permet de saisir le nom de l'utilisateur passé en paramètre
    [Arguments]    ${username}
    Wait Until Element Is Visible    ${USERNAME_INPUT}    timeout=10s
    Input Text    ${USERNAME_INPUT}    ${username}

Enter Password
    [Documentation]     Permet de saisir le mot de passe passé en paramètre
    [Arguments]    ${password}
    Input Text    ${PASSWORD_INPUT}    ${password}

Click Login Button
    [Documentation]     Permet de cliquer sur le bouton de login
    Click Button    ${LOGIN_BUTTON}

Get Error Message
    [Documentation]     Permet de récupérer le message d'erreur affiché
    ${msg}=    Get Text    ${ERROR_MESSAGE}
    RETURN    ${msg}

Login With Credentials
    [Arguments]    ${username}    ${password}
    [Documentation]     Permet de loguer un utilisateur avec un son username, et son mot de passe
    Enter Username    ${username}
    Enter Password    ${password}
    Click Login Button

Inventory Should Be Visible
    [Documentation]     Permet de vérifier que l'url contient bien inventory.html
    Location Should Contain    inventory.html

Locked User Error Should Be Visible
    [Documentation]     Permet de vérifier qu'on affiche un message et un epic sadface
    ${msg}=    Get Error Message
    Should Contain    ${msg.lower()}    epic sadface: sorry, this user has been locked out.

Close Browser If Open
    [Documentation]     Permet de nettoyer le navigateur en fin de test
    Run Keyword And Ignore Error    Close Browser

# Keyword générique pour ouvrir le navigateur et se loguer à l'application
Open And Login
    [Arguments]    ${URL}    ${USER_NAME}    ${USER_PWD}
    [Documentation]     Permet d'ouvrir le navigateur et se loguer à l'application
    Open Browser    ${URL}    chrome    options=add_argument("--incognito")
    Login With Credentials    ${USER_NAME}     ${USER_PWD}
    Inventory Should Be Visible
