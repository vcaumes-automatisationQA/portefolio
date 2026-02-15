from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.checkout import CheckoutPage

# Description de la page cart.html et ses méthodes asscociées
class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.checkout_btn = (By.ID, "checkout")
        self.cart_items = (By.CLASS_NAME, "cart_item")

    # Méthode qui permet de retourner la liste des objets type WebElements ajoutés
    def get_cart_items(self):
        return self.driver.find_elements(*self.cart_items)

    # Méthode qui permet de retourner la liste des noms d'item ajoutés
    def get_cart_items_names(self):
        items = self.get_cart_items()
        return [item.find_element(By.CLASS_NAME, "inventory_item_name").text for item in items]

    # Méthode qui permet d'aller sur la page de checkout
    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.checkout_btn)).click()
        return CheckoutPage(self.driver)

    # Methode qui permet de retirer un élément du pannier
    def remove_item_from_cart(self, item_name):
        item_id = item_name.lower().replace(" ", "-")
        remove_btn = (By.ID, f"remove-{item_id}")
        self.wait.until(EC.element_to_be_clickable(remove_btn)).click()
