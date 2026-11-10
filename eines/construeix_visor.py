"""Munta la pàgina del visor: plantilla + dades de les plantes + foto de la rajola incrustada.

Ús: python construeix_visor.py
Llegeix visor/plantilla.html, visor/planta-baixa.json, visor/planta-primera.json i
visor/rajola-roure.jpg, i escriu visor/casa.html (un sol fitxer, sense dependències locals).
"""
import base64
import json
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
VISOR = ARREL / "visor"
PLANTES = ["planta-baixa.json", "planta-primera.json"]   # de baix a dalt


def main():
    plantilla = (VISOR / "plantilla.html").read_text(encoding="utf-8")
    dades = {"plantes": [json.loads((VISOR / f).read_text(encoding="utf-8")) for f in PLANTES]}
    dades_txt = json.dumps(dades, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    foto = base64.b64encode((VISOR / "rajola-roure.jpg").read_bytes()).decode("ascii")
    for marca in ("__DADES__", "__RAJOLA__"):
        if plantilla.count(marca) != 1:
            raise SystemExit(f"La plantilla ha de tenir exactament un {marca}")
    sortida = plantilla.replace("__DADES__", dades_txt).replace("__RAJOLA__", "data:image/jpeg;base64," + foto)
    desti = VISOR / "casa.html"
    desti.write_text(sortida, encoding="utf-8")
    print(f"{desti} ({desti.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
