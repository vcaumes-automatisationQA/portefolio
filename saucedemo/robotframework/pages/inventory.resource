*** Settings ***
Library    SeleniumLibrary
Library    String

*** Variables ***
${LOGOUT_LINK}              id=logout_sidebar_link
${BURGER_MENU_BOUTON}       id=react-burger-menu-btn
${SHOPPING_CART_BADGE}      css=.shopping_cart_badge
${SHOPPING_CART_LINK}   css=.shopping_cart_link

# Définition des méthodes associée à ma ressource inventory
*** Keywords ***

Add Item From Inventory
    [Arguments]    ${item_name}
    [Documentation]    Ajouter un article passé en paramètre au panier et vérifier le label du bouton avant et après l'ajout

    # Attendre que le bouton associé à l'item à ajouter au panier soit visible et clickable sur la page,
    ${locator}=    Set Variable    xpath=//div[text()='${item_name}']/ancestor::div[@class='inventory_item']//button
    Wait Until Element Is Visible    ${locator}    timeout=10s
    Wait Until Element Is Enabled    ${locator}    timeout=10s

    # Récupérer son label du bouton associé à l'item à ajouter au panier
    ${text}=    Get Text    ${locator}
    ${text}=    Strip String    ${text}
    # Log To Console    Valeur du bouton: "${text}"
    # On vérifie que c'est bien le label "Add to cart" qui est affiché
    Should Be Equal    ${text}    Add to cart    Bouton inattendu : ${text}
    # Appuyer sur le bouton pour ajouter l'article au panier
    Click Element    ${locator}

    # Vérifier que le label du bouton passe bien à "Remove"
    ${locator}=    Set Variable    xpath=//div[text()='${item_name}']/ancestor::div[@class='inventory_item']//button
    Wait Until Element Is Visible    ${locator}    timeout=10s
    Wait Until Element Is Enabled    ${locator}    timeout=10s

    # Récupérer son label du bouton associé à l'item à ajouter au panier
    ${text}=    Get Text    ${locator}
    ${text}=    Strip String    ${text}
    # Log To Console    Valeur du bouton: "${text}"
    # Vérifier que c'est bien le label "Remove" qui est affiché
    Should Be Equal    ${text}    Remove    Bouton inattendu : ${text}

Remove Item From Inventory
    [Arguments]    ${item_name}
    [Documentation]    Supprimer un article passé en paramètre au panier et vérifier le label du bouton avant et après l'ajout

    # Attendre que le bouton associé à l'item à supprimer du panier soit visible et clickable sur la page,
    ${locator}=    Set Variable    xpath=//div[text()='${item_name}']/ancestor::div[@class='inventory_item']//button
    Wait Until Element Is Visible    ${locator}    timeout=10s
    Wait Until Element Is Enabled    ${locator}    timeout=10s

    # Récupérer le label du bouton associé à l'item à supprimer au panier
    ${text}=    Get Text    ${locator}
    # Vérifier que c'est bien le label "Remove" qui est affiché
    Should Be Equal    ${text}    Remove    Bouton inattendu : ${text}
    # Appuyer sur le bouton pour supprimer l'article du panier
    Click Element    ${locator}

    # Vérifier que le label du bouton passe bien à "Add to Cart"
    ${locator}=    Set Variable    xpath=//div[text()='${item_name}']/ancestor::div[@class='inventory_item']//button
    Wait Until Element Is Visible    ${locator}    timeout=10s
    Wait Until Element Is Enabled    ${locator}    timeout=10s

    # Récupérer son label du bouton associé à l'item à ajouter au panier
    ${text}=    Get Text    ${locator}
    # Vérifier que c'est bien le label "Add to cart" qui est affiché
    Should Be Equal    ${text}    Add to cart    Bouton inattendu : ${text}

Add Multiple Items From Inventory
    [Arguments]    @{items}
    [Documentation]    Ajouter tous les articles d'une liste d'articles passée en paramètre depuis la page inventory
    FOR    ${item}    IN    @{items}
        Add Item From Inventory    ${item}
    END

Remove Multiple Items From Inventory
    [Arguments]    @{items}
    [Documentation]    Supprimer tous les articles d'une liste d'articles passée en paramètre depuis la page inventory
    FOR    ${item}    IN    @{items}
        Remove Item From Inventory    ${item}
    END

Get Cart Badge
    [Documentation]    Permet de retourner le nombre d'article présent dans le panier
    # Vérifier que l'élément panier (bagde) existe sur la page, sinon on retourne '0'
    ${exists}=    Run Keyword And Return Status    Page Should Contain Element    ${SHOPPING_CART_BADGE}

    # Si l'élément badge panier n'existe pas, alors on retourne 0
    IF    not ${exists}
        RETURN    0
    END

    # Attendre que l'élément 'shopping cart list' soit présent sur la page (visible et disponible)
    Wait Until Element Is Visible    ${SHOPPING_CART_BADGE}    timeout=10s
    Wait Until Element Is Enabled    ${SHOPPING_CART_BADGE}    timeout=10s

    # Récupérer le nombre d'élément dans le panier
    ${text}=    Get Text    ${SHOPPING_CART_BADGE}
    ${text}=    Strip String    ${text}

    # Gestion du cas particulier ou le panier existe mais le nombre dans le panier est vide
    IF    '${text}' == ''
        RETURN    0
    END

    # Retourner le nombre d'article présent dans le panier (après conversion en entier)
    ${nb_items}=    Convert To Integer    ${text}
    RETURN    ${nb_items}

Go To Cart
    [Documentation]    Permet d'aller sur la page du panier
    # Attendre que l'élément 'panier' soit présent sur la page (visible et disponible)
    Wait Until Element Is Visible    ${SHOPPING_CART_LINK}    timeout=10s
    Wait Until Element Is Enabled    ${SHOPPING_CART_LINK}    timeout=10s

    # Cliquer sur le bouton pour aller sur le panier
    Click Element    ${SHOPPING_CART_LINK}

Open Burger Menu
    [Documentation]    Ouvrir le menu burger
    # Attendre que l'élément menu burger (visible et disponible)
    Wait Until Element Is Visible    ${BURGER_MENU_BOUTON}    timeout=10s
    Wait Until Element Is Enabled    ${BURGER_MENU_BOUTON}    timeout=10s

    # Cliquer sur le menu burger
    Click Element    ${BURGER_MENU_BOUTON}

Logout
    [Documentation]    Se déloguer de l'application
    # Attendre que le bouton logout (visible et disponible)
    Wait Until Element Is Visible    ${LOGOUT_LINK}    timeout=10s
    Wait Until Element Is Enabled    ${LOGOUT_LINK}    timeout=10s

    # Cliquer sur le bouton logout
    Click Element    ${LOGOUT_LINK}