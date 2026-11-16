# FCB1010-S3: koncepce a specifikace (verze 2)

Stav k 16. 11. 2026. Nahrazuje původní zadání „jen ovladač pro DAW“. Nově: plnohodnotné 5pinové MIDI a profil pro Boss GX-700.

## Co má přístroj umět

Tři role v jedné krabici, přepínané profilem:

1. **Ovladač DAW přes USB.** Logic Pro: transport, undo, cycle, metronom, pedály na hlasitost a parametry.
2. **Samostatný nožní MIDI ovladač přes 5pinové MIDI.** Hlavně pro Boss GX-700: volba patchů, pedály. Bez počítače, napájení z libovolné USB nabíječky nebo powerbanky.
3. **MIDI rozhraní USB ↔ DIN.** Mac přes FCB vidí GX-700. Apollo Twin X MIDI porty nemá, takže tudy půjde záloha a nahrání patchů (bulk dump/load) a ovládání GX-700 z Logicu.

NUX MG-30 se ovládat dá, ale ne přes USB port FCB zároveň s Macem. Možnosti jsou v kapitole „Ovládání více přístrojů najednou“.

## Profily

Profil říká, co pošle každý spínač a pedál, kam (USB, DIN, obojí) a jak se chovají LED a displej. Přepnutí profilu: podržet UP + DOWN, vybrat pedálem, displej ukáže název. Poslední profil, banka a patch se pamatují.

### Profil 1: Logic CC (USB)

Momentové CC 20–31 pro Learn v Logicu, pedály CC 85/86. Hotové ve firmwaru 0.1.

### Profil 2: Mackie Control (USB)

Noty Mackie Control, LED ukazují stav Record/Play/Cycle z Logicu, displej stav transportu. Funguje i v LUNA. Chybí handshake a fader touch.

### Profil 3: GX-700 (DIN)

Co o GX-700 víme:

- 200 pamětí: 100 uživatelských a 100 presetových. Konektory MIDI IN, OUT, THRU.
- Patche se volí zprávou Program Change, převod čísel na patche určuje Program Change Map. Patche od čísla 129 výš jsou dosažitelné jen přes mapu.
- Parametry se ovládají zprávami Control Change podle nastavení Control Assign v každém patchi. Manuál jako zdroj uvádí CC 80 (CTL pedál FC-200, např. tuner v režimu TOGGLE) a CC 7 (EXP pedál FC-200, např. výstupní úroveň).
- Výchozí Program Change Map, rozsah použitelných CC a počet přiřazení na patch **nejsou ověřené**; manuál se nepodařilo přečíst celý. Ověří se na přístroji.

Návrh rozložení (stejná logika jako původní FCB, 10 bank × 10 patchů = 100 uživatelských patchů):

| Ovladač | Funkce |
|---|---|
| Pedály 1–10 | Program Change: patch (banka × 10 + pedál) |
| UP / DOWN | banka +1 / −1; patch se pošle až po šlápnutí na pedál |
| Expression A | CC 7 (hlasitost) |
| Expression B | CC 1 (wah nebo co si v patchi přiřadíš) |
| LED 1–10 | svítí aktuální patch |
| Displej | číslo patche 001–100, při listování bankou bliká |
| Dlouhý stisk UP | přepnutí na vrstvu efektů (fáze 2) |

Vrstva efektů (fáze 2): pedály posílají CC s přepínáním stavu a LED ukazují zapnuto/vypnuto. Vyžaduje Control Assign v každém patchi GX-700, takže má smysl jen pro pár efektů (tuner, sólo boost, delay).

Obousměrnost: když změníš patch na panelu GX-700 a jeho MIDI OUT vede do FCB, FCB si číslo převezme a přepne LED a displej. Závisí na tom, jestli GX-700 Program Change vysílá (neověřeno).

### Další profily

Tabulka v kódu, přidání profilu je pár řádků. Kandidáti: obecný Program Change 1–128, TONEX Pedal (má 5pinové MIDI).

## Ovládání více přístrojů najednou

Profil není „jeden přístroj“, ale **sestava**. Firmware zná seznam cílů (přístroj = port + MIDI kanál) a každý spínač může poslat několik zpráv různým cílům. Jeden pedál tak přepne patch na GX-700 a zároveň něco na MG-30. Původní FCB to uměl stejně: až 5 Program Change a 2 CC na preset.

| Cíl | Port | Kanál |
|---|---|---|
| Logic | USB | 1 |
| GX-700 | DIN OUT | 1 |
| MG-30 | podle zvolené cesty níže | 2 |
| MG-30 přes jack | kontakty na zadních jackách | – |

