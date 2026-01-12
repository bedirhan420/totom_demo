import pytest
import os  # <--- Bunu eklemeyi unutma!
from wiki_page import WikiPage
from utils import excelden_veri_oku

# --- YOL AYARI (PATH FIX) ---
# 1. Bu dosyanın (test_wiki_ddt.py) bilgisayardaki tam adresini bul
MEVCUT_KLASOR = os.path.dirname(os.path.abspath(__file__))

# 2. Excel dosyasının tam yolunu oluştur (Klasör yolu + Dosya adı)
# Dosya adın ekran görüntüsünde 'data.xlsx' olarak görünüyor.
EXCEL_YOLU = os.path.join(MEVCUT_KLASOR, "data.xlsx")

# 3. Fonksiyona artık sadece ismini değil, TAM ADRESİNİ gönderiyoruz
TEST_VERILERI = excelden_veri_oku(EXCEL_YOLU)

# --- PARAMETRİK TEST ---
# @pytest.mark.parametrize dekoratörü testi çoğaltır.
# "aranacak, beklenen" isimleri Excel'den gelen sütunlarla eşleşir.
@pytest.mark.parametrize("aranacak, beklenen", TEST_VERILERI)
def test_wikipedia_excel_ile(page, aranacak, beklenen):
    print(f"\n🧪 Test Ediliyor: {aranacak} -> Beklenen: {beklenen}")
    
    # 1. Page Object Başlat
    wiki = WikiPage(page)
    
    # 2. Siteye Git
    wiki.siteye_git()
    
    # 3. Excel'den gelen kelimeyi arat
    wiki.arama_yap(aranacak)
    
    # 4. Excel'den gelen sonucu bekle
    wiki.basligi_dogrula(beklenen)
