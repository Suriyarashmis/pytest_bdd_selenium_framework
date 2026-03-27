from pytest_bdd import scenario,scenarios, given, when, then, parsers
from pages.checkoutcomplete import CheckoutComplete
from pages.login import LoginPage

BASE_URL = "https://www.saucedemo.com/"

# ── Scenarios ────────────────────────────────────────────────────────────────
scenarios('../features/checkout.feature')

# ── Given ─────────────────────────────────────────────────────────────────────

@given(parsers.parse('I am logged in as "{username}" with password "{password}"'))
def logged_in(browserInstance, context, username, password):
    browserInstance.get(BASE_URL)
    context['driver'] = browserInstance
    login = LoginPage(browserInstance)
    context['inventory'] = login.login(username=username, password=password)

@given(parsers.parse('I add "{product}" to the cart'))
def add_product_given(context, product):
    context['inventory'].add_to_cart(product_name=product)

@given("I navigate to the cart")
def navigate_to_cart(context):
    context['cart'] = context['inventory'].go_to_cart()

@given("I click checkout")
def click_checkout_given(context):
    context['checkout1'] = context['cart'].click_checkout()

# ── When ─────────────────────────────────────────────────────────────────────

@when(parsers.parse('I fill details with firstname "{firstname}" lastname "{lastname}" postal "{postal}"'))
def fill_details(context, firstname, lastname, postal):
    context['checkout1'].fill_details(
        firstname="" if firstname == "EMPTY" else firstname,
        lastname="" if lastname == "EMPTY" else lastname,
        postalcode="" if postal == "EMPTY" else postal
    )

@when("I click continue expecting error")
def click_continue_expecting_error(context):
    context['error_msg'] = context['checkout1'].continue_expecting_error()

@when("I cancel from checkout step one")
def cancel_step_one(context):
    context['checkout1'].cancel_and_go_to_cart()

@when("I continue to checkout step two")
def continue_to_step_two(context):
    context['checkout2'] = context['checkout1'].continue_to_page2()

@when("I cancel from checkout step two")
def cancel_step_two(context):
    context['checkout2'].cancel_and_go_to_inventory()

@when("I finish the order")
def finish_order(context):
    context['checkout2'].finish_order()
    context['complete'] = CheckoutComplete(context['driver'])

# ── Then ──────────────────────────────────────────────────────────────────────

@then(parsers.parse('I should see checkout error "{expected_error}"'))
def verify_checkout_error(context, expected_error):
    error = context['error_msg']
    assert expected_error in error, f"Expected '{expected_error}' in '{error}'"

@then(parsers.parse('the URL should contain "{fragment}"'))
def verify_url_contains(context, fragment):
    assert fragment in context['driver'].current_url

@then("the total should equal item price plus tax")
def verify_totals(context):
    item_price, tax, total_price = context['checkout2'].cost()
    assert total_price == round(item_price + tax, 2), (
        f"Total mismatch: {total_price} != {round(item_price + tax, 2)}"
    )

@then(parsers.parse('I should see "{message}"'))
def verify_confirmation_message(context, message):
    assert message in context['complete'].order_complete()