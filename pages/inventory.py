from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from pages.cart import CartPage

class InventoryPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        self.all_products = (By.CSS_SELECTOR, "div[class=inventory_item]")
        self.cart_button = (By.CSS_SELECTOR, "a.shopping_cart_link")

    def add_to_cart(self, product_name):
        self.wait.until(expected_conditions.visibility_of_all_elements_located(self.all_products))
        itemList = self.driver.find_elements(*self.all_products)
        for item in itemList:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                btn = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
                self.wait.until(expected_conditions.element_to_be_clickable(btn))
                self.driver.execute_script("arguments[0].click();", btn)
                btn = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
                # verify item was actually added by checking button text changed
                self.wait.until(lambda d: btn.text == "Remove")
                break

    def remove_from_cart(self, product_name):
        self.wait.until(expected_conditions.visibility_of_all_elements_located(self.all_products))
        itemList = self.driver.find_elements(*self.all_products)
        for item in itemList:
            name = item.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
            if name == product_name:
                btn = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
                self.wait.until(expected_conditions.element_to_be_clickable(btn))
                self.driver.execute_script("arguments[0].click();", btn)
                btn = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
                # verify item was actually added by checking button text changed
                self.wait.until(lambda d: btn.text == "Add to cart")
                break

    def go_to_cart(self):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
        cart = self.wait.until(expected_conditions.element_to_be_clickable(self.cart_button))
        self.driver.execute_script("arguments[0].click();", cart)
        self.wait.until(expected_conditions.url_contains("cart.html"))
        return CartPage(self.driver)




