# Behringer FCB1010 – co je uvnitř a jak na něj navázat vlastní ESP32-S3 desku (ověřovací report)

Výsledek hloubkového průzkumu z 16. 11. 2026. Uloženo beze změn obsahu. Značky: OVĚŘENO = potvrzeno v primárním zdroji, PRAVDĚPODOBNÉ = jeden nebo nepřímý zdroj, NEOVĚŘENO = nepodařilo se potvrdit.

**Hlavní závěr:** Přední desky FCB1010 jsou zapojené přímo, bez matice: na každé desce je 14pinový konektor, každé tlačítko i každá LED má vlastní vodič a LED mají společnou anodu. Gemini se ale spletl v několika detailech, které rozhodují o návrhu PCB. LED je na každé desce jen 5, ne 6 (UP/DOWN žádnou LED nemají). Každé tlačítko má v sérii diodu 1N4148. Spodní deska má dvě anodové linky, ne jednu. Expression senzory mají 3 vodiče (5 V / GND / signál), ne 4. Že jde o „plochý kabel s roztečí 2,54 mm“, nepotvrdil žádný zdroj. Rozteč a typ konektoru proto musíš ve středu změřit, a je to položka číslo 1 na checklistu.

## TL;DR
- **Potvrzeno:** 2 přední desky (1–5 + DOWN, 6–10 + UP), každá na 14pinovém konektoru s přímým zapojením. LED mají společnou anodu (+5 V) a samostatné katody. Tlačítka mají společnou zem a sériové diody. Na MIDI desce je H11L1, firmware je v 27C256 v pozici IC13, 5 V dělá 7805, procesor je Philips P80C32 (rodina 8051). Hodnoty MIDI pro 3,3 V (33 Ω / 10 Ω) i všech 12 tvých MCU not (80–95) sedí.
- **Vyvráceno nebo nepodložené:** 4vodičové pedály (ve skutečnosti 3 vodiče), 6 LED na desku (ve skutečnosti 5), „1 společné + pro LED“ na spodní desce (ve skutečnosti 2). Pro „ribbon 2,54 mm“, revizi se spínaným zdrojem, „matici nebo shift registry podle revize“ ani pro vazbu hmotnosti 3,5 kg na novou revizi jsem nenašel žádný primární zdroj. Oficiální hmotnost je 4,34 kg.
- **Pro návrh:** 12 tlačítek dej přímo na GPIO s pull-upem (funguje i přes diody, ověřeno na Teensy). 12 LED se na DevKitC-1 vedle MIDI a WS2812 už nevejde, použij MCP23017 (I²C) a LED spínej v katodách. Pedály napájej z 5 V a signál veď přes dělič s poměrem ≈0,6 a kondenzátor 100 nF. Pozor: 3místný displej sedí na původní hlavní desce, takže s ní zmizí.

## Kontrola Geminiho tvrzení bod po bodu

