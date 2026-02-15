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
        browser = p.chromium.launch(headless=False)
        # Nouveau contexte → équivalent incognito
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


def test_logout_standard(page):
    page.goto("https://www.saucedemo.com")

    # On se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # On instancie la page inventory
    page_inventory = InventoryPage(page)

    # On ouvre le menu burger
    page_inventory.open_burger_menu()

    # On clique sur le logout
    page_inventory.logout()

    # Vérifier la présence du bouton de login
    assert page.locator("#login-button").is_visible()

    # Vérifier la redirection vers l'URL qui correspond à la page de login du site
    assert page.url == "https://www.saucedemo.com/"


def test_inventory_not_accessible_after_logout(page):
    page.goto("https://www.saucedemo.com")

    # On se logue avec l'utilisateur standard
    login = LoginPage(page)
    login.login("standard_user", "secret_sauce")

    # On instancie la page inventory
    page_inventory = InventoryPage(page)

    # On ouvre le menu burger
    page_inventory.open_burger_menu()

    # On clique sur le logout
    page_inventory.logout()

    # On essaie d'accèder à la page invertory.html
    page.goto("https://www.saucedemo.com/inventory.html")

    # On vérifie qu'on est bien redirigé vers la page de login (même test qu'en fin de méthode test_logout_standard)
    assert page.locator("#login-button").is_visible()
    assert page.url == "https://www.saucedemo.com/"
