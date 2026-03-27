from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class CheckoutComplete:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.order_complete_header = (By.CLASS_NAME, "complete-header")
        self.home_button = (By.ID, "back-to-products")


    def order_complete(self):
        header = self.wait.until(expected_conditions.visibility_of_element_located(self.order_complete_header))
        return header.text

    def go_to_home(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.home_button))  # ← wait for button
        self.driver.execute_script("arguments[0].click();", btn)  # ← JS click
        self.wait.until(expected_conditions.url_contains("inventory"))

