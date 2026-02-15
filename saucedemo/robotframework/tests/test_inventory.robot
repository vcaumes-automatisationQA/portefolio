*** Settings ***
Resource    ../pages/Login.resource
Resource    ../pages/inventory.resource
Library     SeleniumLibrary
Library    String
Library    OperatingSystem

*** Variables ***
${URL}    https://www.saucedemo.com/
${ITEM_NAME}    Sauce Labs Backpack
${USER_NAME}    standard_user
${USER_PWD}    secret_sauce

@{ITEM_LIST}
...    Sauce Labs Backpack
...    Sauce Labs Bike Light
...    Sauce Labs Bolt T-Shirt
...    Sauce Labs Fleece Jacket
...    Sauce Labs Onesie
...    Test.allTheThings() T-Shirt (Red)

*** Test Cases ***
Add One Item To Cart
    [Documentation]     Ajouter un article au panier, et vérifier le nombre d'article présent dans le panier est égal à 1 (badge du panier)

    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article depuis la page inventory
    Add Item From Inventory    ${ITEM_NAME}

    # Vérifier que le nombre d'article présent sur le bagde est égal à 1
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    1

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open

Remove One Item From Cart
    [Documentation]     Vérifier que si on a un article dans le panier et qu'on le supprime depuis la page inventory, le badge panier est égal à 0

    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article depuis la page inventory
    Add Item From Inventory    ${ITEM_NAME}

    # Vérifier que le badge du panier affiche '1'
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    1

    # Supprimer l'article du panier depuis la page inventory
    Remove Item From Inventory    ${ITEM_NAME}

    # Vérifier que le badge du panier est égal à 0 (car inexistant)
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    0

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open

Add And Remove All Items
    [Documentation]     Vérifier qu'on peut ajouter / supprimer tous les articles d'une liste, et s'assurer que le badge panier affiche un nombre cohérent

    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter tous les articles de la liste
    Add Multiple Items From Inventory   @{ITEM_LIST}

    # Vérifier le nombre d'articles dans le panier est bien égal à 6
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    6

    # Supprimer tous les articles de la liste
    Remove Multiple Items From Inventory   @{ITEM_LIST}

    # Vérifier le nombre d'articles dans le panier est bien égal à 0
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    0

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open