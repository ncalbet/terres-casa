"""Dibuixa les parets, obertures, habitacions i mobles del JSON damunt del plànol en PDF.

Ús: python comprova_sobre_planol.py <planol.pdf> <dades.json> <sortida.png>
Serveix per comprovar a ull que el model coincideix amb el plànol abans de fer el 3D.
Si el JSON porta "desplacament_planol" [dx, dy] (model = plànol + desplaçament), es té en compte.
"""
import json
import sys

import pdfplumber
from PIL import Image, ImageDraw

# Origen del model dins del PDF (punts) i punts per metre (escala 1:50).
OX, OY, K = 1417.201, 929.32, 56.6929
DPI = 150
S = DPI / 72


def main(pdf_path, json_path, out_path):
    dades = json.load(open(json_path, encoding="utf-8"))
    dx, dy = dades.get("desplacament_planol", [0, 0])
    ox, oy = OX - dx * K, OY - dy * K
    xs = [v for r in dades["parets"] for v in (r[0], r[2])]
    ys = [v for r in dades["parets"] for v in (r[1], r[3])]
    marge = 0.6
    caixa = (ox + (min(xs) - marge) * K, oy + (min(ys) - marge) * K, ox + (max(xs) + marge) * K, oy + (max(ys) + marge) * K)
    with pdfplumber.open(pdf_path) as pdf:
        img = pdf.pages[0].crop(caixa).to_image(resolution=DPI).original.convert("RGB")
    capa = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)

    def px(x, y):
        return ((ox + x * K - caixa[0]) * S, (oy + y * K - caixa[1]) * S)

    def rect(r, fill, outline):
        a, b = px(r[0], r[1]), px(r[2], r[3])
        d.rectangle([a, b], fill=fill, outline=outline, width=2)

    for t in dades.get("terrasses", []):
        d.polygon([px(*p) for p in t["poligon"]], fill=(120, 120, 120, 50), outline=(80, 80, 80, 255))
    for h in dades["habitacions"]:
        d.polygon([px(*p) for p in h["poligon"]], fill=(255, 190, 0, 50), outline=(200, 120, 0, 255))
        for r in h["extra"]:
            rect(r, (255, 190, 0, 90), None)
    for r in dades["parets"]:
        rect(r, (220, 30, 30, 110), (160, 0, 0, 255))
    for o in dades["obertures"]:
        color = {"finestra": (30, 120, 230, 140), "porta": (30, 170, 60, 140), "entrada": (130, 40, 200, 140)}[o["tipus"]]
        rect(o["r"], color, None)
    for m in dades.get("cuina", []) + dades.get("volums", []):
        rect(m["r"], (0, 160, 160, 70), (0, 110, 110, 255))
    for b in dades.get("baranes", []):
        rect(b["r"], (200, 0, 200, 120), (140, 0, 140, 255))
    if "forat" in dades:
        rect(dades["forat"], None, (0, 0, 0, 255))
    img = Image.alpha_composite(img.convert("RGBA"), capa).convert("RGB")
    img.save(out_path)
    print("desat", out_path, img.size)


if __name__ == "__main__":
    main(*sys.argv[1:4])
