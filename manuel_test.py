from playwright.sync_api import sync_playwright
import time

def run():
    # Playwright'ı başlatıyoruz (Selenium'daki 'driver' mantığı)
    with sync_playwright() as p:
        # Tarayıcıyı aç (Headless=False yaparak ekranda görüyoruz)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🚀 Wikipedia'ya gidiliyor...")
        page.goto("https://www.wikipedia.org")

        # --- LOCATOR MANTIĞI (Selenium'dan Çok Daha Akıllı) ---
        # Selenium'da: driver.find_element(By.NAME, "search")
        # Playwright'ta: page.fill(selector, value)
        
        # Arama kutusunu bul ve yaz
        print("✍️ 'Mustafa Kemal Atatürk' yazılıyor...")
        page.fill("input[name='search']", "Mustafa Kemal Atatürk")

        # Enter tuşuna bas
        print("asd Enter'a basılıyor...")
        page.press("input[name='search']", "Enter")

        # Sayfanın yüklenmesini bekle (Akıllı Bekleme)
        # Selenium'daki WebDriverWait'in otomatik halidir.
        # Sayfada "Atatürk" başlığı çıkana kadar bekler.
        page.wait_for_selector("#firstHeading")

        print("👀 Bilgiler çekiliyor...")
        
        # Doğum tarihini çekmek için CSS Selector kullanıyoruz
        # Wikipedia'daki bilgi kutusunun (infobox) içindeki doğum tarihi sınıfı
        # Bu kısım sayfaya göre değişebilir, genel bir yol izliyoruz.
        try:
            # Bday (Birthday) sınıfını içeren elementi bul
            dogum_tarihi = page.locator(".bday").first.inner_text()
            print(f"\n✅ SONUÇ: Atatürk'ün Doğum Tarihi: {dogum_tarihi}")
        except:
            print("\n⚠️ Tam tarih formatı bulunamadı, alternatif metin aranıyor...")
            # Alternatif olarak tüm bilgi kutusunu alabiliriz
            infobox = page.locator(".infobox").text_content()
            if "1881" in infobox:
                print("✅ SONUÇ: Metin içinde '1881' yılı doğrulandı.")

        # Biraz bekle ki sonucu görebilesin
        time.sleep(5)
        
        # Kapat
        browser.close()
        print("🏁 Test Tamamlandı.")

if __name__ == "__main__":
    run()
