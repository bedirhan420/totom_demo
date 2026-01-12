import pytest
from wiki_page import WikiPage

def test_wikipedia_arama_basarili(page):
    # 1. Page Object'i başlat
    wiki = WikiPage(page)
    
    # 2. Adımları Uygula
    wiki.siteye_git()
    wiki.arama_yap("Mustafa Kemal Atatürk")
    
    # 3. Doğrulama (POM içinde yaptığımız için burası temiz kaldı)
    wiki.basligi_dogrula("Atatürk")

def test_wikipedia_arama_hatali(page):
    wiki = WikiPage(page)
    wiki.siteye_git()
    
    print("\n--- Hatalı Senaryo Başlıyor: Python aratıp Java bekleyeceğiz ---")
    wiki.arama_yap("Python (programming language)")
    
    # HATA BURADA OLACAK:
    # Sayfa başlığında "Python" yazıyor ama biz inatla "Java" yazmasını bekliyoruz.
    # Playwright bir süre bekleyecek, "Java"yı göremeyince hata fırlatacak.
    wiki.basligi_dogrula("Java Programming")
