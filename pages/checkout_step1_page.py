from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkout_step2_page import CheckOutPageTwo

class CheckOutPageOne:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.firstname = (By.ID, "first-name")
        self.lastname = (By.ID, "last-name")
        self.postalcode = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.wait.until(expected_conditions.url_contains("checkout-step-one"))
        self.error = (By.CSS_SELECTOR, ".error-message-container")
        self.cancel_button = (By.ID, "cancel")

    def fill_details(self, firstname, lastname, postalcode):
        first = self.wait.until(expected_conditions.element_to_be_clickable(self.firstname))
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, first, firstname)

        last = self.wait.until(expected_conditions.element_to_be_clickable(self.lastname))
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, last, lastname)

        postal = self.wait.until(expected_conditions.element_to_be_clickable(self.postalcode))
        self.driver.execute_script("""
            var el = arguments[0];
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(el, arguments[1]);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, postal, postalcode)

    def continue_to_page2(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.continue_button))
        self.driver.execute_script("arguments[0].click();", btn)  # ← JS click
        #print("URL after continue:", self.driver.current_url)
        self.wait.until(expected_conditions.url_contains("checkout-step-two"))
        return CheckOutPageTwo(self.driver)

    def continue_expecting_error(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.continue_button))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(expected_conditions.visibility_of_element_located(self.error))
        error_msg = self.driver.find_element(*self.error).text
        return error_msg

    def cancel_and_go_to_cart(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.cancel_button))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(expected_conditions.url_contains("cart"))







