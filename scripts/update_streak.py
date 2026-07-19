#!/usr/bin/env python3
"""
yazilar/ klasöründeki YYYY-MM-DD.md dosyalarına bakarak,
bugünden (veya son yazılan günden) geriye doğru kesintisiz
gün sayısını (streak) hesaplar ve README.md ile index.md
içindeki Günlük Seri badge'lerini günceller.
"""
import os
import re
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

YAZILAR_DIR = Path("yazilar")
README_PATH = Path("README.md")
INDEX_PATH = Path("index.md")

# Badge URL'sini, onu saran markdown ![]() ya da <img src="">
# yapısından bağımsız olarak yakalar. Sadece gün etiketini
# (grup 2) değiştirir; URL'nin geri kalanı (örn. ?style=flat-square
# gibi query parametreleri) olduğu gibi korunur.
BADGE_URL_DESENI = re.compile(
    r"(https://img\.shields\.io/badge/(?:Streak|Günlük_Seri)-)([^-]*)(-orange)"
)


def gunluk_dosya_var_mi(gun: date) -> bool:
    return (YAZILAR_DIR / f"{gun.isoformat()}.md").exists()


def streak_hesapla() -> int:
    bugun = date.today()
    baslangic = bugun if gunluk_dosya_var_mi(bugun) else bugun - timedelta(days=1)
    streak = 0
    gun = baslangic
    while gunluk_dosya_var_mi(gun):
        streak += 1
        gun -= timedelta(days=1)
    return streak


def icerikte_guncelle(icerik: str, streak: int) -> tuple[str, bool]:
    etiket = urllib.parse.quote(f"{streak} gün")

    def degistir(eslesme: re.Match) -> str:
        return f"{eslesme.group(1)}{etiket}{eslesme.group(3)}"

    if not BADGE_URL_DESENI.search(icerik):
        return icerik, False

    yeni_icerik = BADGE_URL_DESENI.sub(degistir, icerik)
    return yeni_icerik, yeni_icerik != icerik


def dosya_guncelle(yol: Path, streak: int) -> bool:
    if not yol.exists():
        print(f"{yol}: dosya bulunamadı, atlanıyor.")
        return False

    icerik = yol.read_text(encoding="utf-8")
    yeni_icerik, degisti_mi = icerikte_guncelle(icerik, streak)

    if not degisti_mi:
        print(f"{yol}: badge bulunamadı ya da seri zaten güncel ({streak} gün).")
        return False

    yol.write_text(yeni_icerik, encoding="utf-8")
    print(f"{yol}: seri güncellendi -> {streak} gün.")
    return True


def main() -> None:
    streak = streak_hesapla()

    readme_degisti = dosya_guncelle(README_PATH, streak)
    index_degisti = dosya_guncelle(INDEX_PATH, streak)
    degisti = readme_degisti or index_degisti

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if degisti else 'false'}\n")
            f.write(f"streak={streak}\n")


if __name__ == "__main__":
    main()
