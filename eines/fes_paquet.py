"""Munta el paquet per editar els mobles sense GitHub ni Python: una carpeta i un zip.

Ús: python eines/fes_paquet.py
Escriu paquet/casa-mobles/ i paquet/casa-mobles.zip (la carpeta paquet/ no va al repositori). Conté:
- casa.html: el visor, que llegeix els mobles de mobles.txt (al seu costat) i, amb un clic, diu
  quin moble és i a quina línia, o les coordenades del punt;
- mobles.txt: el mateix fitxer que visor/mobles.txt;
- planol-planta-baixa.png i planol-planta-primera.png: parets, portes i finestres amb una
  quadrícula de 50 cm i les coordenades, fets amb les dades del model (no amb els plànols originals);
- PER-A-CLAUDE.txt: eines/paquet/PER-A-CLAUDE.txt més les mides de la casa, generades del JSON;
- LLEGEIX-ME.docx: eines/paquet/LLEGEIX-ME.md passat per Pandoc.
Quan tornin mobles.txt canviat, es copia a visor/ i es torna a muntar casa.html amb construeix_visor.py.
El paquet nou es munta apart (paquet/casa-mobles.nou) i només substitueix el d'abans si cap fitxer
d'aquest és obert: si el Word té el LLEGEIX-ME.docx obert, avisa i no toca res.
"""
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from construeix_visor import ARREL, MOBLES, munta, plantes

FONTS = ARREL / "eines" / "paquet"
NOM = "casa-mobles"
SORTIDA = ARREL / "paquet" / NOM

# ---------- Plànols ----------
PXM = 110            # píxels per metre
MARC = (-1.0, -1.0, 9.0, 12.6)   # el mateix marc per a les dues plantes (metres), perquè la quadrícula coincideixi
CAP = 150            # espai per al títol (px)
PEU = 120            # espai per a la llegenda (px)
C = {
    "fons": (255, 255, 255), "q5": (236, 239, 242), "q1": (203, 210, 216), "num": (110, 120, 128),
    "hab": (247, 241, 226), "esc": (226, 228, 230), "terrassa": (232, 229, 222), "paret": (52, 57, 61),
    "finestra": (143, 195, 230), "porta": (240, 184, 110), "volum": (138, 143, 147), "barana": (110, 98, 170),
    "tinta": (28, 35, 32), "suau": (92, 104, 98),
}


