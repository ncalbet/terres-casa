---
title: "Mobles de la casa: com treballar-hi"
lang: ca
---

Aquesta carpeta té el visor 3D de la casa i tot el que cal per posar-hi, moure i treure mobles. No
cal instal·lar res: només un navegador (Chrome, Edge, Firefox o Safari) i internet.

**L'únic fitxer que canvies és `mobles.txt`.** Les parets, les portes i les finestres no s'hi poden
tocar, i així no es pot espatllar la casa.

# Què hi ha a la carpeta

| Fitxer | Què és |
|---|---|
| `casa.html` | El visor. Doble clic per obrir-lo. |
| `mobles.txt` | La llista de mobles: una línia, una caixa. **És el que canvies.** |
| `planol-planta-baixa.png` i `planol-planta-primera.png` | Els plànols amb una quadrícula de 50 cm i les coordenades. |
| `PER-A-CLAUDE.txt` | Les instruccions per a Claude. El penges a cada xat nou. |
| `LLEGEIX-ME.docx` | Aquest document. |

# 1. Per començar

1. **Descomprimeix el zip** (clic dret, *Extreu-ho tot*) i treballa sempre a la carpeta
   descomprimida. Si obres `casa.html` des de dins del zip, no trobarà els mobles.
2. **Obre `casa.html`** amb doble clic.
3. **Obre `mobles.txt`** amb doble clic: s'obre al Bloc de notes (al Mac, a TextEdit). Potser el
   veus amb el nom `mobles`, sense el `.txt`: és el mateix.
4. Deixa'ls tots dos oberts, l'un al costat de l'altre.

# 2. Com es llegeix una línia de mobles.txt

```
Taula                      1.89   1.05   2.71   2.68    0.73   0.77   fusta
```

- **El nom**: el que vulguis.
- **Els quatre primers números** són el rectangle que ocupa el moble vist des de dalt, en metres:
  la x i la y d'una cantonada, i la x i la y de la cantonada oposada. Aquesta taula va de x = 1,89 a
  x = 2,71 i de y = 1,05 a y = 2,68.
- **Els dos següents** són l'alçada: des d'on i fins on, comptant des del terra. Aquesta taula és
  només el tauler, de 0,73 a 0,77 m.
- **L'última paraula** és el material: `moble`, `fusta`, `noguera`, `blanc`, `teixit`, `pedra`,
  `negre`, `inox`, `vidre` o `paret` (agafa el color de les parets). Hi pots afegir un color, com
  `teixit #5b6e8c` per a una tela blava. Els codis de color es troben buscant «selector de color» a
  Google.

On és cada punt:

- El **0, 0** és la cantonada de dalt a l'esquerra dels plànols. La **x** creix cap a la dreta i la
  **y** cap avall. Mira-ho als plànols PNG.
- Els números van amb **punt**, com `2.20` (també s'entén `2,20`).

Altres coses:

- Un moble és **una o més caixes**. La taula de la cuina és un tauler i quatre potes; un sofà seria
  el seient, el respatller i dos braços.
- Les línies que comencen per `#` són **notes** i no es dibuixen. Si poses `#` davant d'un moble,
  desapareix i no el perds.
- Tot el que hi ha sota `[Planta baixa]` és de baix; el que hi ha sota `[Planta primera]`, de dalt.
- **No toquis la primera línia ni l'última.** Sense elles no es llegeix res.

# 3. Com saber on és cada cosa

Al visor, fes **un clic** (sense arrossegar):

- **Sobre un moble:** surt a baix el nom, la línia de `mobles.txt` on és i les seves mides, i el
  moble queda marcat amb un requadre vermell.
- **Sobre el terra:** surten les coordenades x i y d'aquell punt i l'habitació.

Funciona passejant i a la **Maqueta**, que és la manera més còmoda: es veu tota la planta des de
dalt. Apunta't els números per saber on vols les coses.

# 4. Els canvis petits, fes-los tu

És més ràpid que demanar-ho a Claude:

- **Moure:** suma o resta el mateix número als dos x (cap a la dreta o l'esquerra) o als dos y (cap
  avall o amunt). Per exemple, 30 cm cap a la dreta: +0.30 al primer i al tercer número. Recorda
  moure totes les caixes del moble (les potes també).
- **Allargar o escurçar:** canvia només un dels dos números.
- **Treure:** posa `#` al davant o esborra la línia.
- **Fer-ne un altre d'igual:** copia la línia i canvia'n els números.

Després, **desa** (`Ctrl+S`; al Mac, `Cmd+S`) i, al visor, **torna a carregar la pàgina** (`F5`; al
Mac, `Cmd+R`). Al peu del panell de la dreta hi diu quantes caixes ha llegit.

**Abans d'un canvi gros, fes una còpia de `mobles.txt`** (selecciona'l a la carpeta, `Ctrl+C` i
`Ctrl+V`: sortirà una còpia amb un altre nom). Si alguna cosa s'espatlla, esborra `mobles.txt` i
canvia el nom de la còpia a `mobles`.

