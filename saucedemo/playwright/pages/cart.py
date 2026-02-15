# Liste des imports nécessaires pour faire fonctionner les TA: Playwright
from playwright.sync_api import Page
from pages.checkout import CheckoutPage

# Description de la page cart.html et ses méthodes asscociées
class CartPage:
    def __init__(self, page: Page):
        self.page = page

        # Locators basés sur ID / Class
        self.checkout_btn = page.locator("#checkout")
        self.cart_items = page.locator(".cart_item")

    # Méthode qui permet de retourner la liste des objets type WebElements ajoutés
    def get_cart_items(self):
        # Retourne une liste d'objets Locator (un par élément)
        nb_car_items = self.cart_items.count()
        return [self.cart_items.nth(i) for i in range(nb_car_items)]

    # Méthode qui permet de retourner la liste des noms d'item ajoutés
    def get_cart_items_names(self):
        items = self.get_cart_items()
        return [item.locator(".inventory_item_name").text_content() for item in items]

    # Méthode qui permet d'aller sur la page de checkout
    def click_checkout(self):
        self.checkout_btn.click()
        return CheckoutPage(self.page)

    # Methode qui permet de retirer un élément du pannier
    def remove_item_from_cart(self, item_name):
        item_id = item_name.lower().replace(" ", "-")
        remove_btn = f"#remove-{item_id}"
        self.page.locator(remove_btn).click()
