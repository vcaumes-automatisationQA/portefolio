import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from playwright.sync_api import sync_playwright

from pages.login import LoginPage
from pages.inventory import InventoryPage
from pages.cart import CartPage

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Nouveau contexte → équivalent incognito
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

# Test du Happy Path
def test_checkout_complete_order(page):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    # Ajouter un article au panier
    page_inventory.add_item_to_cart("Sauce Labs Backpack")
    cart_page = page_inventory.go_to_cart()

    # Aller à checkout
    checkout_page = cart_page.click_checkout()

    # Remplir le formulaire
    checkout_page.fill_first_name("ABCD")
    checkout_page.fill_last_name("efgh")
    checkout_page.fill_zip("33000")

    checkout_page.click_continue()
    checkout_page.click_finish()

    # Vérifier le message de confirmation, sinon on affiche le message "La commande n'a pas été complétée correctement"
    assert checkout_page.is_order_complete(), "La commande n'a pas été complétée correctement"


# Test checkout des champs vides
def test_checkout_missing_info(page):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")
    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Laisser les champs vides et cliquer sur Continue
    checkout_page.click_continue()

    # Vérifier le message d'erreur
    error_msg = checkout_page.get_error_message()
    assert "Error" in error_msg, f"Message d'erreur attendu, obtenu : {error_msg}"


# Test Cancel retourne au panier
def test_checkout_cancel_returns_to_cart(page):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")

    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Cliquer sur Cancel
    checkout_page.click_cancel()

    # Vérifier qu'on est revenu sur la page du panier
    assert "cart.html" in page.url, f"Devrait être sur cart.html, actuel : {page.url}"