def font(nom, mida):
    for f in (nom, "segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(str(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / f), mida)
        except OSError:
            continue
    return ImageFont.load_default()


def dibuixa_planol(p, desti):
    W = round((MARC[2] - MARC[0]) * PXM)
    H = round((MARC[3] - MARC[1]) * PXM) + CAP + PEU
    img = Image.new("RGB", (W, H), C["fons"])
    d = ImageDraw.Draw(img)
    px = lambda x, y: ((x - MARC[0]) * PXM, (y - MARC[1]) * PXM + CAP)
    rect = lambda r, fill, outline=None, w=1: d.rectangle([px(r[0], r[1]), px(r[2], r[3])], fill=fill, outline=outline, width=w)
    f_tit, f_sub, f_num, f_hab, f_peu = font("seguisb.ttf", 34), font("segoeui.ttf", 21), font("segoeui.ttf", 17), font("seguisb.ttf", 20), font("segoeui.ttf", 19)

    # Quadrícula: cada 50 cm, i més marcada cada metre amb el número
    x = MARC[0]
    while x <= MARC[2] + 1e-9:
        sencer = abs(x - round(x)) < 1e-9
        d.line([px(x, MARC[1]), px(x, MARC[3])], fill=C["q1"] if sencer else C["q5"], width=1)
        if sencer and MARC[0] < x < MARC[2]:
            for yy, anc in ((MARC[1] + 0.12, "mt"), (MARC[3] - 0.12, "mb")):
                d.text(px(x, yy), f"{round(x)}", font=f_num, fill=C["num"], anchor=anc)
        x += 0.5
    y = MARC[1]
    while y <= MARC[3] + 1e-9:
        sencer = abs(y - round(y)) < 1e-9
        d.line([px(MARC[0], y), px(MARC[2], y)], fill=C["q1"] if sencer else C["q5"], width=1)
        if sencer and MARC[1] < y < MARC[3]:
            for xx, anc in ((MARC[0] + 0.12, "lm"), (MARC[2] - 0.12, "rm")):
                d.text(px(xx, y), f"{round(y)}", font=f_num, fill=C["num"], anchor=anc)
        y += 0.5

    for t in p.get("terrasses", []):
        d.polygon([px(*q) for q in t["poligon"]], fill=C["terrassa"])
    for h in p["habitacions"]:
        color = C["esc"] if h["id"] == "esc" else C["hab"]
        d.polygon([px(*q) for q in h["poligon"]], fill=color)
        for r in h["extra"]:
            rect(r, color)
    for r in p["parets"]:
        rect(r, C["paret"])
    for o in p["obertures"]:
        rect(o["r"], C["finestra"] if o["tipus"] == "finestra" else C["porta"], C["paret"])
    for v in p.get("volums", []):
        rect(v["r"], C["volum"])
    for b in p.get("baranes", []):
        rect(b["r"], C["barana"], C["barana"], 2)
    if "forat" in p:   # buit de l'escala, ratllat
        r = p["forat"]
        a, b = px(r[0], r[1]), px(r[2], r[3])
        tros = Image.new("RGB", (round(b[0] - a[0]), round(b[1] - a[1])), C["esc"])
        td = ImageDraw.Draw(tros)
        for k in range(-tros.height, tros.width, 22):
            td.line([(k, tros.height), (k + tros.height, 0)], fill=C["q1"], width=2)
        img.paste(tros, (round(a[0]), round(a[1])))
        d.text(px((r[0] + r[2]) / 2, (r[1] + r[3]) / 2), "Buit de l'escala", font=f_hab, fill=C["tinta"], anchor="mm",
               stroke_width=4, stroke_fill=C["esc"])

    # Noms
    for h in p["habitacions"]:
        d.text(px(*h["etiqueta"]), h["nom"], font=f_hab, fill=C["tinta"], anchor="mm", stroke_width=4, stroke_fill=C["hab"])
    for t in p.get("terrasses", []):
        xs = [q[0] for q in t["poligon"]]; ys = [q[1] for q in t["poligon"]]
        d.text(px((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2), t["nom"], font=f_hab, fill=C["suau"], anchor="mm")
    for o in p["obertures"]:
        if o["tipus"] == "entrada":
            r = o["r"]
            d.text(px((r[0] + r[2]) / 2, r[3] + 0.25), "Entrada", font=f_hab, fill=C["tinta"], anchor="mm")

    # Origen
    ox, oy = px(0, 0)
    d.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=(200, 60, 40))
    d.text((ox - 10, oy - 10), "0, 0", font=f_hab, fill=(200, 60, 40), anchor="rb")

    # Títol i llegenda
    d.text((40, 30), f"{p['nom']} · coordenades en metres", font=f_tit, fill=C["tinta"])
    d.text((40, 82), "x creix cap a la dreta, y creix cap avall. Quadrícula de 50 cm; números cada metre.", font=f_sub, fill=C["suau"])
    yl = H - PEU + 30
    xl = 40
    for color, txt in ((C["paret"], "Paret"), (C["finestra"], "Finestra"), (C["porta"], "Porta (deixa-hi pas)"),
                       (C["esc"], "Escala"), (C["volum"], "Llar de foc, xemeneia, ampit")):
        d.rectangle([xl, yl, xl + 34, yl + 24], fill=color, outline=C["paret"])
        d.text((xl + 44, yl + 12), txt, font=f_peu, fill=C["tinta"], anchor="lm")
        xl += 44 + d.textlength(txt, font=f_peu) + 34
    sostre = f"{p['alcada']:.2f}".replace(".", ",")
    d.text((40, yl + 46), f"Sostre a {sostre} m del terra. Els mobles no surten al plànol: són a mobles.txt.", font=f_peu, fill=C["suau"])
    img.save(desti, optimize=True)


# ---------- Text per a Claude ----------
def n(v):
    return f"{v:.3f}".rstrip("0").rstrip(".") if abs(v - round(v, 2)) > 1e-9 else f"{v:.2f}"


def rect_txt(r):
    return " ".join(n(v) for v in r)


def dades_casa(ps):
    L = ["DADES DE LA CASA (generades del model; no les canviïs)", ""]
    for p in ps:
        L.append(f"[{p['nom']}]  sostre a {n(p['alcada'])} m del terra d'aquesta planta")
        L.append("Habitacions (vores interiors, punts x,y seguint el contorn):")
        for h in p["habitacions"]:
            pts = " ".join(f"({n(x)},{n(y)})" for x, y in h["poligon"])
            nota = "  <- escala: no hi posis res" if h["id"] == "esc" else ""
            L.append(f"- {h['nom']}: {pts}{nota}")
        for t in p.get("terrasses", []):
            pts = " ".join(f"({n(x)},{n(y)})" for x, y in t["poligon"])
            L.append(f"- {t['nom']} (exterior): {pts}")
        if "forat" in p:
            L.append(f"Buit de l'escala (no s'hi pot posar res): {rect_txt(p['forat'])}")
        L.append("Portes (forat a la paret, x0 y0 x1 y1; deixa-hi 0.80 m de pas a cada costat):")
        for o in p["obertures"]:
            if o["tipus"] != "finestra":
                L.append(f"- {o['nom']}: {rect_txt(o['r'])}")
        L.append("Finestres (x0 y0 x1 y1; ampit = alçada on comença el vidre):")
        for o in p["obertures"]:
            if o["tipus"] == "finestra":
                L.append(f"- {o['nom']}: {rect_txt(o['r'])}, ampit {n(o['ampit'])}")
        if p.get("volums"):
            L.append("Altres elements fixos (x0 y0 x1 y1):")
            for v in p["volums"]:
                L.append(f"- {v['nom']}: {rect_txt(v['r'])}")
        L.append("Parets (rectangles x0 y0 x1 y1; cap moble hi pot entrar):")
        L.append("; ".join(rect_txt(r) for r in p["parets"]))
        L.append("")
    return "\n".join(L)


def pandoc():
    for c in (Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe", shutil.which("pandoc")):
        if c and Path(c).exists():
            return str(c)
    raise SystemExit("No trobo Pandoc")


def obert(f):
    """Cert si un altre programa té el fitxer obert (el Word bloqueja el .docx i no es pot esborrar)."""
    try:
        with open(f, "r+b"):
            return False
    except PermissionError:
        return True


def main():
    ps = plantes()
    zip_path = SORTIDA.with_suffix(".zip")
    # Es munta tot apart i el paquet d'abans no es toca fins que el nou és sencer i res no és obert.
    nou = SORTIDA.with_name(NOM + ".nou")
    nou_zip = SORTIDA.with_name(NOM + ".nou.zip")
    if nou.exists():
        shutil.rmtree(nou)
    nou.mkdir(parents=True)
    try:
        (nou / "casa.html").write_text(munta(extern=True), encoding="utf-8")
        shutil.copyfile(MOBLES, nou / "mobles.txt")
        for p in ps:
            nom = "planol-" + p["nom"].lower().replace(" ", "-") + ".png"
            dibuixa_planol(p, nou / nom)
        base = (FONTS / "PER-A-CLAUDE.txt").read_text(encoding="utf-8")
        (nou / "PER-A-CLAUDE.txt").write_text(base.rstrip() + "\n\n" + dades_casa(ps), encoding="utf-8")
        subprocess.run([pandoc(), str(FONTS / "LLEGEIX-ME.md"), "-o", str(nou / "LLEGEIX-ME.docx")], check=True)
        with zipfile.ZipFile(nou_zip, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(nou.iterdir()):
                z.write(f, f"{NOM}/{f.name}")
        vells = [*SORTIDA.iterdir()] if SORTIDA.exists() else []
        oberts = [f.name for f in [*vells, zip_path] if f.is_file() and obert(f)]
        if oberts:
            raise SystemExit(f"No he refet el paquet: {', '.join(oberts)} és obert en un altre programa "
                             "(potser el Word). Tanca'l i torna-ho a provar. El paquet d'abans és sencer.")
    except BaseException:
        shutil.rmtree(nou, ignore_errors=True)
        nou_zip.unlink(missing_ok=True)
        raise
    # La carpeta no s'esborra (pot estar oberta a l'Explorador): se'n canvia el contingut.
    SORTIDA.mkdir(parents=True, exist_ok=True)
    for f in vells:
        if not (nou / f.name).exists():
            shutil.rmtree(f) if f.is_dir() else f.unlink()
    for f in nou.iterdir():
        os.replace(f, SORTIDA / f.name)
    nou.rmdir()
    os.replace(nou_zip, zip_path)
    for f in sorted(SORTIDA.iterdir()):
        print(f"  {f.name} ({f.stat().st_size / 1024:.0f} KB)")
    print(f"{zip_path} ({zip_path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
