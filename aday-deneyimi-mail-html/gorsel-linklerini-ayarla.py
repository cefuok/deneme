#!/usr/bin/env python3
"""Sablonlardaki gorsel yollarini toplu degistirir.

HTML mailde gorseller mutlak URL olmak zorunda; goreli 'assets/...' yolu
sadece tarayici onizlemesinde calisir. Gondermeden once bunu calistirin.

    python3 gorsel-linklerini-ayarla.py https://cdn.ornek.com/tt-mail/

Geri almak icin:

    python3 gorsel-linklerini-ayarla.py assets/
"""
import pathlib
import re
import sys

ASSETS = ("tt-govde-arkaplan.png", "tt-surec-diyagrami.png", "tt-alt-gorsel.png")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base = sys.argv[1]
    if not base.endswith("/"):
        base += "/"

    here = pathlib.Path(__file__).parent
    changed = 0
    for path in sorted(here.glob("*-tasarim.html")):
        text = path.read_text(encoding="utf-8")
        before = text
        for name in ASSETS:
            # her yol bicimini (src=, background=, url(), v:fill src=) yakala
            text = re.sub(r'(?<=[\'"(=])[^\'")\s]*?' + re.escape(name), base + name, text)
        if text != before:
            path.write_text(text, encoding="utf-8")
            hits = sum(text.count(base + n) for n in ASSETS)
            print(f"{path.name}: {hits} gorsel yolu -> {base}")
            changed += 1

    if not changed:
        print("Degisiklik yok (dosya bulunamadi veya yollar zaten ayarli).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
