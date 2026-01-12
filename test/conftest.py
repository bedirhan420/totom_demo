import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# @pytest.fixture dekoratörü bu fonksiyonun bir "Hazırlık" aracı olduğunu belirtir.
@pytest.fixture
def driver():
    # --- SETUP (Test Başlamadan Önce) ---
    print("\n--- Tarayıcı Açılıyor ---")
    service = Service(ChromeDriverManager().install())
    driver_object = webdriver.Chrome(service=service)
    driver_object.maximize_window()
    
    # 'yield' anahtar kelimesi çok önemlidir.
    # Test burada çalışır ve driver objesini test fonksiyonuna teslim eder.
    yield driver_object
    
    # --- TEARDOWN (Test Bittikten Sonra) ---
    # Test başarılı olsa da olmasa da burası çalışır.
    print("\n--- Tarayıcı Kapatılıyor ---")
    driver_object.quit()
