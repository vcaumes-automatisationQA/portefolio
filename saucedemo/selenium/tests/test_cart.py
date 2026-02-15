import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from pages.login import LoginPage
from pages.inventory import InventoryPage
from pages.cart import CartPage

@pytest.fixture
def driver():
    # Choisir le navigateur, ici Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-password-manager-reauthentication")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("--user-data-dir=/tmp/temp_chrome_profile")
    driver = webdriver.Chrome(options=options)

    yield driver  # fournit le driver au test

    driver.quit()  # ferme le navigateur après le test

# Ajouter un article au panier
def test_add_one_item_to_cart(driver):
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Aller au panier
    cart_page = page_inventory.go_to_cart()

    # On vérifie qu'il n'y a qu'un seul objet dans le panier
    assert len(cart_page.get_cart_items()) == 1

# Supprimer un article du panier
def test_remove_one_item_from_cart(driver):
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

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
def test_add_and_remove_all_items(driver):
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

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
def test_go_to_checkout(driver):
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")
    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Vérifier qu'on est bien redirigé vers l'url du Checkout
    assert "checkout-step-one" in driver.current_url