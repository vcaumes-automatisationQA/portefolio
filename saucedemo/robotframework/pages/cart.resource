*** Settings ***
Library    SeleniumLibrary
Library    String
Library    BuiltIn
Library    Collections

*** Variables ***
${CHECKOUT}        id=checkout
${CART_ITEM}       css=.cart_item
${CART_ITEM_NAME}  css=.inventory_item_name

# Définition des méthodes associée à la ressource cart
*** Keywords ***

Get Cart Items Number
    [Documentation]     permet de retourner le nombre d'article présent dans le panier

    ${count}=    Get Element Count    ${CART_ITEM}
    RETURN      ${count}

Get Cart Items Names
    [Documentation]     Permet de retourner la liste des noms des articles présents dans le panier

    @{elements}=    Get WebElements    ${CART_ITEM_NAME}
    @{items}=       Create List
    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        Append To List   ${items}    ${text}
    END
    RETURN    @{items}

Click Checkout
    [Documentation]     Permet d'aller sur la page de checkout

    # Attendre que le bouton de checkout soit visible et disponible
    Wait Until Element Is Visible    ${CHECKOUT}    timeout=10s
    Wait Until Element Is Enabled    ${CHECKOUT}    timeout=10s

    # Cliquer sur le bouton checkout
    Click Element    ${CHECKOUT}

Remove Item From Cart
    [Arguments]    ${item_name}
    [Documentation]     Permet de retirer un élément du pannier depuis la page du panier

    # Transformer le nom de l'article en ID (minuscule + tirets)
    ${item_id}=    Convert To Lower Case    ${item_name}
    ${item_id}=    Replace String    ${item_id}    ${SPACE}    -

    # Construire le locator du bouton Remove
    ${locator}=    Set Variable    id=remove-${item_id}

    # Attendre que le bouton soit visible et cliquable, puis cliquer
    Wait Until Element Is Visible    ${locator}    timeout=10s
    Wait Until Element Is Enabled    ${locator}    timeout=10s
    Click Element    ${locator}

Remove Multiple Items From Cart
    [Arguments]    @{items}
    [Documentation]    Supprimer tous les articles d'une liste d'articles passée en paramètre depuis le panier

    FOR    ${item}    IN    @{items}
        Remove Item From Cart    ${item}
    END

Cart Should Be Empty
    [Documentation]    Vérifier que le panier est vide

    # Vérifier qu'il n'y pas d'éléments sur la page de classe .cart_item et .shopping_cart_badge
    Page Should Not Contain Element    css:.cart_item
    Page Should Not Contain Element    css:.shopping_cart_badge