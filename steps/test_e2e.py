from pytest_bdd import scenario, given, when, then, parsers
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkoutcomplete import CheckoutComplete
from pages.login import LoginPage

BASE_URL = "https://www.saucedemo.com/"

# ── Scenario ─────────────────────────────────────────────────────────────────

@scenario('../features/e2e.feature', 'Full purchase journey with add remove and checkout')
def test_e2e():
    pass

# ── Given ────────────────────────────────────────────────────────────────────

@given("I am on the login page")
def on_login_page(browserInstance, context):
    browserInstance.get(BASE_URL)
    context['driver'] = browserInstance
    context['wait'] = WebDriverWait(browserInstance, 20)
    context['login'] = LoginPage(browserInstance)

# ── When ─────────────────────────────────────────────────────────────────────

@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def login(context, username, password):
    context['inventory'] = context['login'].login(username=username, password=password)
    context['wait'].until(expected_conditions.url_contains("inventory"))

@when(parsers.parse('I add "{product}" to the cart'))
def add_to_cart(context, product):
    context['inventory'].add_to_cart(product_name=product)

@when(parsers.parse('I remove "{product}" from the cart'))
def remove_from_cart(context, product):
    context['inventory'].remove_from_cart(product_name=product)

@when("I go to the cart page")
def go_to_cart(context):
    context['cart'] = context['inventory'].go_to_cart()

@when("I click checkout")
def click_checkout(context):
    context['checkout1'] = context['cart'].click_checkout()

@when(parsers.parse('I fill details with firstname "{firstname}" lastname "{lastname}" postal "{postal}"'))
def fill_details(context, firstname, lastname, postal):
    context['checkout1'].fill_details(
        firstname=firstname,
        lastname=lastname,
        postalcode=postal
    )

@when("I continue to checkout step two")
def continue_to_step_two(context):
    context['checkout2'] = context['checkout1'].continue_to_page2()

@when("I finish the order")
def finish_order(context):
    context['checkout2'].finish_order()
    context['wait'].until(expected_conditions.url_contains("checkout-complete"))
    context['complete'] = CheckoutComplete(context['driver'])

@when("I go back to home")
def go_back_to_home(context):
    context['complete'].go_to_home()
    context['wait'].until(expected_conditions.url_contains("inventory"))

# ── Then ──────────────────────────────────────────────────────────────────────

@then("I should be on the inventory page")
def verify_inventory(context):
    assert "inventory" in context['driver'].current_url

@then(parsers.parse('the cart should contain "{product}"'))
def verify_cart_product(context, product):
    assert context['cart'].get_cart_product_name() == product

@then(parsers.parse('the URL should contain "{fragment}"'))
def verify_url(context, fragment):
    assert fragment in context['driver'].current_url

@then(parsers.parse('I should see "{message}"'))
def verify_message(context, message):
    assert message in context['complete'].order_complete()