import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest_html

# @pytest.fixture dekoratörü bu fonksiyonun bir "Hazırlık" aracı olduğunu belirtir.
@pytest.fixture
def driver():
    # --- SETUP (Test Başlamadan Önce) ---
    print("\n--- Tarayıcı Headless Modda Hazırlanıyor ---")
   
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu") 
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
       
    service = Service(ChromeDriverManager().install())
    driver_object = webdriver.Chrome(service=service,options=chrome_options)
    
    # 'yield' anahtar kelimesi çok önemlidir.
    # Test burada çalışır ve driver objesini test fonksiyonuna teslim eder.
    yield driver_object
    
    # --- TEARDOWN (Test Bittikten Sonra) ---
    # Test başarılı olsa da olmasa da burası çalışır.
    print("\n--- Tarayıcı Kapatılıyor ---")
    driver_object.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    # Eğer test "call" aşamasındaysa (yani çalıştırılıyorsa) ve başarısız olduysa:
    if report.when == "call" and report.failed:
        # Test fonksiyonundan 'driver' fixture'ını çek
        driver = item.funcargs.get('driver')
        
        if driver:
            # Ekran görüntüsünü Base64 formatında (metin olarak) al
            # Bu sayede resmi HTML dosyasının içine gömebiliriz, ekstra dosya oluşmaz.
            screenshot = driver.get_screenshot_as_base64()
            
            # Resmi rapora ekle
            # 'image' fonksiyonu base64 verisini alır ve HTML img etiketine çevirir.
            extras.append(pytest_html.extras.image(screenshot, ""))
            
    report.extras = extras
