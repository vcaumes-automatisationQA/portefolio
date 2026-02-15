# Liste des imports nécessaires pour faire fonctionner les TA: Playwright gestion des exceptions...
from playwright.sync_api import Page

# Description de la page de login et des méthodes asscociées
class LoginPage:
    # Liste des éléments de la page (button, champs textes...)
    def __init__(self, page: Page):
        self.page = page

        # Locators basés sur CSS / ID
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    # Méthode pour connecter un utilisateur à l'application
    def login(self, username, password):
        try:
            self.username_input.fill(username)
        except Exception:
            raise Exception("Erreur : champ 'username' non trouvé ou non interactif")

        try:
            self.password_input.fill(password)
        except Exception:
            raise Exception("Erreur : champ 'password' non trouvé ou non interactif")

        try:
            self.login_button.click()
        except Exception:
            raise Exception("Erreur : bouton 'login' non trouvé ou non cliquable")

    # Méthode pour récupérer le message d'erreur affiché
    def get_error_message(self):
        return self.error_message.text_content()