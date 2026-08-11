import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.data_reader import read_excel_data


# ── Helper: reusable login ───────────────────────────
def do_login(driver):
    driver.delete_all_cookies()
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")
    WebDriverWait(driver, 30).until(
        lambda d: "inventory" in d.current_url
    )


# ══════════════════════════════════════════════════
# SMOKE TESTS
# ══════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.order(1)
def test_login(driver):
    """TC001 - Valid login"""
    do_login(driver)
    assert "inventory" in driver.current_url
    print("\n✅ TC001 PASSED: Login successful")


@pytest.mark.smoke
@pytest.mark.order(2)
def test_add_to_cart(logged_in):
    """TC002 - Add product to cart"""
    page = InventoryPage(logged_in)
    page.add_backpack_to_cart()
    assert page.get_cart_count() == "1"
    print("\n✅ TC002 PASSED: Product added to cart")


# ══════════════════════════════════════════════════
# REGRESSION TESTS
# ══════════════════════════════════════════════════

@pytest.mark.regression
@pytest.mark.order(3)
def test_view_cart(logged_in):
    """TC003 - View cart and verify item"""
    page = InventoryPage(logged_in)
    page.add_backpack_to_cart()
    page.go_to_cart()
    WebDriverWait(logged_in, 20).until(
        lambda d: "cart" in d.current_url
    )
    cart = CartPage(logged_in)
    assert cart.get_item_name() == "Sauce Labs Backpack"
    print("\n✅ TC003 PASSED: Correct item in cart")


@pytest.mark.regression
@pytest.mark.order(4)
def test_checkout(logged_in):
    """TC004 - Checkout and place order"""
    page = InventoryPage(logged_in)
    page.add_backpack_to_cart()
    page.go_to_cart()
    WebDriverWait(logged_in, 20).until(
        lambda d: "cart" in d.current_url
    )
    cart = CartPage(logged_in)
    cart.click_checkout()
    WebDriverWait(logged_in, 20).until(
        lambda d: "checkout-step-one" in d.current_url
    )
    cart.fill_form("Gopika", "Sundar", "600017")
    cart.click_continue()
    WebDriverWait(logged_in, 20).until(
        lambda d: "checkout-step-two" in d.current_url
    )
    assert cart.get_page_title() == "Checkout: Overview"
    cart.click_finish()
    WebDriverWait(logged_in, 20).until(
        lambda d: "checkout-complete" in d.current_url
    )
    assert cart.get_confirmation() == "Thank you for your order!"
    print("\n✅ TC004 PASSED: Order placed successfully")


@pytest.mark.regression
@pytest.mark.order(5)
def test_logout(logged_in):
    """TC005 - Logout"""
    page = InventoryPage(logged_in)
    page.logout()
    WebDriverWait(logged_in, 20).until(
        lambda d: d.current_url == "https://www.saucedemo.com/"
    )
    assert logged_in.current_url == "https://www.saucedemo.com/"
    print("\n✅ TC005 PASSED: Logged out")


# ══════════════════════════════════════════════════
# NEGATIVE TESTS
# ══════════════════════════════════════════════════

@pytest.mark.negative
@pytest.mark.order(6)
def test_wrong_password(driver):
    """TC006 - Wrong password shows error"""
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "wrongpass")
    assert "Epic sadface" in page.get_error_message()
    print("\n✅ TC006 PASSED: Wrong password blocked")


@pytest.mark.negative
@pytest.mark.order(7)
def test_empty_login(driver):
    """TC007 - Empty fields shows error"""
    page = LoginPage(driver)
    page.open()
    page.login("", "")
    assert "Username is required" in page.get_error_message()
    print("\n✅ TC007 PASSED: Empty fields blocked")


# ══════════════════════════════════════════════════
# DATA DRIVEN TESTS
# ══════════════════════════════════════════════════

@pytest.mark.parametrize("row", read_excel_data("LoginData"))
def test_login_data_driven(driver, row):
    """Data driven login test — reads from Excel"""
    page = LoginPage(driver)
    page.open()
    username = row["username"] or ""
    password = row["password"] or ""
    page.login(username, password)

    if row["expected_result"] == "PASS":
        WebDriverWait(driver, 20).until(
            lambda d: "inventory" in d.current_url
        )
        assert "inventory" in driver.current_url
        print(f"\n✅ PASS → {username} logged in")
        driver.get("https://www.saucedemo.com")
    else:
        error = page.get_error_message()
        assert error != ""
        print(f"\n✅ PASS → {username} correctly blocked | Error: {error}")
