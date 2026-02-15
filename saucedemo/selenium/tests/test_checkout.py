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

# Test du Happy Path
def test_checkout_complete_order(driver):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

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
def test_checkout_missing_info(driver):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")
    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Laisser les champs vides et cliquer sur Continue
    checkout_page.click_continue()

    # Vérifier le message d'erreur
    error_msg = checkout_page.get_error_message()
    assert "Error" in error_msg, f"Message d'erreur attendu, obtenu : {error_msg}"


# Test Cancel retourne au panier
def test_checkout_cancel_returns_to_cart(driver):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    page_inventory.add_item_to_cart("Sauce Labs Backpack")

    cart_page = page_inventory.go_to_cart()
    checkout_page = cart_page.click_checkout()

    # Cliquer sur Cancel
    checkout_page.click_cancel()

    # Vérifier qu'on est revenu sur la page du panier
    assert "cart.html" in driver.current_url, f"Devrait être sur cart.html, actuel : {driver.current_url}"
