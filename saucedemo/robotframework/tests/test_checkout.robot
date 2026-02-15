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
${ITEM_NAME}    Sauce Labs Backpack
${USER_NAME}    standard_user
${USER_PWD}    secret_sauce

*** Test Cases ***

Checkout Complete Order
    [Documentation]     Test du happy path pour le checkout complete order
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # Aller au panier
    Go To Cart

    # Cliquer sur le bouton pour aller au Checkout
    Click Checkout

    # Remplir le formulaire
    Enter Firstname     ABDC
    Enter Lastname      efgh
    Enter Zipcode       33000

    # Appuyer sur le bouton Continue
    Click Continue Button

    # Appuyer sur le bouton Finish
    Click Finish Button

    # Vérifier le message de confirmation
    ${order_complete}=    Is Order Complete
    Should Be True    ${order_complete}

Checkout Missing Info
    [Documentation]     Test du checkout dans le cas où on n'a pas rempli les information du formulaire
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # Aller au panier
    Go To Cart

    # Cliquer sur le bouton pour aller au Checkout
    Click Checkout

    # Remplir le formulaire: Pas d'action

    # Appuyer sur le bouton Continue
    Click Continue Button

    ${error_message}=     Get Checkout Error Message
    Should Contain    ${error_message}    Error


Checkout Cancel And Return To Cart
    [Documentation]     Test du checkout dans le cas où on appuie sur le bouton 'Cancel'
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # Aller au panier
    Go To Cart

    # Cliquer sur le bouton pour aller au Checkout
    Click Checkout

    # Cliquer sur le bouton Cancel
    Click Cancel Button

    # Vérifier qu'on est revenu sur la page du panier
    Location Should Contain    cart.html