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

# Ajouter un article au panier
def test_add_one_item_to_cart(page):
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Aller au panier
    cart_page = page_inventory.go_to_cart()

    # On vérifie qu'il n'y a qu'un seul objet dans le panier
    assert len(cart_page.get_cart_items()) == 1

# Supprimer un article du panier
def test_remove_one_item_from_cart(page):
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Aller au panier
    cart_page = page_inventory.go_to_cart()

    # Suppression de l'article
    cart_page.remove_item_from_cart("Sauce Labs Backpack")

    # On vérifie qu'il n'y a plus d'objet dans le panier
    assert len(cart_page.get_cart_items()) == 0

# Ajouter et supprimer plusieurs articles dans le panier
def test_add_and_remove_all_items(page):
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    items = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    # Ajout des articles
    for item in items:
        page_inventory.add_item_to_cart(item)
    cart_page = page_inventory.go_to_cart()
    assert len(cart_page.get_cart_items()) == len(items)

    # Suppression des articles
    for item in items:
        cart_page.remove_item_from_cart(item)
    assert len(cart_page.get_cart_items()) == 0


# Aller au checkout
def test_go_to_checkout(page):
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")
    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Vérifier qu'on est bien redirigé vers l'url du Checkout
    assert "checkout-step-one" in page.url