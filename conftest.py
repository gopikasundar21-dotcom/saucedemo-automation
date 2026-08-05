import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="session")
def driver(request):
    service = Service(r"C:\Users\gpika\Desktop\demo\chromedriver.exe")
    drv = webdriver.Chrome(service=service)
    drv.implicitly_wait(5)
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
        # Try getting driver from fixtures
        try:
            driver = item.funcargs.get("driver")
        except Exception:
            pass
        # Try getting from session if not found directly
        if driver is None:
            try:
                driver = item.session._driver
            except Exception:
                pass
        if driver:
            screenshot_dir = r"C:\Users\gpika\Desktop\demo\screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(path)
            print(f"\n📸 Screenshot saved → {path}")

