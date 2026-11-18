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
- **Neověřeno měřením:** pořadí vodičů 14pinových svazků J1 a J2 (převzato z cizího kusu), pořadí vodičů pedálů J3 a J4, piny 2 a 3 svazku MIDI (J7), rozložení pinů DevKitu (U1, podle oficiálního ESP32-S3-DevKitC-1), pořadí pinů modulu OLED (J5).
- Propojky JP1 a JP2 dovolují obrátit polaritu čtení spínačů, kdyby diody na předních deskách byly orientované opačně.
- U4 (MCP1702-4002E/TO, 4,0 V) je volitelný; bez něj se spojí JP3 a senzory pedálů se napájejí z 5 V přes R24 a C5.
- Deska: součástky jsou rozmístěné bez překryvů (kontrola v `gen_pcb.py`). Spoje natáhl Freerouting 1.9.0: 1181 segmentů, 37 prokovů, 6,5 m spojů, šířka 0,3 mm, izolační mezera 0,2 mm. KiCad i `check_pcb.py` hlásí 0 nepropojených spojení (90 sítí).
- **Nekontrolováno:** DRC (izolační mezery, vzdálenost od hrany) se v KiCadu 7 nedá pustit z příkazové řádky; pustit v editoru desky (Kontrola → Kontrola návrhových pravidel).
- **K dodělání před výrobou:** širší spoje pro napájení (GND, +5V, +3V3 jsou teď 0,3 mm jako signály), rozlitá zem, popisky na potisku, ruční úprava nejdelších spojů. Polohy svazků podél hrany jsou odhad z fotek (±5 mm), rozteč řad DevKitu 25,4 mm je předpoklad pro klon, úhelníky podle otisku na papíře.
- Displej na desce není: připojuje se čtyřpinovým konektorem J5 a jeho držák se vyřeší podle skutečného modulu.
- Do výroby až po zkoušce na drátech.
