from playwright.sync_api import Page, expect

class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.header_title = page.locator(".title")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.inventory_items = page.locator(".inventory_item")
        self.item_prices = page.locator(".inventory_item_price")
        self.add_to_cart_buttons = page.locator("button:has-text('Add to cart')")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_button = page.locator("[data-test='shopping-cart-link']")
        self.product_images = page.locator(".inventory_item_img img")

    def verify_on_inventory_page(self):
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")
        expect(self.header_title).to_have_text("Products")

    def sort_by(self, option_value):
        self.sort_dropdown.select_option(option_value)

    def get_all_prices(self):
        price_texts = self.item_prices.all_inner_texts()
        return [float(price.replace("$", "")) for price in price_texts]

    def add_first_item_to_cart(self):
        self.add_to_cart_buttons.first.click()

    def verify_cart_count(self, count):
        expect(self.cart_badge).to_have_text(str(count))
    
    def click_cart_button(self):
        self.cart_button.click()
    
    def get_all_image_sources(self):
        return self.product_images.evaluate_all("imgs => imgs.map(img => img.getAttribute('src'))")