| # | Tvrzení (Gemini) | Verdikt | Zdroj a co přesně říká |
|---|---|---|---|
| 1a | Repo „FCBInfinity“ (mackatack) | **OVĚŘENO – existuje**, ale obsah je jiný | https://github.com/mackatack/FCBInfinity – složky `Create a PCB`, `Installation`, `Schematics`, `Teensyduino`, `Partlist.md`, `faq.md`. Jde o schéma a Gerbery *jeho vlastní* Teensy desky a kód, ne o schéma originálu ani tabulku pinoutu originálních konektorů. |
| 1b | Blog „mackatackblog“ | **OVĚŘENO – existuje** | https://mackatackblog.wordpress.com/ – deník stavby z roku 2012: Teensy++, MAX7219 pro LED a číslice („MAX7219 IC to control all indicator leds and led digits“), fotky, mod napájení a MIDI přes UTP. Pinout originálu tam není, jen zmínka o chybě v jeho zapojení konektoru horního panelu („Led1, Led2, Led3, lbtn4, Led5, is not how the connector is wired“). |
| 1c | „FCB1010 reverse engineering“, Daniele Veratti | **OVĚŘENO – existuje**, ale je stručné | https://www.danieleveratti.com/behringer-fcb-1010-reverse-engineering-for-arduino/ – slovní popis a 2 fotky, žádná tabulka pinů, žádný typ konektoru. Dráty odstřihl. |
| 1d | Web „Practical Usage“ | **OVĚŘENO – existuje** | https://practicalusage.com/the-behringer-fcb1010-pedal-board/ – seznam IC hlavní desky, fotky, komentáře. Autor uvádí, že má kompletní schéma, ale nezveřejnil ho („Contacted by email“). |
| 2 | „Standardní 14pin a 4pin konektory“ | **Napůl.** 14pin OVĚŘENO, 4pin VYVRÁCENO | Practical Usage: „There is a 14 pin connector there“. Pedály mají 3 vodiče (Fractal forum: „these 3 leads are attached to connectors on the main board“). |
| 3 | 2 přední desky: 1–5 + DOWN, 6–10 + UP | **OVĚŘENO** | Veratti: „one with buttons and leds 1,2,3,4,5 and the DOWN button, the second with buttons 6,7,8,9,10 with the correspoding LEDs and the button UP“. |
| 4 | 14žilový ribbon 2,54 mm; 1× GND, 1× +LED, 6 tlačítek + 6 LED | **Většinou špatně.** 14 pinů OVĚŘENO. Rozteč a „ribbon“ NEOVĚŘENO. Rozložení VYVRÁCENO | Pinout z Fractal fóra (tabulka níže): LED je 5 na desku, spodní deska má 2 anodové piny, horní deska má pin 14 nezapojený a tlačítka mají sériové diody. Konektor je popsán jako „multipin connectors, similar to those used in computers“ a autor stříhal jednotlivé dráty („just cut all the wires“), což ukazuje spíš na diskrétní vodiče v krimpovacím pouzdře než na plochý kabel (PRAVDĚPODOBNÉ). |
| 5 | „Matice nebo shift registry podle revize“ | **NEOVĚŘENO / zavádějící** | Přední desky jsou přímé. Na hlavní desce jsou 3× 74HC273 („2 are used to control the 7-segments LED digits and 1 is used to receive the pedal inputs“, Practical Usage), takže originál spínače i LED nejspíš multiplexuje na straně hlavní desky. Diody u spínačů tomu odpovídají (PRAVDĚPODOBNÉ). Žádný zdroj nedokládá, že by se to mezi revizemi lišilo. |
| 6 | Pedál: IR LED + fototranzistor, 4 vodiče, 2 pro LED a 1 pro kolektor | **Princip OVĚŘEN, 4 vodiče VYVRÁCENO** | el34world: „A LED and a Infrared Sensor assembly… Gradient sensor strip“. Fractal: 3 vodiče, červený = pin 1. Komentář na Practical Usage: „Red – 5VDC (feeder for LED), one black for GND and one black for variable resistance“ (PRAVDĚPODOBNÉ, autor si nebyl jistý). diystompboxes: „a LED, a LDR and two resistors… it's 5v through the pedal circuit“. |
| 7 | H11L1 na MIDI desce | **OVĚŘENO** | Practical Usage: „Midi IN-OUT board. The IC (IC1: H11L1) on that board is a simple opto-isolator“. |
| 8 | Dvě revize: transformátor vs. spínaný zdroj, jiné úchyty | **NEOVĚŘENO** | Žádný z přečtených zdrojů spínaný zdroj nezmiňuje. Transformátor 9 V AC je doložen v letech 2011, 2012, 2017 i 2020 (Practical Usage, mackatack, Veratti, komentář „Mr Pityla“ z 2020: „getting 9V AC at the yellow cables“). |
| 9 | EPROM v IC13; 5 V z 7805 | **OVĚŘENO** | Practical Usage: „IC13: 27C256… firmware“, „IC2: T805: Voltage regulator, 5 Volts“. Autor v komentáři: „4 diodes, then … a condenser … and finally through a 7805“. |
| 10 | 3,5 kg nové vs. 4,34 kg staré | **Napůl.** 4,34 kg OVĚŘENO, vazba na revize NEOVĚŘENO | Behringer (aktuální stránka) uvádí „Weight approx. 4.34 kg“ a stále „Built-in power supply… IEC power connector“: https://www.behringer.com/en/products/0715-AAA. Údaj 3,5 kg pochází z uživatelské tabulky na musiker-board (https://www.musiker-board.de/threads/midi-board-sammlung-inkl-technischer-daten.76180/) a k revizi se nevztahuje. |

