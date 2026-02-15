*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${FIRST_NAME}       id=first-name
${LAST_NAME}        id=last-name
${POSTAL_CODE}     id=postal-code
${CONTINUE}         id=continue
${FINISH}           id=finish
${CANCEL}           id=cancel
${ERROR_MESSAGE_CONTAINER}   css=.error-message-container
${COMPLETE_HEADER}   css=.complete-header

*** Keywords ***
Enter Firstname
    [Documentation]     Permet de remplir le champs prénom dans le formulaire
    [Arguments]    ${data}
    Wait Until Page Contains Element      ${FIRST_NAME}    timeout=15s
    Click Element   ${FIRST_NAME}
    Input Text    ${FIRST_NAME}    ${data}

Enter Lastname
    [Documentation]     Permet de remplir le champs nom de famille
    [Arguments]    ${data}
    Wait Until Page Contains Element    ${LAST_NAME}    timeout=10s
    Input Text    ${LAST_NAME}    ${data}

Enter Zipcode
    [Documentation]     Permet de remplir le champs code postal
    [Arguments]    ${data}
    Wait Until Page Contains Element    ${POSTAL_CODE}    timeout=10s
    Input Text    ${POSTAL_CODE}    ${data}

Click Continue Button
    [Documentation]     Permet de cliquer sur le bouton 'Continue'
    Click Button    ${CONTINUE}

Click Finish Button
    [Documentation]     Permet de cliquer sur le bouton 'Finish'
    Click Button    ${FINISH}

Click Cancel Button
    [Documentation]     Permet de cliquer sur le bouton 'Cancel'
    Click Button    ${CANCEL}


Get Checkout Error Message
    [Documentation]    Récupère le texte du message d'erreur s'il existe, sinon retourne une chaîne vide
    ${is_visible}=    Run Keyword And Return Status    Element Should Be Visible    css=.error-message-container
    IF    ${is_visible}
        ${msg}=    Get Text    css=.error-message-container
    ELSE
        ${msg}=    Set Variable    ${EMPTY}
    END
    RETURN    ${msg}

Is Order Complete
    [Documentation]    Vérifie si le message "THANK YOU FOR YOUR ORDER" est affiché
    ${is_visible}=    Run Keyword And Return Status    Element Should Be Visible    css=.complete-header
    RETURN    ${is_visible}
