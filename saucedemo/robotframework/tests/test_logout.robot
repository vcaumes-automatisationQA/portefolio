*** Settings ***
Resource    ../pages/Login.resource
Resource    ../pages/inventory.resource
Resource    ../pages/cart.resource
Resource    ../pages/checkout.resource

Library     SeleniumLibrary
Library    String
Library    OperatingSystem

*** Variables ***
${URL}    https://www.saucedemo.com/
${INVENTORY_URL}  https://www.saucedemo.com/inventory.html
${ITEM_NAME}    Sauce Labs Backpack
${USER_NAME}    standard_user
${USER_PWD}    secret_sauce

*** Test Cases ***

Logout Standard
    [Documentation]     Test du happy path pour l'action de logout standard depuis la page inventory.html
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # On ouvre le menu burger
    Open Burger Menu

    # On clique sur le logout
    Logout

    # Vérifier que le bouton login est affiché
    Element Should Be Visible    id:login-button

    # Vérifier que l'URL est correcte
    Location Should Be    ${URL}


Inventory Not Accessible After Logout
    [Documentation]     Vérifier que l'on ne peut pas accèder à la page inventory.html après s'être délogué et qu'on est redirigé vers la page de login
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # On ouvre le menu burger
    Open Burger Menu

    # On clique sur le logout
    Logout

    # On essaie d'accèder à la page invertory.html
    Go To    ${INVENTORY_URL}

    # Attendre que le bouton login soit visible (max 5 secondes)
    Wait Until Element Is Visible    id:login-button    5s

    # Maintenant on peut vérifier l'URL
    Location Should Be    ${URL}
