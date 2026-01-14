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

