from playwright.sync_api import Page, expect

class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_button = page.locator("[data-test='checkout']")
        self.cart_items = page.locator(".cart_item")

    def click_checkout(self):
        self.checkout_button.click()
        
    def verify_items_in_cart(self, expected_products):
        actual_products = self.page.locator(".inventory_item_name").all_inner_texts()
        
        for product in expected_products:
            assert product in actual_products, f"{product} sepette bulunamadı!"