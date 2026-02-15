import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from playwright.sync_api import sync_playwright

from pages.login import LoginPage
from pages.inventory import InventoryPage

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        # Nouveau contexte → équivalent incognito
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_add_one_item_to_cart(page):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "1"

def test_remove_one_item_from_cart(page):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    page.goto("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(page)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "1"

    # Supprimer l'article
    page_inventory.remove_item_from_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "0"

def test_add_and_remove_all_items(page):
    page.goto("https://www.saucedemo.com")

    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)

    items = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]

    # Ajouter tous les items un par un
    for index, item in enumerate(items, start=1):
        inventory.add_item_to_cart(item)
        # Vérifier que le badge est correct
        assert inventory.get_cart_badge() == str(index)

    # Retirer tous les items un par un
    for index, item in enumerate(items, start=1):
        inventory.remove_item_from_cart(item)
        # Vérifier que le badge diminue
        expected_badge = str(len(items) - index)
        assert inventory.get_cart_badge() == expected_badge