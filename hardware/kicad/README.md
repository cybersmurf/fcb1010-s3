# Schéma nosné desky (KiCad)

| Soubor | Co to je |
|---|---|
| `fcb1010-s3.kicad_sch`, `fcb1010-s3.kicad_pro` | schéma, otevře se v KiCadu 7 a novějším |
| `gen_sch.py` | generátor schématu; zapojení je popsané v něm a schéma se z něj vyrábí |
| `expected-nets.json` | zamýšlené přiřazení pin → síť, vzniká při generování |
| `check_netlist.py` | porovná netlist vyexportovaný KiCadem se zamýšleným zapojením |
| `../schema-fcb1010-s3.pdf` | schéma v PDF |

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
- Pouzdra `fcb1010:ESP32-S3-DevKit_2x22_RM25.4mm` a `fcb1010:Uhelnik` zatím neexistují, vzniknou s návrhem desky.
- Deska (PCB) zatím není nakreslená. Kreslit se bude až po zkoušce na drátech.
