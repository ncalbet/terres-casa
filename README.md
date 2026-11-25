# Terres de la casa

Visor 3D de dues cases per comparar terres (roure clar, roure fosc i roure gris) i colors de paret, passejant per dins o mirant-les com una maqueta.

**Obrir el visor:**
- Casa de dues plantes: https://ncalbet.github.io/terres-casa/visor/casa.html
- Casa d'una planta: https://ncalbet.github.io/terres-casa/visor/casa-2.html

## Com està fet

- `visor/casa.html` és la pàgina de la casa de dues plantes, en un sol fitxer. Es genera amb `python eines/construeix_visor.py` a partir de `visor/plantilla.html`, `visor/planta-baixa.json`, `visor/planta-primera.json`, `visor/mobles.txt` i la foto `visor/rajola-roure.jpg`.
- `visor/casa-2.html` és la de la casa d'una planta, amb la mateixa plantilla i `visor/casa-2-planta.json` (sense mobles). Aquesta casa no va tota recta: el bloc de les habitacions 2 i 3 va a part, a `blocs`, amb el seu gir; els trossos on es troben els dos girs són a `parets_poligon`. Els textos del panell de cada casa són a `eines/construeix_visor.py`.
- Els JSON tenen la casa (parets, portes, finestres, escala). Els mobles, també la cuina, són a `visor/mobles.txt`: una caixa per línia (nom, x0 y0 x1 y1, alçada des de i fins a, material), en metres.
- `python eines/fes_paquet.py` fa un paquet per editar els mobles sense GitHub ni Python. Hi ha la pàgina, que llegeix `mobles.txt` del seu costat i amb un clic diu quin moble és o on és el punt; els plànols amb quadrícula; un text per donar a Claude; i les instruccions (`eines/paquet/`). El deixa a `paquet/`, que no es publica.
- Les mides són en metres, tretes de plànols a escala 1:50. Alguns valors són suposats (alçades del sostre i de les finestres, mida de la peça). La pàgina els detalla.
- `eines/comprova_sobre_planol.py` dibuixa les dades damunt del plànol en PDF per comprovar-les. Els plànols no són al repositori.
