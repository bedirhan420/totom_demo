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
            # 1. Screenshot Al
            allure.attach(
                page.screenshot(full_page=True), 
                name="Hata Anı (Screenshot)", 
                attachment_type=allure.attachment_type.PNG
            )

            # 2. ÖNEMLİ: İzlemeyi (Trace) durdur ve diske yazılmasını sağla
            # Eğer trace on/retain-on-failure kullanıyorsanız context'i kapatmak yazmayı tetikler
            page.context.close() 
            
            # 3. Video Ekle
            video_path = page.video.path() if page.video else None
            if video_path:
                time.sleep(1) # Dosyanın tam yazılması için biraz daha süre verin
                allure.attach.file(
                    video_path, 
                    name="Hata Anı (Video)", 
                    attachment_type=allure.attachment_type.WEBM
                )

            # 4. TRACE EKLEME (Geliştirilmiş Mantık)
            # Klasör ismindeki özel karakterleri temizleyen daha güvenli bir yol:
            safe_name = item.name.replace("[", "-").replace("]", "-").replace("/", "-")
            trace_path = os.path.join("test-results", safe_name, "trace.zip")
            
            # Dosyanın varlığını ve yazılma işleminin bittiğini kontrol et
            if os.path.exists(trace_path):
                time.sleep(1) # Trace dosyasının finalize edilmesi için bekleme
                try:
                    allure.attach.file(
                        trace_path, 
                        name="Hata İzleme Kaydı (Trace)", 
                        attachment_type=allure.attachment_type.ZIP
                    )
                except Exception as e:
                    print(f"Trace attach hatası: {e}")