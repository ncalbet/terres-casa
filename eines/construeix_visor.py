"""Munta la pàgina del visor: plantilla + dades de les plantes + mobles + foto de la rajola incrustada.

Ús: python construeix_visor.py
Llegeix visor/plantilla.html, visor/planta-baixa.json, visor/planta-primera.json, visor/mobles.txt i
visor/rajola-roure.jpg, i escriu visor/casa.html (un sol fitxer, sense dependències locals).

El paquet per editar mobles (eines/fes_paquet.py) fa servir munta(extern=True): la pàgina no porta
els mobles a dins sinó que llegeix mobles.txt, que ha d'estar al seu costat.
"""
import base64
import json
import re
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
VISOR = ARREL / "visor"
PLANTES = ["planta-baixa.json", "planta-primera.json"]   # de baix a dalt
MOBLES = VISOR / "mobles.txt"


def plantes():
    return [json.loads((VISOR / f).read_text(encoding="utf-8")) for f in PLANTES]


def munta(extern=False):
    plantilla = (VISOR / "plantilla.html").read_text(encoding="utf-8")
    dades_txt = json.dumps({"plantes": plantes()}, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    foto = base64.b64encode((VISOR / "rajola-roure.jpg").read_bytes()).decode("ascii")
    if extern:
        mobles = ('<script src="mobles.txt" onerror="__mobles.falta = true"></script>\n'
                  "<script>__mobles.edicio = true</script>")
    else:
        text = MOBLES.read_text(encoding="utf-8-sig")
        mobles = "<script>\n" + re.sub(r"</(script)", r"<\\/\1", text, flags=re.I) + "</script>"
    for marca in ("__DADES__", "__RAJOLA__", "__MOBLES__"):
        if plantilla.count(marca) != 1:
            raise SystemExit(f"La plantilla ha de tenir exactament un {marca}")
    return (plantilla.replace("__DADES__", dades_txt)
            .replace("__RAJOLA__", "data:image/jpeg;base64," + foto)
            .replace("__MOBLES__", mobles))


def main():
    desti = VISOR / "casa.html"
    desti.write_text(munta(), encoding="utf-8")
    print(f"{desti} ({desti.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
