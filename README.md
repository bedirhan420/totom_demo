# Totom Monorepo: Web & Test Otomasyon Projesi

Bu proje; web sitesi kaynak kodları ile Playwright tabanlı test otomasyonunun aynı repoda yönetildiği, CI/CD süreçleri tamamen Docker üzerinde koşan profesyonel bir **Monorepo** mimarisidir.



---

## Klasör Yapısı ve Görev Dağılımı

```text
├── .github/workflows/ # GitHub Actions CI/CD (YAML) dosyaları.
├── src/               # Uygulama kaynak kodları (Web sitesi).
├── tests/             # Test Otomasyon Klasörü.
│   ├── data/          # Test verileri (JSON).
│   ├── pages/         # Page Object Model (POM) sınıfları.
│   ├── playwright_tests/ # Gerçek senaryolar (test_*.py).
│   └── conftest.py    # Raporlama ve Ekran Görüntüsü ayarları.
├── Dockerfile         # Testlerin koşturulacağı izole Linux ortamı.
├── pytest.ini         # Pytest konfigürasyonu.
└── requirements.txt   # Bağımlılıklar.
```

---

## Teknik Bileşenlerin Detaylı Analizi

### 1. Dockerfile: İzole Test Laboratuvarı
Dockerfile, testlerin "benim bilgisayarımda çalışıyordu" sorununu bitiren reçetedir.



* **Base Image:** `v1.57.0-noble` kullanılarak tarayıcıların çalışması için gereken tüm Linux bağımlılıkları (`libgbm`, `libnss3` vb.) paketlenmiş olarak gelir.
* **ENV PYTHONUNBUFFERED=1:** Python loglarının anlık olarak GitHub Actions konsoluna düşmesini sağlar.
* **Katman Yönetimi:** Önce `requirements.txt` kopyalanarak kütüphane kurulumları cache'e alınır. Kod değişikliklerinde kütüphaneler tekrar indirilmez, test hızı artar.
#### Ana Çalıştırma Komutu:
`CMD ["pytest", "tests/playwright_tests/", "-n", "auto", "--alluredir=allure-results"]`

Bu komut, konteyner ayağa kalktığı anda tüm test mekanizmasını başlatan anahtardır:
* **`pytest`**: Ana test koşturucuyu tetikler.
* **`tests/playwright_tests/`**: Pytest'e sadece bu klasördeki senaryoları taramasını söyleyerek açılış hızını artırır.
* **`-n auto`**: **Parallel Execution (xdist)** özelliğini aktif eder. Konteynerın CPU çekirdek sayısına göre testleri bölerek aynı anda koşturur 
* **`--alluredir=allure-results`**: Test sonuçlarını, ekran görüntülerini ve videoları raporlanmak üzere bu klasörde toplar.

### 2. conftest.py: Raporlama ve Görsel Kanıt
`conftest.py`, Pytest'in beynidir. Yerel sunucu ayarlarından bağımsız olarak, testler hata aldığında **otomatik ekran görüntüsü** alarak raporlara ekler.

* **Screenshot Logic:** Test başarısız olduğunda (failed), Playwright otomatik olarak tarayıcının o anki halini çeker ve Allure raporuna gömer.
* **Fixture Yönetimi:** Tarayıcıyı başlatma, temizleme (cleanup) ve raporlama hook'ları burada yönetilir.



### 3. GitHub Actions (.yml): Otomasyon Orkestrası
GitHub sunucularında kod her değiştiğinde çalışan bu dosya, şu adımları izler:

* **Tetikleyici (Trigger):** `push` ve `pull_request` anında devreye girer.
* **Konteyner Koşumu:** `container: image: ...` satırı ile GitHub Actions'a işi doğrudan bizim Docker imajımız içinde yapması komutu verilir.
* **Artifacts & Pages:** Test sonunda oluşan `allure-results` verilerini toplar, Allure raporuna dönüştürür ve GitHub Pages üzerinde bir web sitesi olarak yayınlar.

### 4. requirements.txt: Bağımlılık ve Versiyon Yönetimi
Bu dosya, projenin çalışması için gerekli olan tüm Python kütüphanelerinin ve bunların spesifik sürümlerinin listesidir. Docker imajı oluşturulurken bu liste üzerinden kurulum yapılır.



#### Temel Kütüphaneler ve Görevleri:
* **`pytest`**: Testlerimizi koşturan ana framework.
* **`pytest-playwright`**: Playwright'ın Pytest ile entegre çalışmasını ve tarayıcı yönetimini sağlar.
* **`pytest-xdist`**: Dockerfile içindeki `-n auto` komutunun çalışmasını, yani testlerin işlemci çekirdeklerine bölünerek **paralel** koşturulmasını sağlayan kritik eklentidir.
* **`allure-pytest`**: Test sonuçlarını Allure raporlama formatına uygun şekilde (JSON/XML) kaydeden köprüdür.
---

### 5. pytest.ini: Test Konfigürasyon Merkezi
`pytest.ini`, test sürecinin standartlarını belirleyen ve komut satırı karmaşasını önleyen ana yapılandırma dosyasıdır. Pytest çalıştırıldığında ilk olarak bu dosyaya bakar.



