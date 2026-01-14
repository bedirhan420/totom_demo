import os
import pytest
import allure
import time

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = item.funcargs.get('page')
        if page:
            # Screenshot hemen eklenebilir
            allure.attach(
                page.screenshot(full_page=True), 
                name="Hata Anı (Screenshot)", 
                attachment_type=allure.attachment_type.PNG
            )

# Trace ve Video dosyasını eklemek için teardown aşamasını kullanalım
@pytest.fixture(autouse=True)
def attach_artifacts_on_failure(request):
    yield
    # Test bittikten sonra burası çalışır
    node = request.node
    if node.rep_call.failed:
        page = request.getfixturevalue("page")
        
        # 1. Önce context'i kapat ki dosyalar serbest kalsın
        page.context.close()
        
        # 2. Dosya yollarını hazırla
        # Playwright varsayılan olarak bu formatı kullanır
        safe_name = node.name.replace("[", "-").replace("]", "-").replace("/", "-")
        trace_path = os.path.join("test-results", safe_name, "trace.zip")
        
        # 3. Dosyanın yazılması için kısa bir bekleme ve kontrol döngüsü
        for _ in range(5): # 5 saniyeye kadar denemeye devam et
            if os.path.exists(trace_path) and os.path.getsize(trace_path) > 0:
                allure.attach.file(
                    trace_path, 
                    name="Hata İzleme Kaydı (Trace)", 
                    attachment_type=allure.attachment_type.ZIP
                )
                break
            time.sleep(1)