# FCB1010-S3: nákupní seznam

Stav k 18. 11. 2026. Ceny a dostupnost jsou z vyhledávání v ten den a mění se; kde cena chybí, nepodařilo se ji spolehlivě dohledat. Počty počítají s jedním kusem do zásoby u levných součástek.

## A. Objednat hned

Nezávisí na měření přístroje. Stačí na zkoušku na drátech i na finální desku.

| Položka | Ks | Kde | Cena za kus | Poznámka |
|---|---|---|---|---|
| OLED 2,42" 128×64, I2C, bílý (SSD1309) | 1 | LaskaKit, kód LA141115 | 17,16 € s DPH | **objednáno 18. 11. 2026 v poledne** (předpoklad: tento typ podle seznamu). Za původní červené okénko se nevejde, počítá se s novým pásem z kouřového plexi, viz `nalezy-z-fotek.md` |
| MCP23017-E/SP (DIP-28) | 2 | TME (201 ks skladem); záloha ecom.cz, Lhotský elektro | 38,40 Kč s DPH (TME) | expandér pro původní LED |
| SN74HCT125N (DIP-14) | 2 | GM electronic, kód 426-025 | 14 Kč | budič MIDI OUT a WS2812B; HCT stačí. Pozor, 74HCT125D (kód 952-167) je SMD |
| LP2951 nastavitelný LDO | 2 | **otevřené**: TME má LP2951ACN/NOPB (DIP-8) na 0 ks; GM electronic LP2951CM/NOPB (SO8, kód 935-006) je potřeba ověřit | – | napájení senzorů pedálů; verze od onsemi (LP2951ACN, LP2951CN) se už nevyrábí, hledat TI s příponou /NOPB. Náhradní typ zatím není ověřený, nekupovat naslepo |
| Patice DIP-28 úzká (300 mil), DIP-14 | po 2 | GM electronic | jednotky Kč | MCP23017-E/SP je úzké pouzdro; precizní patice GME 824-009 je široká a nehodí se, u kódu 823-007 šířku ověřit na prodejně |
| Dutinkové lišty 1×40, 2,54 mm | 4 | GM electronic | – | patice pro DevKit |
| Kolíkové lišty 1×40, 2,54 mm | 2 | GM electronic | – | |
| Odpory 0,25 W: 150 Ω (12), 220 Ω (4), 330 Ω (2), 470 Ω (14), 1 kΩ (4), 4,7 kΩ (4), 10 kΩ (4), 12 kΩ (2), 15 kΩ (4), 22 kΩ (2), 47 kΩ (14) | – | GM electronic | – | v závorce minimum pro jednu desku |
| Keramické kondenzátory: 100 nF (30), 470 nF (4), 10 µF (4) | – | GM electronic | – | |
| Odpory pro LP2951 (dělič výstupního napětí): 100 kΩ (2), 220 kΩ (2), trimr 100 kΩ (1) | – | GM electronic | – | přesné hodnoty až podle měření senzorů |
| Nepájivé pole (830 bodů) | 2 | Drátek, kód 1458404272 | 37 Kč | DevKit z Drátku má řady asi 25 mm od sebe a na jednom poli nechá jen jednu volnou řadu na každé straně, proto dvě pole vedle sebe |
| Propojky dupont M–M a M–F, sada 40 ks, 20 cm | po 1 | Drátek | 35 Kč a 33 Kč | zkouška na drátech |
| Panelový prodlužovací kabel USB-C (zásuvka s přírubou → vidlice), 20 až 30 cm | 1 | LaskaKit, Alza, AliExpress | – | na zadní panel |

## B. Objednat hned, pokud tu funkci chceš

