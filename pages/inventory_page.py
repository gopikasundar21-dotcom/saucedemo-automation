from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    # ── Locators ──────────────────────────────────
    ADD_BACKPACK  = (By.ID, "add-to-cart-sauce-labs-backpack")
    CART_BADGE    = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK     = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BTN      = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK   = (By.ID, "logout_sidebar_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def add_backpack_to_cart(self):
        # Remove item first if already in cart (shared session state)
        try:
            remove_btn = self.driver.find_element(
                By.ID, "remove-sauce-labs-backpack"
            )
            remove_btn.click()
        except:
            pass
        # Now add to cart
        self.wait.until(EC.element_to_be_clickable(self.ADD_BACKPACK)).click()

    def get_cart_count(self):
        self.wait.until(EC.presence_of_element_located(self.CART_BADGE))
        return self.driver.find_element(*self.CART_BADGE).text

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()

    def logout(self):
        self.wait.until(EC.element_to_be_clickable(self.MENU_BTN)).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()