Co jde současně:

| Kombinace | Jde? |
|---|---|
| Mac (USB) + GX-700 (DIN) | ano |
| Mac + GX-700 + MG-30 přes jack TRS | ano |
| Mac + GX-700 + MG-30 přes externí USB host adaptér na DIN | ano |
| Mac + MG-30 přes USB host vestavěný ve FCB | ne, jeden USB port má jen jednu roli |
| GX-700 + MG-30 přes vestavěný USB host (bez Macu) | ano, ale FCB potřebuje zvlášť napájení |

GX-700 a MG-30 se tedy navzájem nevylučují. Vylučuje se jen Mac a MG-30 na jediném USB portu FCB.

### Tři cesty k MG-30

**A. Jack TRS do EXP1 na MG-30 (doporučený začátek).** FCB se tváří jako dvojitý spínač NMP-2: dva kontakty, hrot a kroužek proti objímce. Původní FCB má přesně na tohle dvě relé a dva zadní jacky.

- Výhody: žádný protokol, funguje vždy a souběžně s Macem i GX-700, téměř zadarmo.
- Omezení: jen dvě funkce, které MG-30 dovolí přiřadit na NMP-2 (zapínání bloků). Žádná volba patche číslem, žádná zpětná vazba. Jack EXP1 je buď pro NMP-2, nebo pro expression pedál, ne obojí.
- Kontakty musí být plovoucí (relé nebo PhotoMOS), objímka jacku se nesmí spojit se zemí FCB. Jinak vznikne zemní smyčka mezi USB zemí Macu a audio zemí MG-30.
- Kabel: 2× mono jack → 1× stereo jack, nebo jeden stereo jack zapojený na oba kontakty.

**B. Externí adaptér DIN → USB host („redukce“).** Zapojení: FCB DIN OUT → GX-700 IN, GX-700 THRU → adaptér → USB-C na MG-30. Oba přístroje visí na jedné lince, každý na svém kanálu.

- Výhody: plné MIDI (patche, CC), souběžně s Macem, ve firmwaru FCB žádná práce navíc.
- Nevýhody: cena (Kenton MIDI USB Host mk3 kolem 90 £, levnější DOREMiDi UMH-20), další krabička a zdroj. USB port MG-30 je pak obsazený, takže MG-30 nemůže být zároveň zvukovka nebo připojený k editoru QuickTone.
- Riziko: adaptéry chtějí zařízení class compliant. Jestli MG-30 s takovým hostitelem spolehlivě funguje a které zprávy přijímá, není ověřené. U příbuzného MG-300 fungovalo ovládání z USB hosta na Teensy; jeden uživatel s Arduinem přes OTG redukci u MG-30 neuspěl.

**C. USB host vestavěný ve FCB.** Druhý USB konektor na FCB, ESP32-S3 v roli hostitele.

- Výhody: žádná krabička navíc.
- Nevýhody: nejde zároveň s Macem, FCB potřebuje samostatné napájení, do firmwaru přibude USB host s ovladačem MIDI. Nejvíc práce a nejvíc neznámých.
- Na desce verze 1 se s tím nepočítá. Signály USB (GPIO19/20) jsou na liště DevKitu, takže to jde později doplnit malou přídavnou destičkou.

Postup: nejdřív A. Před případnou koupí adaptéru (B) vyzkoušet, na jaké zprávy MG-30 reaguje, když je připojený k Macu a pošle se mu Program Change a CC. Teprve pak má smysl psát profil.

## Směrování MIDI

| Odkud | Kam | Kdy |
|---|---|---|
| spínače, pedály | USB | profily 1 a 2 |
| spínače, pedály | DIN OUT | profil 3 |
| USB | DIN OUT | režim rozhraní (zapnutelný) |
| DIN IN | USB | režim rozhraní |
| DIN IN | LED, displej | profil 3 (synchronizace patche) |

Pravidla:

- SysEx se nesmí přerušit vloženou zprávou. Vlastní události počkají ve frontě, dokud průchozí SysEx neskončí.
- Jádro arduino-esp32 dává jen jeden USB MIDI port. V profilu Mackie Control by se přes něj do GX-700 dostávaly zprávy pro Logic, proto je průchod USB → DIN v tomto profilu vypnutý.
- Cíl je mít dva USB porty („FCB1010 ovladač“ a „FCB1010 DIN“) vlastním USB deskriptorem. Neověřeno, zkusí se při implementaci.

## Ovládání samotného přístroje

