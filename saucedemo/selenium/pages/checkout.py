from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators
        self.first_name_input = (By.ID, "first-name")
        self.last_name_input = (By.ID, "last-name")
        self.zip_input = (By.ID, "postal-code")
        self.continue_btn = (By.ID, "continue")
        self.finish_btn = (By.ID, "finish")
        self.cancel_btn = (By.ID, "cancel")
        self.error_msg = (By.CLASS_NAME, "error-message-container")
        self.thank_you_msg = (By.CLASS_NAME, "complete-header")

    # Remplir les champs
    def fill_first_name(self, name):
        self.wait.until(EC.visibility_of_element_located(self.first_name_input)).send_keys(name)

    def fill_last_name(self, name):
        self.wait.until(EC.visibility_of_element_located(self.last_name_input)).send_keys(name)

    def fill_zip(self, zip_code):
        self.wait.until(EC.visibility_of_element_located(self.zip_input)).send_keys(zip_code)

    # Cliquer sur Continue
    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.continue_btn)).click()

    # Cliquer sur Finish
    def click_finish(self):
        self.wait.until(EC.element_to_be_clickable(self.finish_btn)).click()

    # Cliquer sur Cancel
    def click_cancel(self):
        self.wait.until(EC.element_to_be_clickable(self.cancel_btn)).click()

    # Récupérer le message d'erreur (s'il y en a)
    def get_error_message(self):
        try:
            return self.driver.find_element(*self.error_msg).text
        except:
            return ""

    # Vérifier si le message "THANK YOU FOR YOUR ORDER" est présent
    def is_order_complete(self):
        try:
            return self.driver.find_element(*self.thank_you_msg).is_displayed()
        except:
            return False