| Položka | Ks | Kde | Cena za kus | K čemu |
|---|---|---|---|---|
| PhotoMOS AQY212EH (DIP-4) | 2 | TME (1 462 ks skladem) | asi 2,05 USD bez DPH | plovoucí spínací výstupy na zadní jacky místo původních relé K1, K2 (NUX místo NMP-2, kanály zesilovače) |
| Druhý ESP32-S3 DevKit, stejný typ jako ten, co máš | 1 | LaskaKit, Botland, TME | – | záloha; musí mít stejnou rozteč řad, jinak nesedí do patice |
| Lišta 8× WS2812B (5050, 5 V, 57 × 10 mm) | 2 | LaskaKit, kód LA145006B (černá) / LA145006W (bílá) | 1,39 € s DPH | jen na zkoušku barevných LED na nepájivém poli; skladem 102 a 64 ks |

K WS2812B (stav 18. 11. 2026): LaskaKit má pásky 60 LED/m jen v 5m rolích (IP65 černý 36,86 €, IP65 bílý 36,71 €, IP30 černý vyprodaný). Do přístroje se pásek nehodí: LED má po 16,6 mm, kdežto LED nad spínači jsou od sebe mnohem dál, takže by se musel rozstříhat na jednotlivé LED a propojit vodiči. Finální provedení barevných LED (jednotlivé destičky, nebo adresovatelné LED 5 mm THT typu WS2812D-F5 / PL9823 do původních otvorů) se rozhodne až podle měření: průměr otvorů pro LED a rozteč spínačů.

Místo dříve uvažovaného TLP222A je AQY212EH: Toshiba TLP222A je vedená jako ukončená výroba.

### Jaký DevKit ano a jaký ne

Musí to být deska s čipem **ESP32-S3** a rozložením pinů jako ESP32-S3-DevKitC-1 (2×22 pinů). Stav k 18. 11. 2026:

| Deska | Kde | Cena | Hodí se? |
|---|---|---|---|
| Espressif ESP32-S3-DevKitC-1 v1.1 (modul WROOM-1U) | RPishop, kód EBV003 | 929 Kč, skladem 2 ks | ano; modul 1U má jen konektor na anténu, pro USB a DIN MIDI nevadí |
| Waveshare ESP32-S3-DevKit-1-N16R8 | RPishop, kód WAV735 | 249 Kč, na objednávku asi 25 dnů | ano, pinově kompatibilní s DevKitC-1; rozteč řad ověřit |
| ESP32-S3 N16R8, vývojový modul (nespájený, lišty 2×22 v balení) | Drátek, kód 1745823675 | 279 Kč, skladem 205 ks | ano; 64 × 28 mm, převodník CH343, RGB LED na GPIO48; rozložení 2×22 odpovídá DevKitC-1, ale prodejce kompatibilitu ani rozteč řad neuvádí (podle šířky 28 mm nejspíš 25,4 mm), změřit |
| ESP32-S3 N16R8 s konektorem pro kameru OV5640 a slotem microSD | Drátek, kód 1785994570 | 287 Kč, skladem 29 ks | jen na zkoušku firmwaru, na desku ne (viz níže) |
| Espressif ESP32-C6-DevKitM-1 | LaskaKit | 498 Kč | **ne** |
| LaskaKit ESP32-S3-DEVKit | LaskaKit | – | ne, vlastní rozložení pinů a napájení z baterie |

Proč ne ESP32-C6: je to jiný čip (RISC-V) bez USB-OTG. Jeho „nativní“ USB umí jen sériovou linku a JTAG, takže se počítači neumí ohlásit jako zařízení USB MIDI. Deska má navíc jen 2×15 pinů, což na 12 spínačů, 2 pedály, I2C, MIDI a LED nestačí. Totéž platí pro C3 a H2. USB MIDI umí jen S2, S3 a P4.

Proč ne deska s konektorem pro kameru (Drátek 1785994570): čip je správný (ESP32-S3 N16R8, USB-C OTG i USB-C UART přes CH343), takže USB MIDI na ní poběží. Prodejce ale neuvádí pinout ani schéma. Podle rozměru 57 × 28 mm, CH343, kamery a slotu SD jde nejspíš o klon desky Freenove ESP32-S3-WROOM CAM (neověřeno). U té platí:

- kamera má na desce natvrdo vedené GPIO 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, tedy přesně piny, kde máme spínače, AUX, data LED a MIDI OUT; bez zasunuté kamery jsou použitelné, ale na GPIO 4 a 5 (sběrnice kamery) bývají pull-upy,
- slot SD používá GPIO 38, 39, 40 (u nás OUT1 a OUT2 na 39 a 40),
- na GPIO 2 je LED, a tam máme analogový vstup pedálu B,
- lišty jsou 2×20, ne 2×22, takže nesedí do stejné patice jako DevKitC-1.

## C. Počkat na měření

| Položka | Na čem závisí |
|---|---|
| Konektory pro přední desky (2×) | nejspíš žádné: svazky jsou do původní desky zapájené (14 vodičů, rozteč 2,0 mm) a do nové se zapájejí stejně, viz `nalezy-z-fotek.md` |
| Konektory pro pedály (2×) a LED pedálů (2×) | 3 a 2 vodiče, taky zapájené; nové konektory jen pokud se rozhodneme pro rozpojitelné provedení |
| Kolíkové lišty 2,54 mm a proužek univerzální desky | redukce pro zkoušku na drátech (jsou už v části A) |
| Konektory pro destičku MIDI a jacků | část 5 |
| Kouřové plexi místo původního černého pásu | rozměr pásu a otvoru v plechu pod ním; obraz displeje 2,42" je 55 × 27,5 mm, pás je vysoký asi 25 mm |
| Kouřové nebo čiré plexi před displej | rozměr výřezu |
| Distanční sloupky a šrouby | výška původních sloupků |
| Samotná deska (JLCPCB) | až po zkoušce na drátech |

## Kde co objednat

Stav k 18. 11. 2026 podle průzkumu obchodů. Položky označené „neověřeno“ se nepodařilo dohledat na stránkách obchodu.

| Obchod | Co | Doprava |
|---|---|---|
| Drátek | ESP32-S3 N16R8 (2 ks po 265,05 Kč), 2× nepájivé pole, dupont M–M a M–F | výdejní místo GLS 74 Kč, na adresu 114 Kč |
| LaskaKit | OLED 2,42" I2C LA141115 (objednáno), 2× lišta 8× WS2812B | Zásilkovna 68 Kč, Balíkovna 70 Kč, zdarma od 1 000 Kč |
| TME | 2× MCP23017-E/SP, 2× AQY212EH | cena dopravy neověřena; prodává i nepodnikatelům, nutná registrace |
| GM electronic, Brno, Přízova 283/16 (Po–Pá 9–18) | 2× SN74HCT125N, patice, lišty, odpory, kondenzátory | osobně; dostupnost na brněnské prodejně ověřit na webu |

Otevřené: LDO pro senzory pedálů (LP2951 v DIP-8 není skladem), panelový kabel USB-C.

Varianta „TME + RPishop“ nevychází: Waveshare ESP32-S3-DevKit-1-N16R8 je u RPishopu na objednávku asi 25 dnů a Waveshare OLED 2,42" je z výroby v režimu SPI (na I2C se přepíná přepájením dvou odporů).

## Co už máš

- ESP32-S3 DevKit (leží v práci). Potřebuju jeho přesné označení: potisk desky a modulu (např. ESP32-S3-DevKitC-1, modul WROOM-1 N16R8) a vzdálenost mezi řadami pinů. Klony mívají jinou rozteč řad než originál a patice na desce se kreslí podle ní.
- Původní destička MIDI s optočlenem a zásuvkami, původní LED na předních deskách, zadní jacky.

## Zdroje cen