**Německé vlákno a Reddit:** Vlákno na musiker-board (https://www.musiker-board.de/threads/fcb1010-mit-modernem-mikrocontroller-bestuecken.756515/, založil „6stringtheory“ 31. 12. 2024) se výzkumnému agentovi nepodařilo otevřít. Jeho obsah (senzory 5V/signál/GND, 12 tlačítek bez matice, WS2812B, stavová LED ruší optiku) proto v reportu zůstává **NEOVĚŘENO** z primárního zdroje. Nezávisle ho ale podporují: 3vodičové senzory (Fractal, Practical Usage), přímé zapojení tlačítek (Veratti, TEE1010) a IR princip senzorů (el34world). K vláknu se váže fork https://github.com/T-vK/PedalinoMini. V diskusi https://github.com/alf45tar/PedalinoMini/discussions/440 to uživatel morpheus1306 komentuje: „I noticed, he did not use LEDs for the expression pedals“. Autor PedalinoMini dodává: „all the hardware is connected to the motherboard with connectors“ (OVĚŘENO ze snippetu). Reddit příspěvek se nenašel (**NEOVĚŘENO**).

*Poznámka mimo report: to vlákno se mi dříve v téže konverzaci otevřít podařilo, výtah z něj je v `zdroje.md`.*

## Details

### B1. Hlavní deska (podle Practical Usage, kus koupený nový v roce 2011)

| Pozice | Součástka | Funkce | Stav |
|---|---|---|---|
| IC8 | Philips P80C32SBAA | MCU, rodina 8051 bez interní ROM | OVĚŘENO (rodinu 8051 potvrzuje i https://github.com/jspyve/FCB1010-lib: „replacing it with an Atmel 8051“) |
| IC13 | 27C256 (32 kB EPROM) v patici | firmware, autorova verze „2.501E“ | OVĚŘENO |
| IC14 | M5M5256FP | 32 kB SRAM | OVĚŘENO |
| IC6 | 24C16 | I²C EEPROM s uživatelskými presety | OVĚŘENO (komentář untergeekDE) |
| IC9 | 74HC373 | adresový latch 8051 | OVĚŘENO |
| IC5 | „74HC130“ (překlep, nejspíš dekodér 74HC138) | generuje takty a clear pro IC3/10/11 | PRAVDĚPODOBNÉ |
| IC3, IC10, IC11 | 74HC273 | 2× pro segmenty displeje, 1× pro vstupy pedálů | OVĚŘENO |
| IC12 | ADC0832 („C0832C“) | 8bit ADC pro expression pedály | OVĚŘENO |
| IC7 | TL7705ACD | reset a supervisor | OVĚŘENO |
| IC2 | 7805 | +5 V | OVĚŘENO |
| – | tranzistorová a odporová pole | buzení segmentů displeje | OVĚŘENO |
| – | 2 relé | výstupy SWITCH 1/2 | OVĚŘENO („relays“); typ NEOVĚŘENO |

- **Displej:** sedí přímo na hlavní desce („Main Board: Display“). Číslice jsou LDD5125 (dvojitá) a SD5685, obě se společnou anodou (komentář autora Practical Usage). Behringer uvádí „3-digit LED display“. **Důsledek: s vyjmutím hlavní desky přijdeš o displej i o indikační LED na panelu displeje**, pokud je na carrier nenahradíš. (OVĚŘENO)
- **Jacky SWITCH 1/2** jsou na samostatné malé desce zapojené kabelem do hlavní desky (mackatack: „Disconnect the plug for the external switch 1&2 from the FCB circuit board“). OVĚŘENO.
- **Uchycení:** „There are 3 mounting studs on the PCB… There is a 4th bolt/nut through a transistor heat sink“ (Tubetonez, Fractal). Rozměry desky ani souřadnice otvorů nikde publikované nejsou (NEOVĚŘENO).
- **Pinout konektorů hlavní desky (pedály, MIDI, switch deska, transformátor) ani referenční označení konektorů** se v žádném zdroji nenašly (NEOVĚŘENO).

### B2. Přední desky – pinout (Fractal forum, Tubetonez, cca 2009–2010)

Zdroj: https://forum.fractalaudio.com/threads/fcb1010-re-house-project.24421/page-3 – „Pin 1 is the red lead… the switches have diodes feeding their outputs… 4148… black band at one end, this end solders to the switch. The other end of the diode is what I label as +, while "-" is a common feed to all switches.“ **Stav: OVĚŘENO jako publikované měření jednoho kusu. Autor sám píše „I think this is correct“ (to se týká pedálů), takže na tvém kusu to ověř multimetrem.**

| Pin | Spodní deska (1–5 + DOWN) | Horní deska (6–10 + UP) |
|---|---|---|
| 1 (červený) | anoda LED 1, 2, 3 | anoda LED 6–10 (všech pět) |
| 2 | anoda LED 4, 5 | katoda LED 10 |
| 3 | katoda LED 5 | katoda LED 9 |
| 4 | katoda LED 4 | katoda LED 8 |
| 5 | katoda LED 3 | katoda LED 7 |
| 6 | katoda LED 2 | katoda LED 6 |
| 7 | katoda LED 1 | tlačítko 6 (anoda diody) |
| 8 | tlačítko 1 | tlačítko 7 |
| 9 | tlačítko 2 | tlačítko 8 |
| 10 | tlačítko 3 | tlačítko 9 |
| 11 | tlačítko 4 | tlačítko 10 |
| 12 | tlačítko 5 | UP |
| 13 | DOWN | společný „−“ tlačítek |
| 14 | společný „−“ tlačítek | nezapojeno |

*(Autor číslo tlačítka uvádí v rámci řádku „SW1–SW6“, „SW6“ je u něj UP/DOWN. Přepočet na čísla 6–10 udělal výzkumný agent.)*

- **LED mají společnou anodu.** Nezávisle to potvrzuje Veratti: „The LEDs… share a +5 Volts wire and every LED has a separate ground wire“. OVĚŘENO.
- **Kde jsou sériové odpory LED:** NEOVĚŘENO. Ani jeden zdroj neuvádí rezistor na přední desce. Veratti přidával vlastní 1 kΩ, z čehož plyne, že odpory jsou nejspíš na hlavní desce (PRAVDĚPODOBNÉ). Počítej s rezistory na své desce.
- **Diody 1N4148 v sérii s každým tlačítkem** (OVĚŘENO, Fractal). Při čtení pull-upem tedy LOW na pinu odpovídá úbytku na diodě, ne nule.
- **Typ tlačítka:** C&K PTS645SL43 („The part is available here… PTS645SL43 LFS“, Practical Usage, odpověď na dotaz k vadnému spínači č. 2). OVĚŘENO.
- **Čtení přes pull-up funguje v praxi.** TEE1010 (Teensy 4.1, 3,3 V) čte originální desky přímo: `pinMode(cFoot, INPUT_PULLUP)` pro 12 nožních spínačů (https://forum.core-electronics.com.au/t/tee1010-part-3-modifying-the-insides-a-fcb1010-rebuild-with-a-teensy-4-1/11362). Mackatack (FAQ): „A Teensy board has a pull-up resistor built in for the push buttons“. OVĚŘENO.

### B3. Expression pedály

- **Princip:** IR LED, gradientní pásek (od tmavého po průhledný) a IR senzor (el34world, https://el34world.com/Misc/Music/FCB_1.htm). OVĚŘENO.
- **Zapojení:** 3 vodiče, červený = pin 1, konektor na hlavní desce (Fractal). Pravděpodobné přiřazení je červená = +5 V (napájí LED i senzor), černá = GND, černá = signál (Practical Usage, komentář). Uvnitř je „LED, a LDR [fototranzistor] and two resistors“ a 5 V (diystompboxes, https://www.diystompboxes.com/smfforum/index.php?topic=32510.0). Stav: PRAVDĚPODOBNÉ. Přiřazení dvou černých vodičů musíš změřit.
- **Výstupní rozsah:** přímé měření ve voltech se nenašlo. Uživatel na musiker-board při kalibraci originálu (8bit ADC0832) viděl min. „07“ a max. „db“ hex. Při Vref = 5 V to odpovídá zhruba 0,14 V až 4,3 V (PRAVDĚPODOBNÉ, Vref neověřeno).
- **Známé problémy:** nedosažení plného rozsahu 0–127 kvůli osové nesouososti LED a senzoru nebo kvůli tomu, že pásek dře o desku. Desku lze posunout dvěma šrouby (el34world, OVĚŘENO). Odezva je lineární, proto se na fórech řeší „plastic around the photo-sensors“ (vguitarforums, PRAVDĚPODOBNÉ).
- **Kalibrace ve stock firmwaru:** zapni přístroj s podrženými spínači 1+3, pak postupně stiskni všechny spínače, pak DOWN, A heel/toe, B heel/toe, každé potvrď UP (Sweetwater, https://www.sweetwater.com/sweetcare/articles/the-expression-pedals-on-my-behringer-fcb1010-midi-foot-controller-dont-work-properly-in-programming-mode/). OVĚŘENO. Firmware si ukládá min/max, takže ve vlastním firmwaru udělej totéž.

### B4. MIDI deska a napájení

- **H11L1 na MIDI IN** (OVĚŘENO). MIDI OUT/THRU je jediná zásuvka. „MIDI merge function allows for soft through“ (Behringer spec), takže THRU i merge dělá firmware, ne hardware (OVĚŘENO). Zapojení konektoru MIDI desky k hlavní desce: NEOVĚŘENO.
- **Transformátor:** sekundár 9 V AC (žluté vodiče), Graetzův můstek ze 4 diod, elektrolyt, 7805 (Practical Usage, Veratti). Primár má dvě odbočky (modrá 110 V, červená 220 V). Pojistka „T50mA“ pro 230 V a T100mA pro 115 V. Spotřeba 10 W (Behringer). OVĚŘENO.
- **Phantom napájení přes MIDI:** napětí se přivádí na krajní piny 1 a 3 zásuvky MIDI OUT (Fractal: „pins 1 & 3 of the MIDI out connector… it is the two outside pins“; musiker-board: https://www.musiker-board.de/threads/behringer-fcb1010-phantomspeisen.191491/). Varianta se 10 V AC po CAT5: https://el34world.com/Misc/Music/FCB_4.htm. OVĚŘENO. Pro tebe to není potřeba, napájet budeš z USB 5 V.

### C. Revize

| Oblast | Co je doloženo | Stav |
|---|---|---|
| Napájení | transformátor 9 V AC doložen 2011–2020; spínaný zdroj nedoložen; Behringer dodnes uvádí „Built-in power supply… IEC“ | revize se spínaným zdrojem NEOVĚŘENO |
| Firmware | V2.2 (komentář JAM), „min. 2.3“ pro expression funkce (musiker-board), V2.5 (riban-bw/fcb1010), „2.501E… the last one“ (Practical Usage) | OVĚŘENO pro 2.x; řada 1.x se nenašla |
| Přední desky a konektory | jediný publikovaný pinout pochází z kusu z let 2009–2010 (Fractal), tedy nejbližší tvému stáří | změny mezi revizemi NEOVĚŘENO |
| Senzory | ve všech zdrojích 3 vodiče | OVĚŘENO bez rozlišení revize |
| Display | LDD5125 + SD5685 (Practical Usage 2011/2017) | OVĚŘENO pro ten kus |

**Jak poznat revizi po otevření:** štítek na EPROM IC13 (verze firmwaru, např. formát „2.501E“). Dále silkscreen a číslo DPS na hlavní desce, datové kódy na 80C32, 27C256 a 24C16 (formát RRTT) a typ zdroje (toroid nebo EI transformátor se žlutými vodiči). Číslo verze při zapnutí se v dokumentaci nenašlo, NEOVĚŘENO.

### D. Praktické závěry pro carrier PCB

**D1. Konektory (hlavní blokující bod).** Typ ani rozteč žádný zdroj neuvádí (NEOVĚŘENO). Že jde o 2×7 IDC krabicový konektor, je podle reportu **nepravděpodobné**: popis „multipin… similar to those used in computers“, stříhání jednotlivých drátů a „pin 1 = red lead“ ukazují na jednořadé krimpovací pouzdro s diskrétními vodiči. Kandidáti (PRAVDĚPODOBNÉ, rozhodne měření):
- 2,54 mm jednořadý (Molex KK 254 / 22-27-2141, kompatibilní s 1×14 kolíkovou lištou): vzdálenost pinů 1–14 je 33,02 mm.
- JST XH 2,5 mm (B14B-XH-A): 32,50 mm. Rozdíl 0,52 mm přes 14 pinů je pro footprint fatální, proto měř posuvkou.
- JST PH 2,0 mm: 26,0 mm.

Footprint udělat přesně podle naměřené rozteče a konektor osadit stejného typu, jaký je na původní hlavní desce. Nejjednodušší a nejbezpečnější je **vypájet originální konektory ze staré hlavní desky a osadit je na novou**.

*Poznámka mimo report: deska FCBInfinity má pro přední desky footprinty 2×7, viz `zdroje.md`. Rozpor vyřeší měření.*

**D2. Tlačítka.** 12 GPIO s interním pull-upem, aktivní v LOW, společný „−“ obou desek na GND. Úbytek na 1N4148 při ~60 µA (interní pull-up má podle Espressif ESP32-S3 Series Datasheet typicky 45 kΩ, „RPU Internal weak pull-up resistor — 45 — kΩ“) bude kolem 0,4–0,5 V. To je pod mezí VIL, kterou tentýž datasheet uvádí jako „0.25 × VDD“ (≈ 0,82 V), ale rezerva je malá. Externí silnější pull-up úbytek naopak zvětší. Doporučení: nechat interní pull-up, firmwarově debouncovat a na PCB přidat 100 nF na vstup, nebo diody na předních deskách přemostit (PRAVDĚPODOBNÉ, inženýrský odhad; TEE1010 to s diodami provozuje).

**D3. LED.** Počet GPIO: DevKitC-1 vyvádí GPIO 0–21 a 35–48. Po odečtení 0/3/45/46, 19/20, 43/44, 35–37 a RGB (38 nebo 48) zbývá 22 pinů: 1, 2, 4–18, 21, 39–42, 47 a 38/48. Mínus 2 ADC, 12 tlačítek, 1 WS2812 a 2 MIDI UART dává **5 volných**. 10 LED (ne 12, viz výše) se tedy přímo nevejde. **Doporučení: MCP23017** (I²C na 2 pinech, 16 výstupů):
- Všechny anody (spodní pin 1+2, horní pin 1) připoj na **+3,3 V**, každou katodu přes vlastní rezistor (≈120–150 Ω pro červenou LED, ~10 mA) na pin MCP23017, který LED rozsvěcí stavem LOW.
- Anody nedávej na 5 V, když je MCP na 3,3 V: v klidu by mezi 5 V a 3,3 V zůstalo ~1,7 V a LED by mohly doutnat a cpát proud do ochranných diod.
- Pokud chceš anody na 5 V (víc jasu), dej mezi MCP a katody **ULN2803A** (otevřený kolektor, snese 5 V).
- 74HCT595 je zbytečný, MCP23017 je čistší.
- Alternativa, kterou už podporuje firmware: WS2812B do 5mm otvorů (THT varianty). Pak ale řeš převodník úrovně 3,3→5 V na data (např. 74AHCT1G125) a dobrou mechaniku.

**D4. Pedály → ADC.** Senzor nech na **5 V**: sériový odpor IR LED je dimenzovaný na 5 V a při 3,3 V by klesl proud LED i rozsah. Signál veď přes dělič s poměrem ≈0,6, tedy **10 k (horní) + 15 k (dolní)**: 4,3 V dá 2,6 V, což je v efektivním rozsahu, který Espressif v ESP32-S3 Hardware Design Guidelines uvádí pro 12 dB („the effective measurement range is 0 ~ 2900 mV“). Teoretických 5 V by dalo 3,0 V, tedy nad tímto rozsahem, ale tolik senzor podle odhadu nedá; pokud ve středu naměříš víc než ~4,7 V, zvol dělič 10 k + 12 k. K tomu **100 nF z ADC pinu na GND** a v softwaru průměrování nebo hystereze. Proč ne 1,5k+3k nebo 2,2k+3,3k: výstup fototranzistoru je vysokoimpedanční (pull-up či emitorový odpor v jednotkách až desítkách kΩ, NEOVĚŘENO) a nízký dělič by ho zatížil a zdeformoval křivku. Proč ne 10k+20k: při 5 V dá 3,33 V, a ESP-FAQ k tomu říká „An input voltage exceeding 2900 mV is undefined.“ Nízkou zdrojovou impedanci pro vzorkovací kapacitu ADC zajistí kondenzátor, ne nízký dělič. (Dělič je inženýrský návrh; kondenzátor přímo doporučuje Espressif v ESP32-S3 Hardware Design Guidelines: „Please add a 0.1 μF filter capacitor between ESP pins and ground when using the ADC function to improve accuracy.“)
- **Rozptýlené světlo:** senzor je IR. Onboard RGB LED na DevKitu vypni nebo zakryj, desku umísti mimo dohled senzorů a štěrbinu senzoru zakryj černou páskou. Hlášení „stavová LED ruší optiku“ z německého vlákna je v reportu NEOVĚŘENO, ale fyzikálně PRAVDĚPODOBNÉ.

**D5. MIDI 3,3 V (OVĚŘENO, CA-033, https://www.midi.org/wp-content/uploads/wpforo/default_attachments/1709416667-ca33-MIDI-10-Electrical-Specification-Update.pdf):**
- MIDI OUT: **RA = 33 Ω 0,5 W** z +3,3 V na pin 4, **RC = 10 Ω 0,25 W** z TX na pin 5. Pro 5 V platí 220 Ω / 220 Ω. Specifikace předpokládá open-drain/open-collector budič („It is assumed that the digital buffer driving RC in 3.3V designs is open collector or open drain“) a varuje před zkratovým proudem. TX z ESP32-S3 je push-pull, takže v praxi stačí přímé připojení, nebo dej budič typu 74LVC1G07.
- MIDI IN: 220 Ω v sérii s LED optočlenu zůstává beze změny (Arduino forum, PRAVDĚPODOBNÉ), plus 1N4148 antiparalelně. **H11L1 napájený z 3,3 V** s pull-upem ~1–4,7 kΩ na 3,3 V. Datasheet onsemi H11L1M uvádí „VCC Operating Voltage Range … 3 · 15 · V“, takže provoz na 3,3 V je ve specifikaci (OVĚŘENO). 6N138 má podle datasheetu Broadcom AV02-1359EN doporučené minimum „Power Supply Voltage VCC 4.5“ V, takže při 3,3 V je mimo specifikaci. Lze také přendat původní MIDI desku s H11L1 a napájet ji 3,3 V.

**D6. Mechanika.** Vnější rozměry jsou 60 × 221 × 687 mm (Behringer). Na zadním panelu je IEC zásuvka s pojistkou, vypínač, SWITCH 1/2, MIDI IN a MIDI OUT/THRU (musiker-board, přehled). **Rozměry hlavní desky, otvory ani rozměry výřezů publikované nejsou (NEOVĚŘENO).** Pro USB-C použít **otvor po IEC zásuvce** (největší) se záslepkou z hliníku nebo 3D tisku a panelovým USB-C (C–C prodloužení s maticí). Otvor po vypínači může nést tlačítko BOOT/RESET.

### E. Mackie Control pro Logic Pro

**Čísla not – všech 12 hodnot z firmwaru sedí** (libMackieControl, „similar to that used by Logic“, https://github.com/Do-sth-sharp/libMackieControl/blob/main/doc/MackieControl.md; TouchMCU, https://github.com/NicoG60/TouchMCU/blob/main/doc/mackie_control_protocol.md):

| Funkce | Firmware | Zdroj | Stav |
|---|---|---|---|
| Save | 80 | 80 UTILITIES: SAVE | OVĚŘENO |
| Undo | 81 | 81 | OVĚŘENO |
| Marker | 84 | 84 | OVĚŘENO |
| Cycle | 86 | 86 (D6, 0x56) | OVĚŘENO |
| Drop | 87 | 87 | OVĚŘENO |
| Replace | 88 | 88 | OVĚŘENO |
| Click | 89 | 89 | OVĚŘENO |
| Rewind | 91 | 91 | OVĚŘENO |
| Fast Fwd | 92 | 92 | OVĚŘENO |
| Stop | 93 | 93 | OVĚŘENO |
| Play | 94 | 94 (A#6, 0x5E) | OVĚŘENO |
| Record | 95 | 95 (B6, 0x5F) | OVĚŘENO |

- **Tlačítka:** stisk = Note On s velocity 127, uvolnění = velocity 0, vše na MIDI kanálu 1. **LED zpětná vazba** od Logicu: velocity 0 = vypnuto, 1 = bliká, 127 = svítí. OVĚŘENO (libMackieControl, TouchMCU). Pozor na posun oktáv: Logic může 94 zobrazovat jako A#5 nebo A#6 podle konvence (logicprohelp).
- **Master fader:** pitch bend na **kanálu 9** (kanály 1–8 jsou stripy). **Fader touch:** noty 104–111 (stripy), **112 = master**. OVĚŘENO. Před posíláním pitch bendu pošli touch 127 a po skončení touch 0.
- **Transportní sekce** podle Apple: „seven small, circular buttons… Marker, Nudge, Cycle, Drop, Replace, Click, and Solo“ (Apple Control Surfaces Support guide, https://help.apple.com/pdf/logicpromac-css/en_US/logic-pro-mac-control-surfaces-support-guide.pdf). OVĚŘENO.
- **Handshake:** SysEx hlavička `F0 00 00 66 14 …`. Host pošle Device Query (`00`), zařízení odpoví Host Connection Query (`01` + 7 B sériové číslo + 4 B challenge), host odpoví `02` a zařízení potvrdí `03` (TouchMCU, OVĚŘENO jako reverse-engineering na originálním MCU). Že Logic **automaticky skenuje** MIDI porty Device Query a přidá zařízení, které odpoví, potvrzuje https://github.com/rosasynthesiz/logic-pro-mcp („Logic auto-scans new MIDI ports with Mackie Control device queries, we answer the handshake“). Ruční přidání (Setup → New → Install → Mackie Control → nastavit oba porty) popisuje Apple a zkouška z 2026 hlásí, že to fungovalo (https://github.com/ambiguouscherry/sharpfive/issues/5). Že Logic **trvale** akceptuje zařízení, které na handshake nikdy neodpoví, primární zdroj výslovně netvrdí: **PRAVDĚPODOBNÉ, ne OVĚŘENO**. Doporučení: implementuj odpověď na `00` (pošli `01` s libovolným sériovým číslem) a na `02` (pošli `03`).

## Checklist na středu (seřazeno podle toho, jak moc blokuje návrh PCB)

1. **Konektory předních desek:** vyfoť zblízka s měřítkem. Posuvkou změř vzdálenost osy pinu 1 a pinu 14 (33,02 / 32,5 / 26 mm) a průměr nebo čtverec kolíku. Zjisti, zda je na desce kolíková lišta nebo zásuvka, jestli má zámek nebo klíč, výšku a výrobce (nápis na pouzdře, např. „JST“, „Molex“).
2. **Ověř pinout podle tabulky B2** multimetrem v režimu diody: pin 1 je červený, anody LED, katody, společný „−“ tlačítek a horní pin 14 nezapojený. Totéž ověř pro diody u tlačítek a jejich orientaci.
3. **Rezistory LED:** změř odpor mezi pinem anody a anodou LED přímo na přední desce (0 Ω znamená, že rezistor je na hlavní desce). Zjisti barvu a průměr LED (3 nebo 5 mm).
4. **Konektory pedálů:** rozteč, počet pinů, barvy vodičů. Za chodu originálu (opatrně, síť!) změř na signálovém vodiči napětí v poloze heel a toe proti GND a napájení senzoru.
5. **Ostatní konektory hlavní desky** (MIDI deska, SWITCH deska, transformátor, displej): rozteč, počet pinů, pinout (MIDI: které piny vedou na H11L1 a které na OUT).
6. **Obrys hlavní desky a 3 + 1 montážní otvory:** vyfoť kolmo s pravítkem v rovině desky, změř souřadnice otvorů od dvou hran a průměr otvorů. Zjisti výšku distančních sloupků a polohu chladiče ke krytu.
7. **Zadní panel:** rozměry výřezu IEC (s pojistkou), vypínače, MIDI a jacků, a tloušťku plechu (kvůli USB-C záslepce).
8. **Identifikace revize:** štítek EPROM IC13, silkscreen a číslo DPS, datové kódy IC, typ transformátoru. Pokud displej při zapnutí ukáže verzi, zapiš ji.
9. **Displej:** jak je připojený (napevno na hlavní desce, nebo na samostatné desce) a zda ho chceš zachovat. Pokud ano, zaznamenej pinout LDD5125/SD5685.

## Výhrady
- Jediný publikovaný pinout předních desek pochází z jednoho kusu (Fractal fórum, cca 2010) a autor ho necituje ze schématu. Je ale nejbližší stáří tvého kusu.
- Výpočty děliče, úbytku na diodě a počtu GPIO jsou inženýrské odvození, ne citace. Datasheetové hodnoty (pull-up 45 kΩ a VIL ESP32-S3, VCC H11L1, VCC 6N138, rozsah ADC) jsou z katalogových listů Espressif, onsemi a Broadcom.
- Originální schéma FCB1010 veřejně dostupné není. Autor Practical Usage ho má a poskytl ho jen e-mailem.
