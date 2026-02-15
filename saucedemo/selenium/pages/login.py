# Liste des imports nécessaires pour faire fonctionner les TA: Selenium, gestion des exceptions...
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Description de la page de login et des méthodes asscociées
class LoginPage:
    # Liste des éléments de la page (button, champs textes...)
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Sélecteurs des éléments sur la page par ID
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.CSS_SELECTOR, "h3[data-test='error']")  # optionnel

    # Méthode qui permet de fermer la modale qui s'ouvre pour enregistrer le mot de passe lors du login de l'utilisateur
    def close_password_modal(driver):
        try:
            close_btn = driver.find_element(By.CLASS_NAME, "close-button")  # exemple
            close_btn.click()
        except NoSuchElementException:
            pass  # pas de popup → rien à faire

    # Méthode pour connecter un utilisateur à l'application
    def login(self, username, password):
        # On met les éléments et leurs noms dans une liste
        elements = [
            (self.username_input, "username"),
            (self.password_input, "password"),
            (self.login_button, "login button")
        ]

        try:
            for locator, name in elements:
                # On attend que l'élément soit visible/cliquable selon le type
                if name == "login button":
                    # Lorsque l'élément est présent, on clique dessus
                    self.wait.until(EC.element_to_be_clickable(locator)).click()
                else:
                    # Lorsque l'élément est présent, on rempli avec l'information passée en paramètre
                    self.wait.until(EC.visibility_of_element_located(locator)).send_keys(
                        username if name == "username" else password)
        # Gestion de l'exception si un élément du DOM n'est pas visible ou cliquable
        except TimeoutException as e:
            # Message clair sur quel champ a échoué
            raise TimeoutException(f"Erreur : l'élément '{name}' n'a pas été trouvé ou cliquable") from e

    # Méthode pour récupérer le message d'erreur affiché
    def get_error_message(self):
        return self.driver.find_element(*self.error_message).text