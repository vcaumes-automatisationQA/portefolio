import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from selenium import webdriver
import pytest
from pages.login import LoginPage

USERS_LIST = {
    "standard_user": "secret_sauce",
    "locked_out_user": "secret_sauce",
    "problem_user": "secret_sauce",
    "performance_glitch_user": "secret_sauce",
    "error_user": "secret_sauce",
    "visual_user": "secret_sauce"
}


@pytest.fixture
def driver():
    # Choisir le navigateur, ici Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.mark.parametrize("username", USERS_LIST.keys())
def test_login_users(driver, username):
    driver.get("https://www.saucedemo.com")
    page = LoginPage(driver)

    page.login(username, USERS_LIST[username])

    if username in ["standard_user", "problem_user", "visual_user", "performance_glitch_user", "error_user"]:
        assert "inventory.html" in driver.current_url
    elif username == "locked_out_user":
        error_text = page.get_error_message()
        assert "epic sadface: sorry, this user has been locked out." in error_text.lower()

def test_login_invalid(driver):
    driver.get("https://www.saucedemo.com")
    page = LoginPage(driver)
    page.login("wrong_user", "wrong_password")
    error_text = page.get_error_message()
    assert "epic sadface: username and password do not match any user in this service" in error_text.lower()
