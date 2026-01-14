import pytest
import allure
import time # Dosyanın en üstüne ekle

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = item.funcargs.get('page')
        if page:
            allure.attach(
                page.screenshot(full_page=True), 
                name="Hata Anı (Screenshot)", 
                attachment_type=allure.attachment_type.PNG
            )

            page.context.close() 
            video_path = page.video.path() if page.video else None
            
            if video_path:
                time.sleep(0.5) 
                allure.attach.file(
                    video_path, 
                    name="Hata Anı (Video)", 
                    attachment_type=allure.attachment_type.WEBM
                )

            # TRACE DOSYASINI RAPORA EKLEME:
            # test-results içindeki ilgili trace dosyasını bulup iliştirir

            trace_path = f"test-results/{item.name.replace('[', '-').replace(']', '-')}/trace.zip"
            # Not: Dosya yolunun doğruluğundan emin olmak için test-results yapınızı kontrol edin
            try:
                allure.attach.file(
                    trace_path, 
                    name="Hata İzleme Kaydı (Trace)", 
                    attachment_type=allure.attachment_type.ZIP
                )
            except:
                pass # Dosya henüz oluşmadıysa hata vermemesi için
