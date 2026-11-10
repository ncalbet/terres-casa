# Terres de la casa

Visor 3D d'una casa de dues plantes per comparar terres (roure clar, roure fosc i roure gris) i colors de paret, passejant per dins o mirant-la com una maqueta.

**Obrir el visor:** https://ncalbet.github.io/terres-casa/visor/casa.html

## Com està fet

- `visor/casa.html` és la pàgina, en un sol fitxer. Es genera amb `python eines/construeix_visor.py` a partir de `visor/plantilla.html`, `visor/planta-baixa.json`, `visor/planta-primera.json` i la foto `visor/rajola-roure.jpg`.
- Les mides són en metres, tretes de plànols a escala 1:50. Alguns valors són suposats (alçades del sostre i de les finestres, mida de la peça). La pàgina els detalla.
- `eines/comprova_sobre_planol.py` dibuixa les dades damunt del plànol en PDF per comprovar-les. Els plànols no són al repositori.
