# Liste des imports nécessaires pour faire fonctionner les TA: Playwright
from playwright.sync_api import Page
from pages.cart import CartPage


# Description de la page inventory.html et ses méthodes asscociées
class InventoryPage:
    def __init__(self, page: Page):
        self.page = page

        # Locators basés sur ID / Class
        self.burger_menu_btn = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.shopping_cart_badge = page.locator(".shopping_cart_badge")
        self.shopping_cart_link = page.locator(".shopping_cart_link")
        self.logout_link = page.locator("#logout_sidebar_link")

    # Méthode pour ajouter un article dans le panier
    def add_item_to_cart(self, item_name):

        # Localiser le bouton "Add to cart" pour l'article
        item_button = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )

        # On vérifier qu'on a bien le texte "Add to cart"
        button_text = item_button.text_content()
        assert button_text == "Add to cart", f"Bouton inattendu : {button_text}"

        # On clique pour ajouter l'élément au panier
        item_button.click()

        # Récupération du bouton qui se trouve sur l'article
        item_button = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )

        # On vérifier qu'on a bien le texte "Remove"
        button_text = item_button.text_content()
        assert button_text == "Remove", f"Bouton inattendu : {button_text}"

    # Méthode qui permet de supprimer un article du panier
    def remove_item_from_cart(self, item_name):
        # Récupération du bouton qui se trouve sur l'article
        item_button = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )

        # On vérifier qu'on a bien le texte "Remove"
        button_text = item_button.text_content()
        assert button_text == "Remove", f"Bouton inattendu : {button_text}"

        # Cliquer pour retirer l'article du panier
        item_button.click()

        # Récupération du bouton qui se trouve sur l'article
        item_button = self.page.locator(
            f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        )

        # On vérifier qu'on a bien le texte "Add to cart"
        button_text = item_button.text_content()
        assert button_text == "Add to cart", f"Bouton inattendu : {button_text}"

    # Méthode pour récupérer le nombre d'article présent dans le panier
    def get_cart_badge(self):
        badge = self.page.locator(".shopping_cart_badge")
        if badge.count() == 0:
            return "0"
        return badge.text_content() or "0"

    # Méthode pour aller au panier
    def go_to_cart(self):
        self.shopping_cart_link.click()
        return CartPage(self.page)

    # Méthode pour ouvrir le menu burger
    def open_burger_menu(self):
        self.burger_menu_btn.click()

    # Méthode pour cliquer sur logout une fois que le menu burger est ouvert
    def logout(self):
        try:
            self.logout_link.click()
        except Exception as e:
            # capture le screenshot complet de la page
            self.page.screenshot(path="logout_error.png")
            raise e