from pytest_bdd import scenarios, scenario, given, when, then, parsers
from pages.login import LoginPage

BASE_URL = "https://www.saucedemo.com/"

# ── Scenarios ────────────────────────────────────────────────────────────────
scenarios('../features/login.feature')

# ── Given ────────────────────────────────────────────────────────────────────

@given("I am on the login page")
def on_login_page(browserInstance, context):
    browserInstance.get(BASE_URL)
    context['driver'] = browserInstance
    context['login'] = LoginPage(browserInstance)

# ── When ─────────────────────────────────────────────────────────────────────

@when(parsers.parse('I enter username "{username}" and click login'))
def enter_username_only(context, username):
    context['login'].enter_username(username)
    context['login'].click_login()

@when(parsers.parse('I enter password "{password}" and click login'))
def enter_password_only(context, password):
    context['login'].enter_password(password)
    context['login'].click_login()

@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login_with_credentials(context, username, password):
    context['login'].login(username=username, password=password)

# ── Then ──────────────────────────────────────────────────────────────────────

@then(parsers.parse('I should see error "{expected_error}"'))
def verify_error_message(context, expected_error):
    error = context['login'].get_error_message()
    assert expected_error in error, f"Expected '{expected_error}' in '{error}'"

@then("I should be on the inventory page")
def verify_on_inventory(context):
    assert "inventory" in context['driver'].current_url