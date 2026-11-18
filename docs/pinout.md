# FCB1010-S3: pinout a rozložení nosné desky (verze 0.2)

Stav k 16. 11. 2026. Podklad pro schéma v KiCadu. Zapojení vstupů (filtry, pull-upy, napájení senzorů) je podrobně v `obvody.md`; hodnoty odtud mají přednost před zkratkami v tabulkách níže. **Tabulky konektorů J1 a J2 vycházejí z měření cizího kusu (Fractal fórum) a platí až po ověření multimetrem.** Typ a rozteč konektorů zatím neznáme.

Změny proti 0.1: 5pinové MIDI je povinné, 74AHCT125 je povinný, zadní jacky umí vstup AUX i plovoucí spínací výstup, UP/DOWN a spínač 10 jsou na jiných pinech (uvolnily se tím dva piny s ADC pro AUX), větší displej.

## Bloky

```
                 USB-C (zadní panel)
                        |
   J1 spodní deska --+  |  +-- J5 displej OLED (I2C)
   J2 horní deska ---+--+--+-- U2 MCP23017 --> katody 10 LED
   J3 pedál A -------+ ESP32-S3 +-- U3 74AHCT125 --> J7 MIDI OUT, J6 WS2812B
   J4 pedál B -------+ DevKitC-1 +-- J7 MIDI IN (H11L1 na původní destičce)
   J8 AUX 1, 2 ------+           +-- J11 spínací výstupy (PhotoMOS) --> zadní jacky
                 SW1 BOOT, SW2 RESET
```

## GPIO na ESP32-S3-DevKitC-1

| GPIO | Funkce | Poznámka |
|---|---|---|
| 1 | Expression A | ADC1_CH0, dělič 10k/15k + 100 nF |
| 2 | Expression B | ADC1_CH1, dělič 10k/15k + 100 nF |
| 4 | Spínač 1 | interní pull-up, 100 nF na GND |
| 5 | Spínač 2 | |
| 6 | Spínač 3 | |
| 7 | Spínač 4 | |
| 15 | Spínač 5 | |
| 16 | Spínač 6 | |
| 17 | Spínač 7 | |
| 18 | Spínač 8 | |
| 8 | Spínač 9 | |
| 11 | Spínač 10 | |
| 41 | UP | |
| 42 | DOWN | |
| 9 | AUX 1 | ADC1_CH8, zadní jack 1: externí spínač nebo expression pedál |
| 10 | AUX 2 | ADC1_CH9, zadní jack 2 |
| 12 | WS2812B data | přes U3, volitelné |
| 13 | MIDI OUT (UART1 TX) | přes U3 na 5 V |
| 14 | MIDI IN (UART1 RX) | z H11L1 přes dělič 10 kΩ / 22 kΩ |
| 21 | I2C SDA | MCP23017 (0x20), OLED (0x3C), pull-up 4k7 na 3V3 |
| 47 | I2C SCL | pull-up 4k7 na 3V3 |
| 39, 40 | spínací výstupy OUT 1, OUT 2 | přes PhotoMOS, plovoucí kontakty na zadní jacky (MG-30 místo NMP-2, kanály zesilovače) |
| 0 | BOOT | tlačítko na zadní panel |
| EN | RESET | tlačítko na zadní panel |
| 19, 20 | nativní USB | jen přes konektor USB na DevKitu |
| 43, 44 | UART0 | ladicí výpis, nahrávání při oživování |
| 38 / 48 | RGB LED na DevKitu | ve firmwaru vypnout nebo přelepit |
| 3, 45, 46, 35–37 | nepoužívat | strapping, PSRAM |

## U2: MCP23017 (I2C 0x20, napájení 3,3 V)

Původních 10 LED má společnou anodu. Anody na 3,3 V, katody přes odpor na expandér, LED svítí při LOW.

| Pin MCP | Funkce | Odpor |
|---|---|---|
| GPA0–GPA4 | katody LED 1–5 | 150 Ω |
| GPB0–GPB4 | katody LED 6–10 | 150 Ω |
| GPA5–7, GPB5–7 | volné | header |

Červená LED asi 9 mA, všech deset 90 mA; expandér snese 25 mA na pin a 125 mA celkem. Odpory platí jen tehdy, když na předních deskách žádné nejsou.

## U3: 74AHCT125 (napájení 5 V)

| Hradlo | Vstup | Výstup |
|---|---|---|
| 1 | GPIO13 | MIDI OUT; odpory 220 Ω jsou na původní destičce MIDI |
| 2 | GPIO12 | WS2812B data přes 330 Ω |
| 3, 4 | volné | vstupy na GND |

MIDI OUT: oba odpory 220 Ω (R7, R8) jsou podle fotek na původní destičce MIDI, na nosné desce se neosazují.

## J1: spodní přední deska (14 pinů, neověřeno)

| Pin | Na přední desce | Kam na nosné desce |
|---|---|---|
| 1 | anoda LED 1, 2, 3 | 3V3 |
| 2 | anoda LED 4, 5 | 3V3 |
| 3 | katoda LED 5 | R → GPA4 |
| 4 | katoda LED 4 | R → GPA3 |
| 5 | katoda LED 3 | R → GPA2 |
| 6 | katoda LED 2 | R → GPA1 |
| 7 | katoda LED 1 | R → GPA0 |
| 8 | spínač 1 | GPIO4 |
| 9 | spínač 2 | GPIO5 |
| 10 | spínač 3 | GPIO6 |
| 11 | spínač 4 | GPIO7 |
| 12 | spínač 5 | GPIO15 |
| 13 | DOWN | GPIO42 |
| 14 | společný vodič spínačů | GND |

