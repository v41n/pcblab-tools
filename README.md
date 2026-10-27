# pcblab-tools

## ean_label.py – zatwierdzony generator etykiet EAN-13 (PDF)

Standard etykiet PCBLAB: SKU w jednej linii, EAN-13 z wydłużonymi kreskami skrajnymi i środkową,
cyfry pod kreskami danych (pierwsza z lewej), kod skracany tylko w wysokości, całość wyśrodkowana,
kontrola sumy kontrolnej EAN.

Wymagania: `pip install reportlab pillow` oraz czcionki DejaVu (`/usr/share/fonts/truetype/dejavu/`).

```bash
curl -sO https://raw.githubusercontent.com/v41n/pcblab-tools/main/ean_label.py
# 70x50 mm (domyślnie)
python3 ean_label.py out.pdf 70 50 "GL-RC-009S;5904183697352"
# 50x25 mm, kilka etykiet, z danymi importera (najmniejszy tekst)
python3 ean_label.py out.pdf 50 25 "slzb-06u;5906124219104" "slzb-mr5u;5904741320500" --imp
```

Każda etykieta to osobna strona PDF. Po wygenerowaniu warto sprawdzić odczyt kodu (np. pyzbar).