#### Yapılandırma Detayları:
* **`testpaths`**: Pytest'e sadece `tests/playwright_tests/` klasörüne odaklanmasını söyler. Bu, projenin geri kalanındaki (src, venv vb.) dosyaların taranmasını engelleyerek hız kazandırır.
* **`addopts` (Additional Options)**: Her çalıştırmada otomatik olarak eklenen parametrelerdir. 
    * Örneğin `-n auto` ve `--alluredir` burada tanımlandığında, Dockerfileda sadece `pytest` yazmanız yeterli olur; geri kalan her şeyi bu dosya halleder.
* **`python_files`**: Hangi dosyaların test olarak kabul edileceğini belirler. Standart olarak `test_*.py` kalıbı kullanılır.
* **`markers`**: Testlerinizi gruplandırmanıza (Örn: `@pytest.mark.smoke`) ve sadece belirli grupları çalıştırmanıza olanak tanır.



> **Best Practice:** Ekip çalışmasında, tüm çalışma parametrelerini `pytest.ini` içinde sabitlemek, tüm geliştiricilerin ve CI/CD sisteminin testleri **aynı standartlarla** koşturmasını garanti eder.

## Kritik Kurallar ve Standartlar

1.  **Test Keşfi (Discovery):** Dosya isimleri mutlaka `test_` ile başlamalıdır. İçindeki fonksiyonlar da `def test_...` yapısında olmalıdır. Aksi halde Pytest bu testleri görmez.
2.  **POM (Page Object Model):** UI elementlerine ait selector'lar asla test dosyasında durmaz. `pages/` altındaki sınıflarda tanımlanır.
3.  **Hata Analizi:** Testler bittiğinde GitHub Actions loglarından Allure linkine giderek, hata anında alınan ekran görüntülerini inceleyin.

---

## Yeni Test Ekleme İş Akışı

1.  **Codegen:** Yerel bilgisayarınızda (Python ve Playwright yüklü olmalı) selector'ları yakalayın:
    ```bash
    playwright codegen <hedef_site_adresi>
    ```
2.  **Sayfa Tanımı:** Yakalanan selector'ları `tests/pages/` altına yeni bir sayfa sınıfı olarak ekleyin.
3.  **Veri Girişi:** Varsa test verilerini `tests/data/` altındaki ilgili JSON dosyasına yazın.
4.  **Senaryo:** `tests/playwright_tests/` altında testinizi yazın ve POM metodunu çağırın.
5.  **Push:** Kodunuzu gönderin ve GitHub Actions'ın testi sizin yerinize Docker içinde koşturmasını izleyin!

## Gelişmiş Raporlama ve Hata Ayıklama (Debugging)

Projemiz, test sonuçlarını sadece "geçti/kaldı" şeklinde değil, hataların nedenini saniyeler içinde bulmanızı sağlayacak görsel kanıtlarla birlikte sunar.

### 1. Allure Report (Test Sonuç Paneli)
GitHub Actions üzerinde koşan her testten sonra otomatik olarak bir **Allure Report** oluşturulur ve GitHub Pages üzerinden yayınlanır.

![Allure Test Paneli](https://github.com/bedirhan420/totom_demo/blob/main/allure.png) 

* **Görsel Kanıt (Screenshot):** Bir test başarısız olduğunda, sistem otomatik olarak "Hata Anı (Screenshot)" kaydı alır (conftest.py). Bu sayede hatanın koddan mı yoksa arayüzdeki bir değişiklikten mi kaynaklandığını anında görebilirsiniz.
* **Kategorizasyon:** Testler; ürün defektleri, test hataları ve sistem hataları olarak otomatik gruplandırılır.
* **Parametrik İzleme:** Hangi kullanıcının (`standard_user`, `problem_user` vb.) hangi tarayıcıda hata aldığını parametreler kısmından detaylıca inceleyebilirsiniz.

### 2. Playwright Trace Viewer (Adım Adım İzleme)
"Hata anında ekranda ne vardı?" sorusundan daha fazlasına ihtiyacınız olduğunda **Playwright Trace** devreye girer. Bu araç, testin her bir milisaniyesini kaydeden bir "kara kutu" gibidir.

![Playwright Trace Paneli](https://github.com/bedirhan420/totom_demo/blob/main/trace.png) 

* **Timeline (Zaman Çizelgesi):** Testin başından sonuna kadar ekranın nasıl değiştiğini film şeridi gibi izleyebilirsiniz.
* **Action Log:** Playwright'ın hangi elemente tıkladığını, hangi metni yazdığını ve o an DOM (HTML) yapısının ne durumda olduğunu görebilirsiniz.
* **Source Code Entegrasyonu:** Hata alınan satırın, sayfa objesi (`inventory_page.py`) içindeki hangi koda denk geldiğini doğrudan Trace Viewer üzerinden analiz edebilirsiniz.

#### Trace Nasıl İncelenir?
1.  GitHub Actions'tan veya yerel testten sonra oluşan `trace.zip` dosyasını indirin.
2.  [trace.playwright.dev](https://trace.playwright.dev) adresine gidin.
3.  İndirdiğiniz dosyayı sürükleyip bırakın. Tüm test sürecini interaktif bir şekilde yeniden yaşayın!

---