## J2: horní přední deska (14 pinů, neověřeno)

| Pin | Na přední desce | Kam na nosné desce |
|---|---|---|
| 1 | anoda LED 6–10 | 3V3 |
| 2 | katoda LED 10 | R → GPB4 |
| 3 | katoda LED 9 | R → GPB3 |
| 4 | katoda LED 8 | R → GPB2 |
| 5 | katoda LED 7 | R → GPB1 |
| 6 | katoda LED 6 | R → GPB0 |
| 7 | spínač 6 | GPIO16 |
| 8 | spínač 7 | GPIO17 |
| 9 | spínač 8 | GPIO18 |
| 10 | spínač 9 | GPIO8 |
| 11 | spínač 10 | GPIO11 |
| 12 | UP | GPIO41 |
| 13 | společný vodič spínačů | GND |
| 14 | nezapojeno | – |

U spínačů je v sérii dioda 1N4148. Musí být orientovaná tak, aby proud tekl z GPIO do společného vodiče (ověřit).

## J3, J4: expression pedály (3 piny, pořadí neověřeno)

| Pin | Funkce |
|---|---|
| 1 (červený) | +5 V z USB |
| ? | GND |
| ? | signál → 10 kΩ → GPIO1 (A) / GPIO2 (B); z pinu 15 kΩ a 100 nF na GND |

## J7: původní destička MIDI (lišta 1×4, protikus původní zástrčky z X18)

Stav k 18. 11. 2026, viz `nalezy-z-fotek.md`. Pin 1 je červený vodič. Zem na pinu 4 je změřená, pin 1 a 2 jsou přečtené z fotky spojů, pin 3 je odvozený. Piny 2 a 3 ověřit při zkoušce na drátech.

| Pin | Signál | Kam |
|---|---|---|
| 1 | +5 V | 5 V; napájí H11L1, pull-up R6 a odpor MIDI OUT k pinu 4 zásuvky |
| 2 | MIDI IN (výstup H11L1) | přes 10 kΩ na GPIO14, z GPIO14 22 kΩ na GND |
| 3 | MIDI OUT | výstup U3 hradlo 1 (5 V); odpory R7, R8 jsou na destičce |
| 4 | GND | GND |

Výstup H11L1 má na destičce pull-up R6 4,7 kΩ k 5 V, proto dělič: 3,0 V v klidu, pod 0,3 V při sepnutém optočlenu. Bez děliče by na GPIO14 bylo 5 V.

## Ostatní konektory

| Ozn. | Funkce | Piny |
|---|---|---|
| J5 | displej I2C | 3V3, GND, SDA, SCL |
| J6 | WS2812B (volitelné) | 5 V, DATA, GND |
| J8 | zadní jacky, varianta vstup | AUX1, AUX2, 3V3, GND |
| J11 | zadní jacky, varianta výstup (protikus původní zástrčky z X17, 4 piny) | 1 (červený) hrot A, 2 objímka, 3 hrot B, 4 objímka. Piny 2 a 4 jsou spojené, s GND desky se nespojují. Který hrot patří kterému jacku, zatím neurčeno |
| J9 | volné | GPA5–7, GPB5–7, 3V3, 5 V, GND |
| J10 | USB-C na panel | kabelem do konektoru USB na DevKitu |
| – | kostra | GND v jednom bodě |

## Zadní jacky: vstup, nebo výstup

Každý jack se kabelem zapojí buď do J8 (vstup AUX), nebo do J11 (spínací výstup). U varianty výstup jsou kontakty galvanicky oddělené (PhotoMOS AQY212EH v pouzdru DIP-4; dříve uvažovaný TLP222A se už nevyrábí) a objímka jacku nesmí být spojená se zemí desky ani s kostrou, jinak přes MG-30 vznikne zemní smyčka. Původní jacky jsou plastové na samostatné destičce, takže objímka je od panelu izolovaná (potvrzeno 18. 11. 2026).

Pro MG-30 (náhrada NMP-2): OUT1 mezi hrot a objímku, OUT2 mezi kroužek a objímku jednoho stereo jacku.

## Displej

Doporučení: **OLED 2,42" (SSD1309, 128 × 64) v režimu I2C**, na kablíku do J5, ve zvětšeném výřezu panelu.

- Přístroj leží na zemi a čte se ze stoje. Na 2,42" vyjdou tři číslice patche vysoké přes 20 mm, původní číslice měly 14 mm. Displej 1,3" by byl ze stoje špatně čitelný.
- SSD1309 se ovládá stejně jako SSD1306, knihovny jsou společné.
- Při nákupu hlídat, aby modul uměl I2C. Část modulů 2,42" se dodává nastavená na SPI a na I2C se přepíná přepájením odporů.
- Aktivní plocha je přibližně 55 × 28 mm; přesný výřez podle výkresu konkrétního modulu.
- Vlastní výřez řeší i zabarvení původního okénka: stačí čiré nebo kouřové plexi.

## Co ještě chybí do schématu

1. Typ a rozteč konektorů J1–J4 a zapojení destičky MIDI (středa).
2. Ověření tabulek J1 a J2 a pořadí vodičů pedálů (středa, zkouška na drátech).
3. Obrys desky a montážní otvory (středa).
4. Konkrétní modul displeje kvůli výřezu.
