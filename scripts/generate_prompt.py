import sys
from datetime import date
from pathlib import Path

def main():
    # Terminalden gelen yapay zeka çıktısını okuyoruz
    if len(sys.argv) > 1:
        konu = sys.argv[1].strip()
    else:
        konu = "Dijital dünyada kelimelerin gücü ve geleceği."

    bugun = date.today().isoformat()
    
    # Yeni ana klasörümüz
    fikir_dir = Path("yazi-fikri")
    fikir_dir.mkdir(exist_ok=True)
    
    dosya_yolu = fikir_dir / f"{bugun}.md"
    
    # Eğer o günün dosyası zaten varsa üzerine yazmasın
    if dosya_yolu.exists():
        print(f"{bugun}.md zaten mevcut, işlem atlandı.")
        return
        
    sablon = f"""# {bugun} - Günün Yazı Fikri

> 💡 **10 Dakikalık Hızlı Yazı Önerisi:**
> {konu}

---
# ✍️ 10 Dakikalık Geri Sayımı Başlat ve Karala...

"""
    dosya_yolu.write_text(sablon, encoding="utf-8")
    print(f"Yeni fikir dosyası oluşturuldu: {dosya_yolu}")

if __name__ == "__main__":
    main()