- [LaskaKit: 2.42" 128x64 OLED display, I²C, white](https://www.laskakit.cz/en/2-42--128x64-oled-displej-i--c--bily/)
- [Lhotský elektro: MCP23017-E/SP](https://www.lhotsky-elektro.cz/MCP23017-E-SP-d3370.htm)
- [ecom.cz: MCP23017-E/SP](https://ecom.cz/eshop/detail/9360-MCP23017-E-SP)
- [GM electronic: lineární regulátory nastavitelné (LP2951CM/NOPB)](https://www.gme.cz/c/15204/linearni-regulatory-napeti-nastavitelne)
- [DigiKey: LP2951CN](https://www.digikey.com/en/products/detail/texas-instruments/LP2951CN/5056017)
- [RPishop: Espressif ESP32-S3-DevKitC-1 v1.1](https://rpishop.cz/esp32-a-esp8266/6143-espressif-vyvojova-deska-esp32-s3-devkitc-1-v11.html)
- [RPishop: Waveshare ESP32-S3-DevKit-1-N16R8](https://rpishop.cz/645315/waveshare-vyvojova-deska-esp32-s3-dev-kit-n16r8/)
- [Drátek: ESP32-S3 N16R8, vývojový modul (nespájený)](https://dratek.cz/arduino-platforma/180247-esp32-s3-n16r8-vyvojovy-modul-s-wifi-a-ble-5.0-nespajeny-s-pinovou-listou-v-baleni.html)
- [Drátek: ESP32-S3 s konektorem pro kameru OV5640](https://dratek.cz/arduino-platforma/232701-vyvojova-deska-esp32-s3-s-konektorem-pro-kameru-ov5640-wifi-bluetooth.html)
- [Freenove: piny kamery, SD a WS2812 na desce ESP32-S3-WROOM](https://docs.freenove.com/projects/fnk0102/en/latest/fnk0102/codes/Main/Preface.html)
- [GitHub profharris: přehled klonů ESP32-S3 CAM, 40 vs. 44 pinů](https://github.com/profharris/GOOUUU-Tech-ESP32-S3-CAM-Expansion-Board)
- [LaskaKit: lišta 8× WS2812B](https://www.laskakit.cz/en/8x-inteligentni-rgb-led-neopixel-pasek--ws2812b--5050--5v/)
- [LaskaKit: pásek WS2812B 60 LED/m IP65 5 m černý](https://www.laskakit.cz/en/led-pasek-neopixel-ws2812b-60led-m-ip65-5m-cerny/)
- [LaskaKit: Espressif ESP32-C6-DevKitM-1 (nevhodná)](https://www.laskakit.cz/espressif-esp32-c6-devkitm-1-wifi-6--bluetooth-5--zigbee/)
- [TME: MCP23017-E/SP](https://www.tme.eu/cz/details/mcp23017-e_sp/integrovane-obvody-interface-ostatni/microchip-technology/?brutto=1)
- [TME: LP2951ACN/NOPB](https://www.tme.eu/en/details/lp2951acn_nopb/ldo-adjustable-voltage-regulators/texas-instruments/)
- [TME: AQY212EH](https://www.tme.eu/en/details/aqy212eh/one-phase-solid-state-relays/panasonic/)
- [GM electronic: SN74HCT125N](https://www.gme.cz/v/1490661/texas-instruments-sn74hct125n-cmos-4x-budic-sbernice-s-3stavovymi-vystupy-negativni-aktivace)
- [GM electronic: patice 28 DIP](https://www.gme.cz/v/1498419/sokl-28-dip-patice)
- [GM electronic: prodejna Brno](https://www.gme.cz/prodejny/33)
- [Drátek: nepájivé pole 830 bodů](https://dratek.cz/arduino/1225-eses-nepajive-pole-830-pinu.html)
- [Drátek: kabely s konektory dupont](https://dratek.cz/308-kabely-oboustranne-osazene-konektory/)
- [Drátek: terminálový shield pro ESP32-S3 (rozteč řad 25 mm)](https://dratek.cz/arduino-platforma/232705-terminal-shield-s-napajecim-zdrojem-pro-esp32-s3-vyvojovy-modul.html)
- [Waveshare wiki: 2.42inch OLED Module](https://www.waveshare.com/wiki/2.42inch_OLED_Module)
- [RPishop: Waveshare ESP32-S3-DevKit-N16R8-M s piny](https://rpishop.cz/645319/waveshare-vyvojovy-modul-esp32-s3-devkit-n16r8-m-s-piny/)
- [HledejSoučástky.cz: AQY212](http://www.hledejsoucastky.cz/LastSearches/Show?lastsearch=aqy212)
- [Octopart: TLP222A(F), stav Obsolete](https://octopart.com/part/toshiba/TLP222A(F))
