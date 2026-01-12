from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from login_page import LoginPage  # Yukarıdaki dosyayı import ediyoruz

# Setup
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.saucedemo.com/")

# --- POM KULLANIMI ---

# 1. Sayfa nesnesini oluştur
login_page = LoginPage(driver)

# 2. Sayfa yeteneklerini kullan (Kod ne kadar temiz görünüyor değil mi?)
login_page.enter_username("standard_user")
login_page.enter_password("secret_sauce")
login_page.click_login()

# Assertion (Doğrulama)
assert "inventory" in driver.current_url
print("Login testi başarılı!")

driver.quit()
