from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1. Tarayıcı Ayarları (Driver Kurulumu)
# Bu satır, Chrome sürümünüze uygun driver'ı otomatik indirir ve kurar.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 2. Siteye Git
url = "https://www.google.com"
driver.get(url)
print(f"{url} adresine gidildi.")

# 3. Elementi Bul (Arama Kutusu)
# Google'ın arama kutusunun 'name' özelliği 'q' dur.
search_box = driver.find_element(By.NAME, "q")

# 4. Aksiyon Al (Yazı Yaz ve Enter'a Bas)
search_box.send_keys("Python Selenium Dersleri")
search_box.send_keys(Keys.RETURN) # Enter tuşuna basar

print("Arama yapıldı.")

# 5. Bekle ve Kapat
# Not: Gerçek testlerde time.sleep yerine 'Explicit Wait' kullanılır.
# Şimdilik sonucu görebilmek için koyuyoruz.
time.sleep(5)

driver.quit()
print("Tarayıcı kapatıldı.")