import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def driver(request):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    if os.environ.get("CI"):
        # Selenium Manager auto-resolves chromedriver on CI
        drv = webdriver.Chrome(options=options)
    else:
        # Local — use your chromedriver.exe
        service = Service(r"C:\Users\gpika\Desktop\demo\chromedriver.exe")
        drv = webdriver.Chrome(service=service, options=options)

    drv.implicitly_wait(10)
    request.session._driver = drv
    yield drv
    drv.quit()


# ── Auto screenshot on every test failure ──────────
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = None
        try:
            driver = item.funcargs.get("driver")
        except Exception:
            pass
        if driver is None:
            try:
                driver = item.session._driver
            except Exception:
                pass
        if driver:
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(path)
            print(f"\n📸 Screenshot saved → {path}")
