from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    # ── Locators ──────────────────────────────────
    ITEM_NAME     = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BTN  = (By.ID, "checkout")
    FIRST_NAME    = (By.ID, "first-name")
    LAST_NAME     = (By.ID, "last-name")
    POSTAL_CODE   = (By.ID, "postal-code")
    CONTINUE_BTN  = (By.ID, "continue")
    PAGE_TITLE    = (By.CLASS_NAME, "title")
    FINISH_BTN    = (By.ID, "finish")
    CONFIRM_MSG   = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def get_item_name(self):
        self.wait.until(EC.presence_of_element_located(self.ITEM_NAME))
        return self.driver.find_element(*self.ITEM_NAME).text

    def click_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()

    def fill_form(self, first, last, postal):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME)).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal)

    def click_continue(self):
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BTN)).click()

    def get_page_title(self):
        self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
        return self.driver.find_element(*self.PAGE_TITLE).text

    def click_finish(self):
        self.wait.until(EC.element_to_be_clickable(self.FINISH_BTN)).click()

    def get_confirmation(self):
        self.wait.until(EC.presence_of_element_located(self.CONFIRM_MSG))
        return self.driver.find_element(*self.CONFIRM_MSG).text
