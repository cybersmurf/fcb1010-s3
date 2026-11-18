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
- [RPishop: Espressif ESP32-S3-DevKitC-1 v1.1](https://rpishop.cz/esp32-a-esp8266/6143-espressif-vyvojova-deska-esp32-s3-devkitc-1-v11.html)
- [RPishop: Waveshare ESP32-S3-DevKit-1-N16R8](https://rpishop.cz/645315/waveshare-vyvojova-deska-esp32-s3-dev-kit-n16r8/)
- [Drátek: ESP32-S3 N16R8, vývojový modul (nespájený)](https://dratek.cz/arduino-platforma/180247-esp32-s3-n16r8-vyvojovy-modul-s-wifi-a-ble-5.0-nespajeny-s-pinovou-listou-v-baleni.html)
- [Drátek: ESP32-S3 s konektorem pro kameru OV5640](https://dratek.cz/arduino-platforma/232701-vyvojova-deska-esp32-s3-s-konektorem-pro-kameru-ov5640-wifi-bluetooth.html)
- [Freenove: piny kamery, SD a WS2812 na desce ESP32-S3-WROOM](https://docs.freenove.com/projects/fnk0102/en/latest/fnk0102/codes/Main/Preface.html)
- [GitHub profharris: přehled klonů ESP32-S3 CAM, 40 vs. 44 pinů](https://github.com/profharris/GOOUUU-Tech-ESP32-S3-CAM-Expansion-Board)
- [LaskaKit: lišta 8× WS2812B](https://www.laskakit.cz/en/8x-inteligentni-rgb-led-neopixel-pasek--ws2812b--5050--5v/)
- [LaskaKit: pásek WS2812B 60 LED/m IP65 5 m černý](https://www.laskakit.cz/en/led-pasek-neopixel-ws2812b-60led-m-ip65-5m-cerny/)
- [LaskaKit: Espressif ESP32-C6-DevKitM-1 (nevhodná)](https://www.laskakit.cz/espressif-esp32-c6-devkitm-1-wifi-6--bluetooth-5--zigbee/)
- [HledejSoučástky.cz: AQY212](http://www.hledejsoucastky.cz/LastSearches/Show?lastsearch=aqy212)
- [Octopart: TLP222A(F), stav Obsolete](https://octopart.com/part/toshiba/TLP222A(F))
