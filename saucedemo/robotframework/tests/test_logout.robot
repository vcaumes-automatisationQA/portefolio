import sys
from pathlib import Path

from selenium.webdriver.common.by import By

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from selenium import webdriver
import pytest
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


def test_logout_standard(driver):
    driver.get("https://www.saucedemo.com")

    # On se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # On instancie la page inventory
    page_inventory = InventoryPage(driver)

    # On ouvre le menu burger
    page_inventory.open_burger_menu()

    # On clique sur le logout
    page_inventory.logout()

    # Vérifier la présence du bouton de login
    assert driver.find_element(By.ID, "login-button").is_displayed()

    # Vérifier la redirection vers l'URL qui correspond à la page de login du site
    assert driver.current_url == "https://www.saucedemo.com/"


def test_inventory_not_accessible_after_logout(driver):
    driver.get("https://www.saucedemo.com")

    # On se logue avec l'utilisateur standard
    login = LoginPage(driver)
    login.login("standard_user", "secret_sauce")

    # On instancie la page inventory
    page_inventory = InventoryPage(driver)

    # On ouvre le menu burger
    page_inventory.open_burger_menu()

    # On clique sur le logout
    page_inventory.logout()

    # On essaie d'accèder à la page invertory.html
    driver.get("https://www.saucedemo.com/inventory.html")

    # On vérifie qu'on est bien redirigé vers la page de login (même test qu'en fin de méthode test_logout_standard)
    assert driver.find_element(By.ID, "login-button").is_displayed()
    assert driver.current_url == "https://www.saucedemo.com/"
