# 1. Taban İmaj (Playwright Hazır İmajı)
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

# 2. Çalışma klasörünü ayarla
WORKDIR /app

# 3. Önce gereksinimleri kopyala ve kur (Cache avantajı için)
# requirements.txt ana dizinde olduğu için direkt kopyalıyoruz.
COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages  -r requirements.txt

# 4. TÜM projeyi kopyala
# (pom, test, playwright_test klasörlerinin hepsi /app içine kopyalanır)
COPY . .

# 5. Konteyner çalıştığında ne yapsın?
# Test dosyasının yolunu 'playwright_test/...' olarak belirtiyoruz.
CMD ["pytest", "playwright_test/test_wiki_ddt.py", "--html=rapor_docker.html"]