| Akce | Jak |
|---|---|
| Přepnutí profilu | podržet UP + DOWN 1 s, pak pedál 1–10 |
| Kalibrace pedálů | v menu profilu pedál 10, displej vede krok po kroku |
| Aktualizace firmwaru | kombinace pedálů přepne do zavaděče, nahrává se přes zadní USB-C bez otevírání; záloha jsou tlačítka BOOT a RESET na zadním panelu |
| Jas LED a displeje | v nastavení |

Dlouhý stisk: spínač, který má i funkci na dlouhý stisk, pošle krátkou funkci až při puštění. Proto dlouhé stisky jen na UP/DOWN, ne na pedálech pro patche a transport.

## Hardware: co se mění proti první verzi

- **5pinové MIDI je povinné.** Použije se původní destička MIDI s H11L1 a zásuvkami, které sedí v zadním panelu.
- **74AHCT125 je povinný.** Jedno hradlo budí MIDI OUT na 5 V (odpory 2× 220 Ω podle normy), druhé data pro WS2812B.
- **Displej je potřeba**, kvůli číslu patche. OLED 2,42" (SSD1309) na I2C ve zvětšeném výřezu panelu; úpravy skříně jsou možné. Totéž platí pro čistý výřez na USB-C vzadu.
- **LED: základ jsou původní červené** přes MCP23017. Na ukázání aktuálního patche stačí a nevyžadují žádnou mechanickou práci. WS2812B zůstává jako volitelný konektor.
- **Zadní jacky Switch 1/2:** deska bude umět obojí. Buď dva plovoucí spínací výstupy (PhotoMOS, pro MG-30 místo NMP-2 nebo pro kanály zesilovače), nebo dva pomocné vstupy AUX (externí spínač, expression pedál). Volí se zapojením kabelu od jacků.
- **Kostra** se spojí s GND desky v jednom bodě. Po odstranění síťové části už není uzemněná přes přívod.
- **Zemní smyčka** při současném zapojení do Macu a do GX-700 nehrozí: vstup MIDI na straně GX-700 je oddělený optočlenem.

## Stavba firmwaru

| Modul | Úkol |
|---|---|
| `inputs` | spínače (debounce, krátký a dlouhý stisk), pedály (filtr, kalibrace), AUX |
| `midi_usb`, `midi_din` | odesílání a příjem, parser včetně SysEx a running status |
| `router` | směrování a fronta kolem SysEx |
| `profiles` | tabulky profilů, stav (banka, patch, přepínače) |
| `leds` | společné rozhraní, ovladače MCP23017 a WS2812B |
| `display` | OLED: profil, patch, hodnoty, menu |
| `settings` | NVS: profil, kalibrace, jas |

Logika profilů a směrování půjde testovat na počítači bez hardwaru (PlatformIO `native`). Konfigurace profilů je zatím v kódu; editor přes web nebo USB až bude potřeba.

## Postup

1. **Středa 18. 11.:** otevřít, vyfotit, změřit (checklist v `navrh.md`). Nově i destičku MIDI: kde jsou odpory 220 Ω a pull-up optočlenu a jak je připojená.
2. **Zkouška na drátech:** přední desky, pedály a MIDI destičku připojit k DevKitu propojkami a ověřit pinouty firmwarem. Teprve potom objednat desku.
3. **Firmware 0.2:** moduly podle tabulky, profily 1 a 3, DIN MIDI, původní LED, OLED.
4. **Schéma a deska** v KiCadu, výroba.
5. **Firmware 0.3:** Mackie Control s handshake, režim rozhraní se dvěma USB porty, aktualizace přes USB.

## Rizika a neověřené věci

| Věc | Dopad | Kdy se vyjasní |
|---|---|---|
| Typ a rozteč konektorů | blokuje desku | středa |
| Pinout předních desek z cizího kusu | špatné zapojení | středa, zkouška na drátech |
| Zapojení destičky MIDI | volba napájení a odporů | středa |
| Výchozí Program Change Map GX-700 | čísla patchů | zkouška s GX-700 |
| Dva USB MIDI porty na ESP32-S3 | pohodlí v Logicu | firmware 0.3 |
| Co MG-30 přijímá přes USB MIDI a jestli funguje s USB host adaptérem | cesta B k MG-30 | zkouška s MG-30 u Macu |
| Které funkce jdou v MG-30 přiřadit na NMP-2 | užitečnost cesty A | zkouška s MG-30 |
| Místo na panelu pro výřez 2,42" displeje | velikost displeje | středa |
| Firmware neběžel na hardwaru | chyby při oživení | až dorazí DevKit |
