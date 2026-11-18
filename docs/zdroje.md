# Zdroje k přestavbě FCB1010 na ESP32-S3

Všechny zdroje, které se v projektu použily, s poznámkou, co v nich je a jak moc se na ně dá spolehnout. Stav k 16. 11. 2026. Nové zdroje sem připisovat.

Spolehlivost: **A** = primární zdroj, přečtený; **B** = jeden kus nebo jedna zkušenost; **C** = neověřené tvrzení.

## Vnitřní zapojení FCB1010

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [Fractal forum: FCB1010 re-house project, str. 3](https://forum.fractalaudio.com/threads/fcb1010-re-house-project.24421/page-3) | Jediný zveřejněný pinout 14pinových konektorů předních desek, diody 1N4148 u spínačů, 3 vodiče pedálů, uchycení hlavní desky (3 sloupky + šroub přes chladič), phantom napájení přes MIDI. Kus z let 2009–2010. | B |
| [Practical Usage: The Behringer FCB1010 pedal board](https://practicalusage.com/the-behringer-fcb1010-pedal-board/) | Seznam IC hlavní desky (80C32, 27C256 v IC13, 24C16, 74HC273, ADC0832, 7805), deska MIDI s H11L1, typ spínače C&K PTS645SL43, typy číslic displeje, fotky. Autor má schéma, poskytuje ho jen e-mailem. | A |
| [Daniele Veratti: reverse engineering for Arduino](https://www.danieleveratti.com/behringer-fcb-1010-reverse-engineering-for-arduino/) (15. 1. 2017) | Slovní popis: dvě přední desky, LED se společným +5 V a samostatnými zeměmi, tlačítka se společnou zemí. 2 fotky, žádná tabulka pinů, žádný typ konektoru, nic o pedálech. Výtah níže. | A |
| [Daniele Veratti: death and resurrection with Arduino](https://www.danieleveratti.com/behringer-fcb-1010-death-and-resurrection-with-arduino/) (15. 1. 2017) | Úvod k opravě: FCB přestal posílat Program Change a pak se přestal zapínat. Plán nahradit hlavní desku Arduinem Mega a zachovat MIDI obvod, desky spínačů a pedály. Žádné technické údaje, výsledek neuveden. | A |
| [el34world: FCB1010 mods](https://el34world.com/Misc/Music/FCB_1.htm) | Fotky vnitřku, princip pedálů (IR LED, senzor, gradientní pásek), seřízení polohy desky senzoru. | A |
| [el34world: napájení po CAT5](https://el34world.com/Misc/Music/FCB_4.htm) | Úprava na 10 V AC po kabelu. | A |
| [diystompboxes: pedál FCB1010](https://www.diystompboxes.com/smfforum/index.php?topic=32510.0) | Senzor pedálu: LED, fotocitlivý prvek, dva odpory, 5 V. | B |
| [Sweetwater: kalibrace pedálů](https://www.sweetwater.com/sweetcare/articles/the-expression-pedals-on-my-behringer-fcb1010-midi-foot-controller-dont-work-properly-in-programming-mode/) | Postup kalibrace v původním firmwaru (zapnout s 1+3). | A |
| [Behringer: stránka produktu](https://www.behringer.com/en/products/0715-AAA) | Oficiální parametry: 60 × 221 × 687 mm, 4,34 kg, 10 W, vestavěný zdroj. | A |
| [pikobus.webnode.cz: Foot controler FCB1010](https://pikobus.webnode.cz/upg/foot-controler-fcb1010/) | Česká recenze a úpravy: phantom napájení, UnO, oprava pedálu přesměrováním LED. Žádné vnitřní zapojení. | A |
| [musiker-board: Phantomspeisen](https://www.musiker-board.de/threads/behringer-fcb1010-phantomspeisen.191491/) | Phantom napájení přes krajní piny MIDI zásuvky. | B |

### Výtah: Veratti (Arduino Mega)

- Původní napájení: transformátor 220 V → 9 V AC, usměrnění čtyřmi diodami na hlavní desce. Hlavní deska byla vadná, vyndal ji i s transformátorem a napájí z externího zdroje.
- Tlačítka: společný zemní vodič, každé tlačítko má vlastní vodič. O diodách se nezmiňuje.
- LED: původně společné +5 V a zem každé LED zvlášť. Při prvním pokusu vedl zem LED na výstup Arduina přes 1 kΩ, takže LED svítila při LOW.
- Nakonec všechny LED vypájel a otočil, aby je mohl spínat stavem HIGH se společnou zemí. Pro nás zbytečné: stačí spínat katody stavem LOW.
- Vodiče k pedálům a jejich LED odstřihl. Piny Arduina, kód ani schéma neuvádí.

## Přestavby na jiný mikrokontrolér

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [musiker-board: FCB1010 mit modernem Mikrocontroller bestücken](https://www.musiker-board.de/threads/fcb1010-mit-modernem-mikrocontroller-bestuecken.756515/) | Přestavba na ESP32-S3 s PedalinoMini. Výtah níže. | B |
| [GitHub: mackatack/FCBInfinity](https://github.com/mackatack/FCBInfinity) | Vlastní deska s Teensy++ 2.0 pro FCB (2012): schéma v PDF a Multisim, Gerbery, kód, seznam dílů. Výtah níže. | A |
| [mackatackblog](https://mackatackblog.wordpress.com/) | Deník stavby FCBInfinity, fotky, úprava napájení a MIDI po UTP. | A |
| [TEE1010: přestavba s Teensy 4.1, díl 3](https://forum.core-electronics.com.au/t/tee1010-part-3-modifying-the-insides-a-fcb1010-rebuild-with-a-teensy-4-1/11362) a [repozitář](https://github.com/ExpensiveNotes/TEE1010) | Čte původní desky spínačů přímo přes `INPUT_PULLUP` na 3,3 V. | A |
| [GitHub: alf45tar/PedalinoMini](https://github.com/alf45tar/PedalinoMini) | Firmware pro ESP32/ESP32-S3: web rozhraní, USB/BLE/Wi-Fi MIDI. Od v4 closed source, licence 1 € na MAC adresu (neověřený údaj). | A |
| [PedalinoMini: diskuse 440](https://github.com/alf45tar/PedalinoMini/discussions/440) | Diskuse k FCB1010 s PedalinoMini. | B |
| [GitHub: T-vK/PedalinoMini](https://github.com/T-vK/PedalinoMini) | Fork PedalinoMini z doby, kdy byl ještě open source (licence GPL v3, poslední commit 2. 7. 2025). Obsahuje konfiguraci pro `esp32-s3-devkitc-1-n16r8v` s kompletní mapou pinů německé přestavby. Výtah níže. | A |
| [GitHub: jspyve/FCB1010-lib](https://github.com/jspyve/FCB1010-lib) | Vlastní firmware pro **původní** hlavní desku (8051, SDCC), uvolněný jako public domain v roce 2019. Dokládá, jak původní deska obsluhuje periferie. Výtah níže. | A |
| [PJRC: Modded MIDI Foot Controller](https://www.pjrc.com/modded-midi-foot-controller/) | Shrnutí projektu TEE1010. | A |
| [Cantabile forum: FCB1010 na USB napájení](https://community.cantabilesoftware.com/t/behringer-fcb1010-foot-pedal-convert-to-usb-power-incorporate-midi-expression-quattro-with-single-cable/1819) | Původní elektronika odebírá 90 mA při 5 V. | B |

### Výtah: německá přestavba na ESP32-S3

- ESP32-S3 (asi 5 €), původní hlavní deska pryč, konektory desek vedené přímo na ESP32. Původní deska MIDI zůstala.
- 12 spínačů. Plánovaná matice 3×4 nebyla potřeba, zbylo 10 volných GPIO.
- Původní LED nahrazeny pásky WS2812B na jednom datovém pinu.
- Displej: nakonec OLED SSD1306 0,96" 128×64 na I2C; autor ho považuje za malý. Bez displeje se firmware špatně oživoval.
- Pedály: optické senzory, 3 piny (5 V, signál, GND), signál 0–5 V. Dělič 1,5 kΩ ze signálu na GPIO14 (pedál 1) a GPIO15 (pedál 2), 3 kΩ z GPIO na GND.
- Převodník úrovní na linkách MIDI.
- Síťový konektor nahrazen USB-C, přidán druhý USB-C a konektor antény. Baterie plánovaná, neosazená.
- Problémy: stavová LED mikrokontroléru ruší optické senzory (přelepit); web rozhraní zpočátku nešlo přes Wi-Fi; jiný uživatel hlásil kolísání hodnot pedálů při napájení z USB.

### Výtah: fork T-vK/PedalinoMini (mapa pinů na ESP32-S3-DevKitC-1 N16R8V)

Ze souboru `src/Pedalino.h` a `platformio.ini`:

| Funkce | GPIO |
|---|---|
| Tlačítka 1–4 | 12, 11, 10, 9 |
| Tlačítko 5 | 8 |
| Tlačítka 6–9 | 18, 17, 16, 15 |
| Tlačítka 10–12 | 7, 6, 5 |
| Expression 1 (levý), 2 (pravý) | 14, 13 (přes dělič) |
| MIDI OUT, MIDI IN | 1, 2 (přes převodník úrovní) |
| WS2812B data | 42 |
| OLED I2C SDA, SCL | 41, 40 |
| Baterie | 4 |
| Nepoužité | 21, 38, 39, 47, 48 |

Postaveno na `espressif32@6.9.0` (jádro Arduino 2.x). Jako hotový firmware je to záložní cesta, kdyby se vlastní kód zadrhl. Náš pinout se liší (pedály máme na ADC1, GPIO1 a 2), není důvod ho měnit.

### Výtah: FCB1010-lib (jak pracuje původní hlavní deska)

- Periferie jsou mapované do paměti od adresy 0x1FF8: latch společných vývodů, latch segmentů, latch pro relé a sloupce kláves.
- Komentář v kódu: LED se multiplexují co nejrychleji, tlačítka se debouncují v 6 × 8 krocích.
- Závěr: původní deska LED i tlačítka **multiplexuje** (LED spolu s displejem, tlačítka po sloupcích). Tím se vysvětlují diody 1N4148 u tlačítek a dvě anodové linky na spodní desce.
- Pro nás to nic nemění: na předních deskách má každé tlačítko a každá LED vlastní vodič, takže je můžeme zapojit napřímo bez multiplexu.
- Repozitář obsahuje i datasheety (W78C032, ADC0832, 24C16) a původní manuál. Schéma ani pinout konektorů v něm nejsou.

### Výtah: FCBInfinity (z obsahu repozitáře)

- Deska 160 × 40 mm, dvouvrstvá. Není to kopie obrysu původní desky.
- Konektory na desce: 2× dvouřadý 2×7 označený LOWER a UPPER (sběrnice LED a tlačítek), 2× 1×3 EXPLEFT a EXPRIGHT, MIDI IN/OUT, LCD 2×8.
- Signály na 2×7: jeden společný vodič LED (`lkat`/`ukat`), 5× LED, 6× tlačítko. To je 12 signálů na 14 pinech.
- LED a 3 číslice (SC56-11, společná katoda) řídí MAX7219. Napájení 10 V AC → můstek → 7805.
- Autor první desku vyhodil kvůli prohozenému pořadí pinů na konektoru horního panelu.
- Návod k instalaci je nedokončený. Uvádí, že některé kabely jsou do původní desky zapájené a musí se odstřihnout.
- Nejasné: jestli do lišt 2×7 pasovaly původní kabely, nebo nové.

## ESP32-S3 a USB MIDI

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| arduino-esp32 3.3.12, `libraries/USB/src/USBMIDI.h` | API třídy `USBMIDI` (noteOn, controlChange, pitchBend, readPacket). Ověřeno sestavením firmwaru. | A |
| [ESP_MIDI (collaborative-music-lab)](https://gh.r-mj.com/collaborative-music-lab/ESP_MIDI) | Pro USB MIDI musí být režim USB nastavený na OTG (TinyUSB). | A |
| [Espressif: USB Device Stack](https://docs.espressif.com/projects/esp-idf/en/v5.3/esp32s3/api-reference/peripherals/usb_device.html) | USB D− a D+ jsou na GPIO19 a GPIO20. | A |
| [Control Surface (tttapa)](https://tttapa.github.io/Control-Surface/Doxygen/d8/d4a/md_pages_MIDI-over-USB.html) | Alternativní knihovna pro MIDI ovladače, podporuje ESP32-S3. Zatím nepoužita. | A |
| Espressif: ESP32-S3 datasheet a Hardware Design Guidelines | Pull-up typ. 45 kΩ, VIL 0,25 × VDD, rozsah ADC při 12 dB do 2900 mV, 100 nF na vstupu ADC. Hodnoty převzaté z reportu. | B |

## MIDI a Mackie Control

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [MIDI 1.0 Electrical Specification Update CA-033](https://www.midi.org/wp-content/uploads/wpforo/default_attachments/1709416667-ca33-MIDI-10-Electrical-Specification-Update.pdf) | MIDI OUT při 3,3 V: 33 Ω na pin 4, 10 Ω na pin 5. Při 5 V 2× 220 Ω. | A |
| [TouchMCU: Mackie Control protocol](https://github.com/NicoG60/TouchMCU/blob/main/doc/mackie_control_protocol.md) | Čísla not, LED, fadery, SysEx handshake. | A |
| [libMackieControl](https://github.com/Do-sth-sharp/libMackieControl/blob/main/doc/MackieControl.md) | Totéž, druhý nezávislý popis. | A |
| [Apple: Control Surfaces Support Guide (PDF)](https://help.apple.com/pdf/logicpromac-css/en_US/logic-pro-mac-control-surfaces-support-guide.pdf) | Mackie Control v Logicu, ruční přidání zařízení. | A |
| [UA: Using MCU Control Surfaces with LUNA](https://help.uaudio.com/hc/en-us/articles/4406796987540) | LUNA podporuje ovladače jen přes MCU, vybírá se vstupní i výstupní port. | A |

## Boss GX-700

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [Roland: GX-700 Technical Specifications](https://support.roland.com/hc/en-us/articles/201946639-GX-700-Technical-Specifications) | 200 pamětí (100 User + 100 Preset), MIDI IN/OUT/THRU, jack pro expression pedál a dva jacky CONTROL. | A |
| [ManualsLib: GX-700 Owner's Manual, str. 50](https://www.manualslib.com/manual/3288415/Boss-Gx-700.html?page=50) | Volba patchů zprávou Program Change přes Program Change Map (str. 52 manuálu), patche 129 a výš jen přes mapu; ovládání parametrů zprávami Control Change podle Control Assign (str. 23). | A |
| [ManualsLib: GX-700 Owner's Manual, str. 57](https://www.manualslib.com/manual/3288415/Boss-Gx-700.html?page=57) | Ovládání z FC-200: CTL pedál posílá CC 80 (příklad: tuner, režim TOGGLE), EXP pedál CC 7 (příklad: OUTPUT LEVEL, režim NORMAL). | A |

Nepřečteno (stránky manuálu se nepodařilo načíst): výchozí Program Change Map, úplný seznam zdrojů pro Control Assign, tabulka MIDI implementace (str. 63), Manual Mode s FC-200. Hodnoty CC 7 / CC 80 / CC 1 jako výchozí nastavení FC-200 potvrzuje i manuál Boss GT-PRO.

## NUX MG-30 a ovládání více přístrojů

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [manuals.plus: NUX MG-30](https://manuals.plus/m/206215c9a5225df9b1380791ec87e711feba6c4121f3645526cdaa58d6c3604e) | Jack EXP 1 je 6,3mm TRS pro externí expression pedál nebo dvojitý spínač NMP-2. USB-C pro firmware, nahrávání a editor QuickTone. | A |
| [zZounds: NUX MG-30](https://www.zzounds.com/item--NUXMG30) | Text výrobce: s NMP-2 a spínačem CTRL jdou ovládat 3 bloky jako krabičky; USB slouží i pro MIDI. | A |
| [Arduino forum: Arduino a MG-30](https://forum.arduino.cc/t/connecting-arduino-to-a-multi-effect-guitar-processor/1177284) | Uživatel stavěl MIDI ovladač pro MG-30 a přes OTG redukci se mu nepodařilo spojit. | B |
| [PJRC forum: MG-300 na USB hostu Teensy](https://forum.pjrc.com/threads/62787-MIDI-device-stops-working-when-connected-through-hub-(using-USBHost_t36-library)?p=251973) | MG-300 (ne MG-30) funguje přímo na USB hostu Teensy 3.6, přes hub zlobí; patch se u něj mění zprávou CC 60. | B |
| [Kenton MIDI USB Host mk3](https://kentonuk.com/?p=404) | Adaptér USB host ↔ 5pinové MIDI pro zařízení class compliant; vyžaduje skutečně class compliant zařízení. Cena kolem 90 £. | A |
| [DOREMiDi UMH-20 (Reverb)](https://reverb.com/item/45962086-high-speed-usb-midi-host-box-midi-interface-adapter-usb-to-midi-converter) | Levnější USB MIDI host box, napájení 5 V z USB adaptéru. | B |
| [UA: Troubleshooting the USB Host MIDI Interface](https://help.uaudio.com/hc/en-us/articles/43206511122964) | Obecná zkušenost s USB host adaptéry u kytarových efektů včetně možného rušení v audiu přes USB. | A |

Neověřeno: které zprávy MIDI MG-30 přes USB přijímá, jestli je class compliant pro tyto adaptéry a které funkce jdou přiřadit na NMP-2.

## Původní firmware a čipy (nepoužijeme, pro úplnost)

| Zdroj | Co obsahuje | Spol. |
|---|---|---|
| [EurekaPROM](https://sites.google.com/a/eurekasound.com/www/eurekaprom) a [režim PP](https://sites.google.com/a/eurekasound.com/www/eurekaprom/pp) | Náhradní čip, 35 USD, verze 3.2 z roku 2016. V režimu PP posílají spínače CC, noty jen v režimu Specials. | A |
| FCB1010 Manager (Mountain Utilities), [fcb1010.online](https://fcb1010.online) | Editory pro původní firmware 2.4/2.5. | B |

## Konzultace s Gemini (16. 11. 2026)

Čtyři odpovědi od Gemini posloužily jako výchozí seznam tvrzení a zdrojů. Berou se jako **neověřená tvrzení (C)**; kontrola bod po bodu je v `pruzkum-vnitrni-zapojeni.md`. Texty samotné v repozitáři nejsou. Ze zdrojů, které jmenovaly, se nepodařilo dohledat vlákno „Behringer FCB1010 hardware mods“ na fóru Gig Performer a příspěvek na Redditu o PedalinoMini.

Co z nich neplatí nebo není doložené:

- pedály mají 3 vodiče, ne 4;
- LED je 5 na desku, ne 6, a spodní deska má dva anodové piny;
- „plochý kabel s roztečí 2,54 mm“ žádný zdroj nepotvrzuje;
- „matice nebo posuvné registry podle revize“ a „revize se spínaným zdrojem“ nejsou doložené;
- signál pedálu při napájení 5 V nesmí jít přímo na ADC;
- 2× 220 Ω u MIDI OUT platí pro 5 V (ve třetím textu už správně 33 Ω a 10 Ω);
- dělič 10 kΩ + 20 kΩ dá při 5 V 3,33 V, což je nad rozsahem ADC.

Co se potvrdilo: dvě přední desky a jejich rozdělení, 14 pinů, přímé zapojení bez matice, H11L1, EPROM v IC13, 7805, existence všech čtyř jmenovaných zdrojů, tip se skenem desky 1:1 jako podkladem do KiCadu.
