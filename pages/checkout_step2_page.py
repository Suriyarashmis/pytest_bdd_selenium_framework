from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

class CheckOutPageTwo:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.item_price = (By.CLASS_NAME, "summary_subtotal_label")
        self.tax = (By.CLASS_NAME, "summary_tax_label")
        self.total_price = (By.CLASS_NAME, "summary_total_label")
        self.cancel_button = (By.ID, "cancel")
        self.finish_button = (By.ID, "finish")

    def cost(self):
        item_price = float(self.driver.find_element(*self.item_price).text.split("$")[1])
        tax = float(self.driver.find_element(*self.tax).text.split("$")[1])
        total_price = float(self.driver.find_element(*self.total_price).text.split("$")[1])
        return item_price, tax, total_price

    def cancel_and_go_to_inventory(self):
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.cancel_button))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(expected_conditions.url_contains("inventory"))

    def finish_order(self):
        self.wait.until(expected_conditions.url_contains("checkout-step-two"))
        btn = self.wait.until(expected_conditions.element_to_be_clickable(self.finish_button))
        self.driver.execute_script("arguments[0].click();", btn)
        self.wait.until(expected_conditions.url_contains("checkout-complete"))

