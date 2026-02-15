import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By

from pages.login import LoginPage
from pages.inventory import InventoryPage

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

def test_add_one_item_to_cart(driver):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "1"

def test_remove_one_item_from_cart(driver):
    # initialisation du test: on va sur la page 'www.saucedemo.com'
    driver.get("https://www.saucedemo.com")
    # on se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # on instancie la page inventory
    page_inventory = InventoryPage(driver)

    item_name = "Sauce Labs Backpack"

    # Ajouter l'article
    page_inventory.add_item_to_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "1"

    # Supprimer l'article
    page_inventory.remove_item_from_cart(item_name)

    # Vérifier le badge
    assert page_inventory.get_cart_badge() == "0"

def test_add_and_remove_all_items(driver):
    driver.get("https://www.saucedemo.com")

    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)

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