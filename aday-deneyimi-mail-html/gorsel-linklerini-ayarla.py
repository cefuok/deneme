#!/usr/bin/env python3
"""Sablonlardaki gorsel yollarini toplu degistirir.

HTML mailde gorseller mutlak URL olmak zorunda; goreli 'assets/...' yolu
sadece tarayici onizlemesinde calisir. Her sablon ayni gorsele birden cok
yerden atif yapar (stylesheet url(), background attribute, Outlook'un VML
v:fill src'i, img src) ve bunlarin hepsi birlikte degismeli.

Gonderime hazirlamak icin:

    python3 gorsel-linklerini-ayarla.py

Taraticida onizlemek icin geri almak icin:

    python3 gorsel-linklerini-ayarla.py assets/

Baska bir sunucu icin:

    python3 gorsel-linklerini-ayarla.py https://ornek.com/yol/
"""
import pathlib
import re
import sys

CANLI = "https://turktelekomkariyer.com.tr/assets/mailing/20260929/"

ASSETS = (
    "tt-arkaplan-desen.png",
    "mail-1-link.png",
    "mail-1-logo.png",
    "mail-2-logo.png",
    "mail-2-surec.png",
    "ikon-1.png", "ikon-2.png", "ikon-3.png",
    "ikon-4.png", "ikon-5.png", "ikon-6.png",
    "sosyalmedya-1.png", "sosyalmedya-2.png", "sosyalmedya-3.png",
)


def main() -> int:
    if len(sys.argv) > 2:
        print(__doc__)
        return 2
    base = sys.argv[1] if len(sys.argv) == 2 else CANLI
    if not base.endswith("/"):
        base += "/"

    here = pathlib.Path(__file__).parent
    toplam = 0
    for path in sorted(here.glob("*-tasarim.html")):
        text = path.read_text(encoding="utf-8")
        before = text
        sayac = 0
        for name in ASSETS:
            text, n = re.subn(
                r'(?<=[\'"(=])[^\'")\s]*?' + re.escape(name), base + name, text
            )
            sayac += n
        if text != before:
            path.write_text(text, encoding="utf-8")
            print(f"{path.name}: {sayac} gorsel yolu")
            toplam += sayac

    print(f"\nToplam {toplam} yol -> {base}" if toplam else "Degisiklik yok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
