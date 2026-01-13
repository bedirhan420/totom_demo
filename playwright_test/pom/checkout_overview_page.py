from playwright.sync_api import Page, expect

class CheckoutOverviewPage:
    def __init__(self,page:Page):
        self.page = page
        
        self.finish_button = page.locator("[data-test='finish']")
        self.complete_header = page.locator(".complete-header")
        self.total_price_label = page.locator("[data-test='total-label']")
        
    def click_finish(self):
        self.finish_button.click()
    
    def verify_success_message(self):
        expect(self.complete_header).to_have_text("Thank you for your order!")
        
    def print_total_price(self):
        raw_text = self.total_price_label.inner_text()
        clean_price = raw_text.split(": ")[1].replace("$", "")
        
        print(f"Toplam fiyat: {clean_price} dolar")
