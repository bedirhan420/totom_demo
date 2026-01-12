from playwright.sync_api import Page, expect

class WikiPage:
    def __init__(self, page: Page):
        self.page = page
        # Dinamik başlık kontrolü için locator
        self.article_title = page.locator("#firstHeading")

    def siteye_git(self):
        # İngilizce Wikipedia'ya gidiyoruz
        self.page.goto("https://en.wikipedia.org/wiki/Main_Page")

    def arama_yap(self, kelime):
        # --- DÜZELTME: .first KULLANIMI ---
        # Sayfada birden fazla arama kutusu varsa (Strict Mode Hatası)
        # .first diyerek "ilk bulduğunu kullan" diyoruz.
        search_box = self.page.locator("input[name='search']").first
        
        search_box.fill(kelime)
        search_box.press("Enter")

    def basligi_dogrula(self, beklenen_baslik):
        expect(self.article_title).to_contain_text(beklenen_baslik)