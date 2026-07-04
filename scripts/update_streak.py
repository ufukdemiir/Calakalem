#!/usr/bin/env python3
"""
yazilar/ klasöründeki YYYY-MM-DD.md dosyalarına bakarak,
bugünden (veya son yazılan günden) geriye doğru kesintisiz
gün sayısını (streak) hesaplar ve README.md'deki Günlük Seri
badge'ini günceller.
"""

import re
import sys
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

YAZILAR_DIR = Path("yazilar")
README_PATH = Path("README.md")


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


def readme_guncelle(streak: int) -> bool:
    if not README_PATH.exists():
        print("README.md bulunamadı, çıkılıyor.")
        return False

    icerik = README_PATH.read_text(encoding="utf-8")

    # Yeni badge yapısı
    etiket = urllib.parse.quote(f"{streak} gün")
    yeni_badge = f"![Günlük Seri](https://img.shields.io/badge/Günlük_Seri-{etiket}-orange)"

    # Regex: Hem eski "Streak" etiketini hem de yeni "Günlük Seri" etiketini yakalar
    desen = r"!\[(Streak|Günlük Seri)\]\(https://img\.shields\.io/badge/(Streak|Günlük_Seri)-[^)]*\)"

    if not re.search(desen, icerik):
        print("README.md içinde uygun badge bulunamadı, çıkılıyor.")
        return False

    yeni_icerik = re.sub(desen, yeni_badge, icerik)

    if yeni_icerik == icerik:
        print(f"Seri zaten güncel: {streak} gün.")
        return False

    README_PATH.write_text(yeni_icerik, encoding="utf-8")
    print(f"Seri güncellendi: {streak} gün.")
    return True


def main() -> None:
    streak = streak_hesapla()
    degisti = readme_guncelle(streak)
    
    github_output = sys.stdin.isatty() is False and __import__("os").environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if degisti else 'false'}\n")
            f.write(f"streak={streak}\n")


if __name__ == "__main__":
    main()
