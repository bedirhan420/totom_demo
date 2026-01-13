from playwright.sync_api import Page, expect

class CheckoutInfoPage:
    def __init__(self,page:Page):
        self.page = page
        
        self.firstname_textbox = page.locator("[data-test='firstName']")
        self.lastname_textbox = page.locator("[data-test='lastName']")
        self.postlacode_textbox = page.locator("[data-test='postalCode']")
        
        self.continue_button = page.locator("[data-test='continue']")
        
    def fill_info(self,first_name, last_name, zip_code):
        self.firstname_textbox.fill(first_name)
        self.lastname_textbox.fill(last_name)
        self.postlacode_textbox.fill(zip_code)
        self.continue_button.click()