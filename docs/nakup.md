# FCB1010-S3: nákupní seznam

Stav k 18. 11. 2026. Ceny a dostupnost jsou z vyhledávání v ten den a mění se; kde cena chybí, nepodařilo se ji spolehlivě dohledat. Počty počítají s jedním kusem do zásoby u levných součástek.

## A. Objednat hned

Nezávisí na měření přístroje. Stačí na zkoušku na drátech i na finální desku.

| Položka | Ks | Kde | Cena za kus | Poznámka |
|---|---|---|---|---|
| OLED 2,42" 128×64, I2C, bílý (SSD1309) | 1 | LaskaKit, kód LA141115 | 17,16 € s DPH | při hledání skladem 5 ks; modul už je v provedení I2C |
| MCP23017-E/SP (DIP-28) | 2 | Lhotský elektro, ecom.cz, Farnell | 68 Kč (Lhotský) | expandér pro původní LED |
| 74AHCT125N nebo 74HCT125N (DIP-14) | 2 | GM electronic, TME; AHCT v DIP spíš AliExpress | – | budič MIDI OUT a WS2812B; HCT stačí |
| LP2951 nastavitelný LDO | 2 | GM electronic (LP2951CM/NOPB, SO8, kód 935-006); v DIP-8 DigiKey (LP2951CN/NOPB) | jednotky až desítky Kč | napájení senzorů pedálů; SO8 se dá ručně zapájet, na nepájivé pole je potřeba redukce SO8 → DIP |
| Patice DIP-28 úzká, DIP-14 | po 2 | GM electronic | – | |
| Dutinkové lišty 1×40, 2,54 mm | 4 | GM electronic | – | patice pro DevKit |
| Kolíkové lišty 1×40, 2,54 mm | 2 | GM electronic | – | |
| Odpory 0,25 W: 150 Ω (12), 220 Ω (4), 330 Ω (2), 470 Ω (14), 1 kΩ (4), 4,7 kΩ (4), 10 kΩ (4), 12 kΩ (2), 15 kΩ (4), 47 kΩ (14) | – | GM electronic | – | v závorce minimum pro jednu desku |
| Keramické kondenzátory: 100 nF (30), 470 nF (4), 10 µF (4) | – | GM electronic | – | |
| Odpory pro LP2951 (dělič výstupního napětí): 100 kΩ (2), 220 kΩ (2), trimr 100 kΩ (1) | – | GM electronic | – | přesné hodnoty až podle měření senzorů |
| Nepájivé pole (830 bodů) | 1 | LaskaKit, GM electronic | – | pokud nemáš |
| Propojky dupont M–M a M–F, sada 40 ks | po 1 | LaskaKit, GM electronic | – | zkouška na drátech |
| Panelový prodlužovací kabel USB-C (zásuvka s přírubou → vidlice), 20 až 30 cm | 1 | LaskaKit, Alza, AliExpress | – | na zadní panel |

## B. Objednat hned, pokud tu funkci chceš

| Položka | Ks | Kde | Cena za kus | K čemu |
|---|---|---|---|---|
| PhotoMOS AQY212EH (DIP-4) | 2 | Conrad a další | 60 Kč | plovoucí spínací výstupy na zadní jacky (NUX místo NMP-2, kanály zesilovače) |
| Druhý ESP32-S3 DevKit, stejný typ jako ten, co máš | 1 | LaskaKit, Botland, TME | – | záloha; musí mít stejnou rozteč řad, jinak nesedí do patice |
| Pásek WS2812B, 60 LED/m, 5 V, 0,5 m | 1 | LaskaKit | – | jen pro variantu s barevnými LED |

Místo dříve uvažovaného TLP222A je AQY212EH: Toshiba TLP222A je vedená jako ukončená výroba.

## C. Počkat na měření

| Položka | Na čem závisí |
|---|---|
| Konektory pro přední desky (2×) | typ a rozteč z protokolu, část 2 |
| Konektory pro pedály (2×) | rozteč a počet pinů, část 4 |
| Konektory pro destičku MIDI a jacků | část 5 |
| Odpory 220 Ω pro MIDI OUT | podle toho, jestli už jsou na destičce MIDI |
| Kouřové nebo čiré plexi před displej | rozměr výřezu |
| Distanční sloupky a šrouby | výška původních sloupků |
| Samotná deska (JLCPCB) | až po zkoušce na drátech |

## Co už máš

- ESP32-S3 DevKit (leží v práci). Potřebuju jeho přesné označení: potisk desky a modulu (např. ESP32-S3-DevKitC-1, modul WROOM-1 N16R8) a vzdálenost mezi řadami pinů. Klony mívají jinou rozteč řad než originál a patice na desce se kreslí podle ní.
- Původní destička MIDI s optočlenem a zásuvkami, původní LED na předních deskách, zadní jacky.

## Zdroje cen

- [LaskaKit: 2.42" 128x64 OLED display, I²C, white](https://www.laskakit.cz/en/2-42--128x64-oled-displej-i--c--bily/)
- [Lhotský elektro: MCP23017-E/SP](https://www.lhotsky-elektro.cz/MCP23017-E-SP-d3370.htm)
- [ecom.cz: MCP23017-E/SP](https://ecom.cz/eshop/detail/9360-MCP23017-E-SP)
- [GM electronic: lineární regulátory nastavitelné (LP2951CM/NOPB)](https://www.gme.cz/c/15204/linearni-regulatory-napeti-nastavitelne)
- [DigiKey: LP2951CN](https://www.digikey.com/en/products/detail/texas-instruments/LP2951CN/5056017)
- [HledejSoučástky.cz: AQY212](http://www.hledejsoucastky.cz/LastSearches/Show?lastsearch=aqy212)
- [Octopart: TLP222A(F), stav Obsolete](https://octopart.com/part/toshiba/TLP222A(F))
