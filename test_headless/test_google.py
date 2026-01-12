import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Fonksiyon isminin de 'test_' ile başlaması zorunludur.
# Parantez içine 'driver' yazarak conftest.py'deki fixture'ı çağırıyoruz.
def test_google_arama(driver):
    driver.get("https://www.google.com")
    
    # Google arama kutusunu bul
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Pytest ve Selenium")
    search_box.send_keys(Keys.RETURN)

    WebDriverWait(driver,10).until(EC.title_contains("Pytest"))
    
    # Assertion (Doğrulama)
    # Başlıkta aradığımız kelime geçiyor mu?
    assert "Pytest" in driver.title
    print("Google Testi Başarılı!")

def test_google_baslik(driver):
    driver.get("https://www.google.com")
    expected_title = "Google"
    assert driver.title == expected_title
    print("Başlık Testi Başarılı!")
