*** Settings ***
Resource    ../pages/Login.resource
Resource    ../pages/inventory.resource
Resource    ../pages/cart.resource

Library     SeleniumLibrary
Library    String
Library    OperatingSystem

*** Variables ***
${URL}    https://www.saucedemo.com/
${ITEM_NAME}    Sauce Labs Backpack
${USER_NAME}    standard_user
${USER_PWD}    secret_sauce
${SHOPPING_CART_BADGE}  css=.shopping_cart_badge

@{ITEM_LIST}
...    Sauce Labs Backpack
...    Sauce Labs Bike Light
...    Sauce Labs Bolt T-Shirt
...    Sauce Labs Fleece Jacket
...    Sauce Labs Onesie
...    Test.allTheThings() T-Shirt (Red)

*** Test Cases ***

Add One Item To Cart
    [Documentation]     Ajouter un article au panier, et vérifier le nombre d'article présent dans le panier et le nom de l'article ajouté
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    Add Item From Inventory    ${ITEM_NAME}
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    1

    # Aller au panier
    Go To Cart

    # On vérifie qu'il n'y a qu'un seul objet dans le panier
    ${nb_cart_items}=       Get Cart Items Number
    Should Be Equal As Integers    ${nb_cart_items}    1

    # Vérifier que le nom de l'article présent dans le panier égal au nom de l'article ajouté
    ${cart_items_names}=     Get Cart Items Names
    ${first_item}=    Get From List    ${cart_items_names}    0
    Should Be Equal    ${first_item}    ${ITEM_NAME}

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open

Remove One Item From Cart
    [Documentation]     Ajouter un article au panier, supprimer l'article depuis le panier et vérifier que le panier est vide

    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    Add Item From Inventory    ${ITEM_NAME}
    ${nb_items}=    Get Cart Badge
    Should Be Equal As Integers    ${nb_items}    1

    # Aller au panier
    Go To Cart

    # Vérifier qu'il n'y a bien un objet dans le panier
    ${nb_cart_items}=       Get Cart Items Number
    Should Be Equal As Integers    ${nb_cart_items}    1

    # Supprimer l'article du panier
    Remove Item From Cart    ${ITEM_NAME}

    # Vérifier que le panier est vide
    Cart Should Be Empty

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open

Add And Remove All Items
    [Documentation]     Ajouter tous les items d'une liste depuis la page inventory, aller au panier, supprimer tous les articles depuis le panier

    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter tous les articles de la liste
    Add Multiple Items From Inventory   @{ITEM_LIST}

    # Aller au panier
    Go To Cart

    # Vérifier que le nombre d'articles présents dans le panier = longuer de ma liste
    ${nb_cart_items}=       Get Cart Items Number
    ${nb_items}=    Get Length    ${ITEM_LIST}
    Should Be Equal As Integers    ${nb_cart_items}    ${nb_items}

    # Ajouter tous les articles de la liste depuis le panier
    Remove Multiple Items From Cart    @{ITEM_LIST}

    # On vérifier que le panier est vide
    Cart Should Be Empty

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open

Go To Checkout
    [Documentation]     Aller au checkout et vérifier qu'on est bien redirigé vers l'url du Checkout
    # Se loguer à l'application
    Open And Login    ${URL}   ${USER_NAME}     ${USER_PWD}

    # Ajouter un article
    Add Item From Inventory    ${ITEM_NAME}

    # Aller au panier
    Go To Cart

    # Cliquer sur le bouton pour aller au Checkout
    Click Checkout

    # Vérifier qu'on est bien redirigé vers l'url du Checkout
    Location Should Contain    checkout-step-one

    # Fermer automatiquement le navigateur à la fin de ce test, même si une vérification échoue
    [Teardown]    Close Browser If Open