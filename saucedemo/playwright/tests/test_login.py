import sys
from pathlib import Path

# Ajouter le chemin racine du projet au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pytest
from playwright.sync_api import sync_playwright
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
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # Nouveau contexte → équivalent incognito
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


@pytest.mark.parametrize("username", USERS_LIST.keys())
def test_login_users(page, username):
    page.goto("https://www.saucedemo.com")
    login_page = LoginPage(page)

    login_page.login(username, USERS_LIST[username])

    if username in ["standard_user", "problem_user", "visual_user", "performance_glitch_user", "error_user"]:
        assert "inventory.html" in page.url
    elif username == "locked_out_user":
        error_text = login_page.get_error_message()
        assert "epic sadface: sorry, this user has been locked out." in error_text.lower()

def test_login_invalid(page):
    page.goto("https://www.saucedemo.com")
    login_page = LoginPage(page)
    login_page.login("wrong_user", "wrong_password")
    error_text = login_page.get_error_message()
    assert "epic sadface: username and password do not match any user in this service" in error_text.lower()
