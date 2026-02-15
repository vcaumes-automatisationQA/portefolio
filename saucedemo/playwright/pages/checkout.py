# Liste des imports nécessaires pour faire fonctionner les TA: Playwright
from playwright.sync_api import Page

class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.first_name_input = page.locator("#first-name")
        self.last_name_input = page.locator("#last-name")
        self.zip_input = page.locator("#postal-code")
        self.continue_btn = page.locator("#continue")
        self.finish_btn = page.locator("#finish")
        self.cancel_btn = page.locator("#cancel")
        self.error_msg = page.locator(".error-message-container")
        self.thank_you_msg = "h2.complete-header"

    # Remplir les champs
    def fill_first_name(self, name):
        self.first_name_input.fill(name)

    def fill_last_name(self, name):
        self.last_name_input.fill(name)

    def fill_zip(self, zip_code):
        self.zip_input.fill(zip_code)

    # Cliquer sur Continue
    def click_continue(self):
        self.continue_btn.click()

    # Cliquer sur Finish
    def click_finish(self):
        self.finish_btn.click()

    # Cliquer sur Cancel
    def click_cancel(self):
        self.cancel_btn.click()

    # Récupérer le message d'erreur (s'il y en a)
    def get_error_message(self):
        return self.error_msg.text_content() or ""

    # Vérifier si le message "THANK YOU FOR YOUR ORDER" est présent
    def is_order_complete(self):
        return self.page.locator(self.thank_you_msg).is_visible()
