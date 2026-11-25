"""Munta les pàgines del visor: plantilla + dades de les plantes + mobles + foto de la rajola incrustada.

Ús: python construeix_visor.py
Per a cada casa de CASES, llegeix visor/plantilla.html, els JSON de les seves plantes, el seu fitxer de
mobles (si en té) i visor/rajola-roure.jpg, i escriu la seva pàgina (un sol fitxer, sense dependències locals):
- visor/casa.html: la casa de dues plantes (la de la dreta d'A12/A13), amb visor/mobles.txt.
- visor/casa-2.html: la casa d'una planta (la de l'esquerra d'A12), amb visor/mobles-casa-2.txt.

El paquet per editar mobles (eines/fes_paquet.py) fa servir munta(extern=True) amb la casa de dues
plantes: la pàgina no porta els mobles a dins sinó que llegeix mobles.txt, que ha d'estar al seu costat.
"""
import base64
import html
import json
import re
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
VISOR = ARREL / "visor"
MOBLES = VISOR / "mobles.txt"
SQ = 0.5 ** 0.5

CASES = {
    "casa": {
        "pagina": "casa.html",
        "plantes": ["planta-baixa.json", "planta-primera.json"],   # de baix a dalt
        "mobles": MOBLES,
        "titol": "Terres de la casa",
        "ullet": "Dues plantes · escala 1:50",
        "nota_m2": "Superfície útil aproximada de les dues plantes, sense terrasses, retalls ni sobrants.",
        "notes": [
            "El to exacte i la brillantor s'han de mirar amb la mostra física i amb llum de dia. Cada pantalla ensenya els colors a la seva manera.",
            "Mida de la peça suposada: 20 × 120 cm, col·locada a trencajunts amb junta de 2,5 mm.",
            "El roure fosc i el roure gris són la mateixa foto retocada, no rajoles reals.",
            "La cuina està feta a partir del render, amb mides aproximades.",
            "Al pis, l'alçada del sostre i la de les finestres són suposades.",
        ],
        "peu": "Font: plànols A12 i A13 (cotes). Pis a 3,00 m. Sostres a 2,70 m.",
        "altra": ("casa-2.html", "Veure la casa d'una planta"),
        # Al plànol el nord mira avall a l'esquerra (x cap a la dreta, y cap avall)
        "nord": [-SQ, SQ],
    },
    "casa-2": {
        "pagina": "casa-2.html",
        "plantes": ["casa-2-planta.json"],
        "mobles": VISOR / "mobles-casa-2.txt",
        "titol": "Terres de la casa d'una planta",
        "ullet": "Una planta · escala 1:50",
        "nota_m2": "Superfície útil aproximada de la casa, sense el pati, retalls ni sobrants.",
        "notes": [
            "El to exacte i la brillantor s'han de mirar amb la mostra física i amb llum de dia. Cada pantalla ensenya els colors a la seva manera.",
            "Mida de la peça suposada: 20 × 120 cm, col·locada a trencajunts amb junta de 2,5 mm.",
            "El roure fosc i el roure gris són la mateixa foto retocada, no rajoles reals.",
            "L'alçada del sostre i la de les finestres són suposades. La llar de foc és la del plànol, de terra a sostre.",
            "Els mobles són els que dibuixa el plànol, amb mides aproximades i els colors dels de l'altra casa.",
        ],
        "peu": "Font: plànol A12 (cotes), casa de l'esquerra. Sostres a 2,70 m.",
        "altra": ("casa.html", "Veure la casa de dues plantes"),
        # El cos principal va girat 42,41° respecte del full: el nord del full, passat al seu marc
        "nord": [-0.999, 0.045],
    },
}


def plantes(casa="casa"):
    return [json.loads((VISOR / f).read_text(encoding="utf-8")) for f in CASES[casa]["plantes"]]


def munta(extern=False, casa="casa"):
    C = CASES[casa]
    plantilla = (VISOR / "plantilla.html").read_text(encoding="utf-8")
    dades = {"casa": {"nord": C["nord"]}, "plantes": plantes(casa)}
    dades_txt = json.dumps(dades, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    foto = base64.b64encode((VISOR / "rajola-roure.jpg").read_bytes()).decode("ascii")
    if extern:
        mobles = ('<script src="mobles.txt" onerror="__mobles.falta = true"></script>\n'
                  "<script>__mobles.edicio = true</script>")
    else:
        text = C["mobles"].read_text(encoding="utf-8-sig") if C["mobles"] else "mobles`\n`\n"
        mobles = "<script>\n" + re.sub(r"</(script)", r"<\\/\1", text, flags=re.I) + "</script>"
    for marca in ("__DADES__", "__RAJOLA__", "__MOBLES__"):
        if plantilla.count(marca) != 1:
            raise SystemExit(f"La plantilla ha de tenir exactament un {marca}")
    e = lambda t: html.escape(t, quote=False)
    href, nom = C["altra"]
    textos = {
        "__TITOL__": e(C["titol"]),
        "__ULLET__": e(C["ullet"]),
        # Enllaç a l'altra casa (no al paquet de mobles, que només porta aquesta pàgina)
        "__ALTRA__": "" if extern else f'<p><a class="altra" href="{e(href)}">{e(nom)} →</a></p>',
        "__NOTA_M2__": e(C["nota_m2"]),
        "__NOTES__": "\n".join(f"        <li>{e(n)}</li>" for n in C["notes"]),
        "__PEU__": e(C["peu"]),
    }
    for marca, valor in textos.items():
        if marca not in plantilla:
            raise SystemExit(f"A la plantilla hi falta {marca}")
        plantilla = plantilla.replace(marca, valor)
    return (plantilla.replace("__DADES__", dades_txt)
            .replace("__RAJOLA__", "data:image/jpeg;base64," + foto)
            .replace("__MOBLES__", mobles))


def main():
    for casa, C in CASES.items():
        desti = VISOR / C["pagina"]
        desti.write_text(munta(casa=casa), encoding="utf-8")
        print(f"{desti} ({desti.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
