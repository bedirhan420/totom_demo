import pytest
from playwright.sync_api import Page
from pom.login_page import LoginPage
from pom.inventory_page import InventoryPage
from pom.cart_page import CartPage
from pom.checkout_info_page import CheckoutInfoPage
from pom.checkout_overview_page import CheckoutOverviewPage
import allure

def test_valid_login(page: Page):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)

    login_p.navigate()
    login_p.login("standard_user", "secret_sauce")
    
    inventory_p.verify_on_inventory_page()

def test_locked_out_user(page: Page):
    login_p = LoginPage(page)
    login_p.navigate()
    
    login_p.login("locked_out_user", "secret_sauce")
    
    login_p.verify_error_message("Epic sadface: Sorry, this user has been locked out.")

def test_price_sorting_low_to_high(page: Page):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)

    login_p.navigate()
    login_p.login("standard_user", "secret_sauce")

    inventory_p.sort_by("lohi")

    prices = inventory_p.get_all_prices()
    
    assert prices == sorted(prices), f"Sıralama Hatası! Liste: {prices}"

def test_add_to_cart(page: Page):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)

    login_p.navigate()
    login_p.login("standard_user", "secret_sauce")

    inventory_p.add_first_item_to_cart()

    inventory_p.verify_cart_count(1)

def test_checkout(page: Page):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)
    cart_p = CartPage(page)
    checkout_info_p = CheckoutInfoPage(page)
    checkout_overview_p = CheckoutOverviewPage(page)

    login_p.navigate()
    login_p.login("standard_user", "secret_sauce")

    selected_products = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
    
    inventory_p.add_items_to_cart(selected_products)
    inventory_p.click_cart_button()
    
    cart_p.verify_items_in_cart(selected_products)
    cart_p.click_checkout()
    
    checkout_info_p.fill_info("Bedirhan", "Celik", "06000")
    
    checkout_overview_p.print_total_price()
    checkout_overview_p.click_finish()
    checkout_overview_p.verify_success_message()

@pytest.mark.parametrize("username", [
    "standard_user", 
    "problem_user", 
    "performance_glitch_user", 
    "error_user", 
    "visual_user"
])
def test_checkout_multi_user(page: Page, username):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)
    cart_p = CartPage(page)
    checkout_info_p = CheckoutInfoPage(page)
    checkout_overview_p = CheckoutOverviewPage(page)

    login_p.navigate()
    login_p.login(username, "secret_sauce")

    selected_products = ["Sauce Labs Backpack", "Sauce Labs Bike Light","Test.allTheThings() T-Shirt (Red)"]
    inventory_p.add_items_to_cart(selected_products)
    
    inventory_p.click_cart_button()
    cart_p.verify_items_in_cart(selected_products)
    
    cart_p.click_checkout()
    checkout_info_p.fill_info("Bedirhan", "Celik", "06000")
    
    checkout_overview_p.print_total_price()
    checkout_overview_p.click_finish()
    
    checkout_overview_p.verify_success_message()
    
def test_problem_user_wrong_images(page: Page):
    login_p = LoginPage(page)
    inventory_p = InventoryPage(page)

    login_p.navigate()
    login_p.login("problem_user", "secret_sauce")

    sources = inventory_p.get_all_image_sources()
    
    print(f"\nBulunan Resimler: {sources}")

    unique_images = set(sources)
    
    assert len(unique_images) == 1, "HATA! Resimlerin hepsi aynı değil, problem_user düzelmiş mi?"
    
    with allure.step("Resim Kontrolü Başarılı"):
        allure.attach("Tüm resimlerin kaynak kodları aynı, problem_user hatası doğrulandı.", name="Sonuç")