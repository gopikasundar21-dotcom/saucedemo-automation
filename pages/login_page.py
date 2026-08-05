from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # ── Locators ──────────────────────────────────
    USERNAME  = (By.ID, "user-name")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CLASS_NAME, "error-message-container")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://www.saucedemo.com")
        # Wait until login button is visible before proceeding
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN))

    def login(self, username, password):
        self.wait.until(EC.element_to_be_clickable(self.USERNAME)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()

    def get_error_message(self):
        self.wait.until(EC.visibility_of_element_located(self.ERROR_MSG))
        return self.driver.find_element(*self.ERROR_MSG).text