# 5. Els canvis grans, amb Claude

1. Obre [claude.ai](https://claude.ai) i comença **un xat nou**.
2. **Penja-hi tres fitxers** (amb el clip o arrossegant-los): `PER-A-CLAUDE.txt`, `mobles.txt` i el
   plànol de la planta on treballes.
3. **Demana-ho tot en un sol missatge**, amb les mides si les saps. Per exemple:

   > Llegeix PER-A-CLAUDE.txt i fes els canvis a mobles.txt. Planta baixa, sala: un sofà de 2,40 m
   > de tela gris fosc d'esquena a la paret de l'escala, mirant als finestrals; davant, una tauleta
   > de noguera d'1,10 × 0,60 i una catifa de 2 × 3 m a sota de tots dos. Al costat de la llar de foc,
   > una butaca blanca.

4. Claude et tornarà el `mobles.txt` sencer. **Copia'l tot** (a sobre del bloc hi ha el botó
   *Copiar*), ves a `mobles.txt`, selecciona-ho tot (`Ctrl+A`), enganxa (`Ctrl+V`), desa i torna a
   carregar el visor.
5. Si alguna cosa no t'agrada, digues-ho **al mateix xat**: «el sofà, 20 cm més a prop de la
   finestra».

# 6. Si surt un avís vermell

Si una línia de `mobles.txt` no s'entén, el visor no la dibuixa i t'ho diu a dalt: **el número de
línia, el principi de la línia i què hi falla**. La resta de mobles es veuen igualment.

- Si és fàcil (falta un número, el material està mal escrit, has posat centímetres en lloc de
  metres), arregla-ho tu. Per trobar la línia, busca-la amb `Ctrl+F`.
- Si no, copia el text de l'avís i enganxa'l a Claude, al mateix xat.
- Si diu que **no pot llegir `mobles.txt`**, s'ha espatllat la primera o l'última línia: torna a la
  còpia. Si diu que **no el troba**, és que no has descomprimit la carpeta o li has canviat el nom.

# 7. Per estalviar temps i missatges

El Claude gratuït té un límit de missatges cada poques hores.

- **Demana moltes coses en un sol missatge.**
- **Els canvis petits, fes-los tu** (apartat 4).
- **No pengis mai `casa.html` a Claude:** és molt gran i no li cal.
- **Quan el xat s'allargui** o Claude comenci a liar-se, obre'n un de nou i torna a penjar-hi els
  tres fitxers, amb l'últim `mobles.txt`.
- Si Claude et torna només un tros del fitxer, digues-li: «torna'm el mobles.txt sencer».
- Si tens les mides d'un moble de veritat (d'un catàleg o d'una botiga), dona-les-hi.

# 8. El que no es pot fer

- Els mobles són **caixes rectes**, sempre paral·leles a les parets: no es poden girar en diagonal
  ni fer rodons. Una taula rodona serà quadrada.
- Un llum es pot dibuixar, però **no fa llum**.
- **Les parets, les portes i les finestres no es toquen** des d'aquí. Si en vols canviar alguna,
  apunta-ho i m'ho dius.

# 9. Quan acabis

**Envia'm només el fitxer `mobles.txt`** (per correu o per WhatsApp). Jo el poso a la web de la casa.
