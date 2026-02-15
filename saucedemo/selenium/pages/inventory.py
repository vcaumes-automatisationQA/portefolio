import time

from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.cart import CartPage

# Description de la page inventory.html et ses méthodes asscociées
class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.burger_menu_btn = (By.ID, "react-burger-menu-btn")
        self.logout_link = (By.ID, "logout_sidebar_link")

    # Méthode pour ajouter un article dans le panier
    def add_item_to_cart(self, item_name):
        # Attendre que l'élément à ajouter soit cliquable
        item = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
            )
        )
        # On vérifier qu'on a bien le texte "Add to cart"
        assert item.text == "Add to cart", f"Bouton inattendu : {item.text}"
        # On clique pour ajouter l'élément au panier
        item.click()

        # attendre que le bouton passe sur "Remove"
        self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            ).text == "Remove"
        )

        # assert sur le texte Remove du bouton
        button_text = self.driver.find_element(
            By.XPATH,
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        ).text
        assert button_text == "Remove", f"Le bouton pour '{item_name}' devrait être 'Remove' mais est '{button_text}'"

    # Méthode qui permet de supprimer un article du panier
    def remove_item_from_cart(self, item_name):
        # Attendre que le bouton Remove de cet item soit cliquable
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button")
            )
        )

        # Vérifier qu'on a bien le texte "Remove" avant le clic
        assert button.text == "Remove", f"Bouton inattendu avant clic : {button.text}"

        # Cliquer pour retirer l'article du panier
        button.click()

        # Attendre que le bouton repasse sur "Add to cart"
        self.wait.until(
            lambda d: d.find_element(
                By.XPATH,
                f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            ).text == "Add to cart"
        )

        # Assert final pour plus de clarté
        button_text = self.driver.find_element(
            By.XPATH,
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        ).text
        assert button_text == "Add to cart", f"Le bouton pour '{item_name}' devrait être 'Add to cart' mais est '{button_text}'"

    # Méthode pour récupérer le nombre d'article présent dans le panier
    def get_cart_badge(self):
        try:
            return self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        except NoSuchElementException:
            return "0"

    # Méthode pour aller au panier
    def go_to_cart(self):
        cart_icon = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )
        cart_icon.click()
        return CartPage(self.driver)

    # Méthode pour ouvrir le menu burger
    def open_burger_menu(self):
        for _ in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable(self.burger_menu_btn)).click()
                return
            except ElementClickInterceptedException:
                time.sleep(0.5)

        raise Exception("Impossible de cliquer sur le menu burger après plusieurs tentatives")

    # Méthode pour cliquer sur logout une fois que le menu burger est ouvert
    def logout(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.logout_link)).click()
        except Exception as e:
            self.driver.save_screenshot("logout_error.png")
            raise e