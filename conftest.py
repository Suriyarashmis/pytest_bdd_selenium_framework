import pytest
from selenium import webdriver
import os

BROWSERSTACK_USERNAME = os.getenv("BS_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BS_ACCESS_KEY")
driver = None
BS_HUB = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub.browserstack.com/wd/hub"
GRID_URL = "http://localhost:4444"

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="browser selection")
    parser.addoption("--env", action="store", default="local", help="local | grid | browserstack")
    parser.addoption("--headless", action="store_true", default=False, help="run headless")

@pytest.fixture(scope="function")
def browserInstance(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    env = request.config.getoption("env")

    if env == "local":
        headless = request.config.getoption("--headless")
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)

    elif env == "grid":
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(command_executor=GRID_URL, options=options)

    elif env == "browserstack":
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            options.set_capability("browserName", "Chrome")
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            options.set_capability("browserName", "Firefox")

        options.set_capability("browserVersion", "latest")
        options.set_capability("bstack:options", {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "Pytest BDD Test"
        })
        driver = webdriver.Remote(command_executor=BS_HUB, options=options)

    driver.maximize_window()
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.fixture()
def context():
    """Shared state dictionary passed between BDD steps."""
    return {}

@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join( os.path.dirname( __file__ ), 'reports' )
            file_name = os.path.join( reports_dir, report.nodeid.replace( "::", "_" ) + ".png" )
            print( "file name is " + file_name )
            if driver:
                _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra


def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)
