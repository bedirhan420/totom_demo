import openpyxl

def excelden_veri_oku(dosya_yolu):
    # Data_only=True formülleri değil, sonuçları alır
    workbook = openpyxl.load_workbook(dosya_yolu, data_only=True)
    sheet = workbook.active
    
    veriler = []
    
    # --- DÜZELTME BURADA ---
    # min_col=2: A sütununu (Sayıları) atla, B'den başla.
    # max_col=3: C sütununa kadar git.
    for satir in sheet.iter_rows(min_row=1, min_col=2, max_col=3, values_only=True):
        
        # Güvenlik Kontrolleri
        if satir[0] is None or satir[1] is None:
            continue
            
        # Başlık satırı kontrolü (Eğer başlıkları metin olarak yazdıysan filtreler)
        if "aranacak" in str(satir[0]) or "beklenen" in str(satir[1]):
            continue
            
        veriler.append(satir)
        
    return veriler