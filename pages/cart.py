from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages.checkout_step1_page import CheckOutPageOne

class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.product = (By.CLASS_NAME, "inventory_item_name")
        self.checkout_button = (By.ID, "checkout")

    def get_cart_product_name(self):
        self.wait.until(expected_conditions.visibility_of_element_located(self.product))
        return self.driver.find_element(*self.product).text

    def click_checkout(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.checkout_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(expected_conditions.url_contains("checkout-step-one"))
        checkoutpage1 = CheckOutPageOne(self.driver)
        return checkoutpage1



