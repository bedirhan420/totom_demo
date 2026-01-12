import pytest
from wiki_page import WikiPage
from utils import excelden_veri_oku  # Az önce yazdığımız fonksiyonu çağırıyoruz

# Excel'den verileri çekiyoruz
# Bu değişken şöyle bir liste olacak: [('Atatürk', 'Atatürk'), ('Python', 'Python')...]
TEST_VERILERI = excelden_veri_oku("data.xlsx")

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
