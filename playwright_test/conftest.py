import pytest
import allure
from playwright.sync_api import Page

# Test başarısız olursa Allure raporuna ekran görüntüsü ekle
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Sadece test çalışırken (setup/teardown değil) ve hata aldıysa
    if report.when == "call" and report.failed:
        # Test fonksiyonundaki 'page' fixture'ını yakala
        page = item.funcargs.get('page')
        if page:
            # Ekran görüntüsünü al
            screenshot = page.screenshot(full_page=True)
            
            # Allure raporuna "Hata Anı" adıyla ekle
            allure.attach(
                screenshot, 
                name="Hata Anı (Screenshot)", 
                attachment_type=allure.attachment_type.PNG
            )