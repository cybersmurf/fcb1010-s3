# Schéma nosné desky (KiCad)

| Soubor | Co to je |
|---|---|
| `fcb1010-s3.kicad_sch`, `fcb1010-s3.kicad_pro` | schéma, otevře se v KiCadu 7 a novějším |
| `gen_sch.py` | generátor schématu; zapojení je popsané v něm a schéma se z něj vyrábí |
| `expected-nets.json` | zamýšlené přiřazení pin → síť, vzniká při generování |
| `check_netlist.py` | porovná netlist vyexportovaný KiCadem se zamýšleným zapojením |
| `../schema-fcb1010-s3.pdf` | schéma v PDF |
| `gen_pcb.py` | generátor desky: rozmístění součástek a sítě; spouští se `/usr/bin/python3 gen_pcb.py` (potřebuje modul `pcbnew` z KiCadu) |
| `fcb1010-s3.kicad_pcb` | deska 229 × 41 mm, dvouvrstvá, součástky rozmístěné a spoje natažené autorouterem |
| `import_ses.py` | načte výsledek autorouteru Freerouting (`.ses`) do desky |
| `check_pcb.py` | nezávislá kontrola, že jsou v každé síti všechny pájecí body propojené |
| `../deska-fcb1010-s3.pdf`, `../deska-spoje.png` | deska se spoji |
| `../fcb1010-s3-gerber-v0.1.zip` | gerbery a vrtání pro výrobu |
| `fcb1010.pretty/` | vlastní pouzdra: DevKit 2×22 a úhelník |
| `parts.json` | seznam součástek (hodnota, pouzdro), vzniká při generování schématu |
| `../deska-rozmisteni.png` | obrázek rozmístění |

Postup po změně zapojení:

```
python3 gen_sch.py
kicad-cli sch export netlist -o fcb1010-s3.net fcb1010-s3.kicad_sch
python3 check_netlist.py fcb1010-s3.net
kicad-cli sch export pdf -o ../schema-fcb1010-s3.pdf fcb1010-s3.kicad_sch
```

Schéma se neupravuje ručně v editoru, jinak ho další generování přepíše.

## Stav (v0.1, 18. 11. 2026)

- Kontrola netlistu: 310 pinů, 90 sítí, bez rozdílů proti zadání.
- **Ověřeno z fotek (24. 11. 2026):** zapojení 14pinových svazků J1 a J2 (společný vodič, UP/DOWN, krajní spínač, napájení LED; pořadí prostředních pinů jednotlivě ne, dá se přemapovat ve firmwaru), rozložení pinů DevKitu a rozteč jeho řad 25,4 mm. Viz `docs/nalezy-z-fotek.md`.
- Orientace diod u spínačů: z fotek vychází společný vodič na GND a pull-up, tedy JP1 i JP2 v poloze A; při oživení ověřit.
- **Neověřeno:** pořadí vodičů pedálů J3 a J4, rozteč lišt X17 a X18 (na desce pouzdro JST XH 2,5 mm), pořadí pinů modulu OLED (J5).
- Propojky JP1 a JP2 dovolují obrátit polaritu čtení spínačů, kdyby diody na předních deskách byly orientované opačně.
- U4 (MCP1702-4002E/TO, 4,0 V) je volitelný; bez něj se spojí JP3 a senzory pedálů se napájejí z 5 V přes R24 a C5.
- Deska: součástky jsou rozmístěné bez překryvů (kontrola v `gen_pcb.py`). Spoje natáhl Freerouting 1.9.0: 1186 segmentů, 51 prokovů, 7,0 m spojů. Signály 0,3 mm, GND, +5 V a napájení senzorů 0,6 mm, +3V3 0,4 mm (s 0,6 mm se nedalo natáhnout). Izolační mezera 0,2 mm, spoje nejméně 0,6 mm od hrany desky. Na obou vrstvách je rozlitá zem.
- Kontroly (24. 11. 2026): KiCad i `check_pcb.py` hlásí 0 nepropojených spojení (90 sítí). Kontrola návrhových pravidel KiCadu (`drc.rpt`, pouští ji `import_ses.py`) nenašla žádný zkrat, porušení izolační mezery ani vzdálenosti od hrany. Zbývají jen upozornění: překryvy potisku, 2 zemní body připojených k rozlité zemi jedním můstkem místo dvou (jsou připojené i spojem) a překryvy obrysů součástek pod DevKitem, které jsou záměrné.
- Konektory svazků J1 až J4 mají pin 1 (červený vodič) na konci dál od displeje, stejně jako původní deska (fotka IMG_9456). J1 je blíž k displeji a patří ke spodní desce spínačů (1–5, DOWN), J2 k horní (6–10, UP), viz `docs/nalezy-z-fotek.md`.
- Popisky konektorů jsou na potisku.
- Výrobní podklady: `../fcb1010-s3-gerber-v0.1.zip` (gerbery a vrtání, 2 vrstvy, 229 × 41 mm, tloušťka 1,6 mm). Oválné otvory úhelníků jsou prokovené drážky 1,3 × 2,1 mm.
- Polohy 14pinových konektorů J1 a J2 jsou podle metru přiloženého k původní desce (plošky 24,5 až 50 mm a 58,7 až 84,4 mm od hrany u displeje, za předpokladu, že metr byl zaháknutý za tuto hranu). Polohy J3, J4 jsou odhad z fotek (±5 mm), úhelníky podle otisku na papíře.
- Displej na desce není: připojuje se čtyřpinovým konektorem J5 a jeho držák se vyřeší podle skutečného modulu.
- Deska je připravená k objednání prototypu. Zbylé neověřené body se dají vyřešit při osazování (pořadí vodičů při pájení, propojky, firmware).
