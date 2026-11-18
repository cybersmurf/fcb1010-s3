# FCB1010-S3: nálezy z otevřeného přístroje (18. 11. 2026)

Zdroj: fotky přístroje zvenku i otevřeného (IMG_9137 až IMG_9199). Nic z toho zatím není měřené multimetrem. U každého bodu je uvedeno, jestli je to **vidět** (jisté), **odhad z fotky**, nebo **neověřeno**.

## Identifikace přístroje

| Co | Nález | Jistota |
|---|---|---|
| Hlavní deska | potisk „CONTROLLER & DISPLAY“, BEHRINGER MODEL FCB1010/01, kód desky končí REVG (revize G), výrobce desky BYJ, kód 0920, DE005755, RoHS | vidět |
| Spodní deska spínačů | „LOWER STEP PCB“, BEHRINGER MODEL FCB1010/03, BYJ 0918 | vidět |
| Destičky senzorů pedálů | označení X10 a X11, BYJ-3 E230225, kódy 0822 a zřejmě 0845 | vidět |
| Firmware | štítek na EPROM „FCB1010 V2.501E“, tedy 2.5.1E | vidět |
| Destička MIDI | BEHRINGER MODEL FCB1010/04, kód desky končí REVG | vidět |
| Štítek na zadním panelu | Date Code 0906, 230 V~ 50/60 Hz, 10 W, pojistka T 50 mA L 250 V, RoHS | vidět |
| Stáří | Date Code 0906 a kódy desek 0918, 0920 ukazují na výrobu v roce 2009 | odhad |

Závěr: nejde o ranou revizi. Je to pozdní provedení s modrými deskami, SMD osazením a firmwarem 2.5.1E.

## Hlavní deska

- CPU Philips P80C32SBAA (PLCC-44), krystal Q1 12 MHz.
- 3× 74HC273D (IC3, IC10, IC11), 74HC373 (IC9), SRAM GoldStar GM76C256ALFW70 (IC14), EPROM v patici DIP-28 (IC13), IC4 MM74HC04M, IC5 74HC138, dále IC6, IC7 (SO-8) a IC12 (typy z fotek nečitelné). Usměrňovač tvoří čtyři diody řady 1N400x.
- Tranzistory T5 až T18 v pouzdře SOT-23 s potiskem A06 a A56 (spínání číslic, segmentů a LED), odpory R28 až R35 po 33 Ω.
- 2× relé Bestar BT-5S, cívka 5 V (K1, K2). To jsou původní spínací výstupy na zadní jacky.
- Stabilizátor v pouzdře TO-220 (KIA 7805A), usměrňovací diody D16 až D19, dva elektrolyty.
- Displej a stavové LED jsou na straně spojů a koukají tónovaným okénkem v horním panelu:
  - sedmisegmentový displej: znak ±1 a dvoumístný modul E1-2056AUR1 (výška číslic 0,56"),
  - 2 červené a 9 zelených obdélníkových LED ve dvou černých držácích.
- Všechno to zmizí spolu s deskou, jak předpokládal návrh.
- Rozměr desky **229 × 41 mm, změřeno majitelem**. Odhad z fotek na čtverečkovaném papíře (IMG_9259, IMG_9266) vyšel na 220 × 41 mm, tedy o 4 % kratší: deska leží na součástkách asi 1,5 cm nad papírem, fotky jsou pořízené zblízka širokoúhlým objektivem a měřítko se po délce desky mění. Polohy odečtené z těchto fotek jsou proto jen orientační.
- Upevnění a otvory, odečteno z fotek s metrem položeným na desce (IMG_9276 až IMG_9287). Polohy jsou od krátké hrany na konci u displeje (konec s X13 a X14), měřeno na straně součástek:

  | Prvek | Od krátké hrany | Poznámka | Nejistota |
  |---|---|---|---|
  | úhelník 1 (střed) | 4,3 mm | nožky zapájené v 1,6 a 7,1 mm | ±0,5 mm |
  | kulatý otvor A, ⌀ asi 2,2 mm | 9,6 mm | 2,6 mm od dlouhé hrany s úhelníky | ±0,5 mm |
  | kulatý otvor B, ⌀ asi 2,2 mm | asi 2 mm | asi 5,5 mm od dlouhé hrany se svazky | ±1 mm |
  | úhelník 2 (střed) | 116,5 mm | z fotek s metrem přiloženým od hrany u displeje (IMG_9311 až IMG_9325) vychází 115 až 118,5 mm | ±2,5 mm |
  | úhelník 3 (střed) | 211,5 mm | 17 až 18 mm od opačné krátké hrany; vývody 7805 jsou o 10 mm dál | ±1,5 mm |

  - Všechny tři úhelníky jsou u dlouhé hrany protilehlé ke svazkům, šrouby zajištěné červeným lakem. Rozteč nožek úhelníku je asi 5,5 až 6 mm.
  - Stabilizátor 7805 (IC2) sedí v rohu u úhelníku 3, je ohnutý přes okraj desky a přišroubovaný ke kostře jako k chladiči.
  - Kontrola: metr na těchto fotkách ukazuje konce desky na 37,4 a 59,7 cm, tedy jen 223 mm. Na konci u relé ale metr leží asi 1 cm nad deskou (na EPROM a kondenzátoru) a fotka je zblízka, takže čtení je tam zkreslené paralaxou. Podle rozteče vývodů 7805 (2,54 mm) vychází měřítko desky v tom místě 0,80 měřítka metru; po opravě je délka 227 až 228 mm, což sedí s naměřenými 229 mm. Úhelník 3 je proto počítaný v měřítku desky, ne přímo z metru.
  - Oprava: dříve uvedených 112 mm u úhelníku 2 bylo špatně, vzniklo odečtením dvou čtení metru ze dvou různých fotek.
  - Přesněji to z fotek nejde: metr leží na součástkách asi 1 cm nad deskou a každá fotka je z jiného úhlu, takže stejný úhelník vychází na různých fotkách o 2 až 3 mm jinde. Rozteč nožek úhelníku vychází na 5 až 6 mm.
  - Rozhodující míra pro novou desku jsou rozteče tří otvorů pro šrouby v horním panelu (plech, dá se změřit přesně) a poloha prvního otvoru vůči oknu displeje. Do té doby počítat s oválnými otvory s vůlí ±3 mm.
- Rozmístění na straně spojů, odečteno z fotek s metrem zaháknutým za krátkou hranu u stabilizátoru (IMG_9289 až IMG_9296). Držáky LED a displej jsou asi 1 cm nad deskou a fotky jsou šikmé, nejistota je zhruba ±2 mm:

  | Prvek | Od hrany u stabilizátoru | Od hrany u displeje |
  |---|---|---|
  | držák se 2 červenými LED | 6,5 až 30 mm | 199 až 222,5 mm |
  | držák s 5 zelenými LED | 33 až 113,5 mm | 115,5 až 196 mm |
  | držák se 4 zelenými LED | 118 až 172,5 mm | 56,5 až 111 mm |
  | displej (modul ±1 a dvoumístný modul) | 182 až 221 mm | 8 až 47 mm |

  - Displej je široký asi 39 mm (moduly asi 13 a 26 mm) a vysoký 19 mm. Jeho střed je asi 27 mm od krátké hrany u displeje a asi 12,5 mm od dlouhé hrany s úhelníky. Tam je tedy i střed červeného okénka v panelu.
  - LED jsou v držácích ob jednu buňku, rozteč LED vychází na 12,5 až 14 mm (nejspíš 12,7 mm).
  - Stejné fotky potvrzují délku desky: s metrem zaháknutým za hranu končí deska na 22,9 cm.
- Vedle LED a displeje je na desce řada tranzistorů T1 až T18 s odpory (spínání číslic, segmentů a LED).

### Okénko v horním panelu

- Zvenku je to černý potištěný pás dlouhý asi 23 cm s popisky (SWITCH 1, SWITCH 2, SELECT, NUMBER, VALUE 1, VALUE 2, DIRECT SELECT, MIDI FUNCTION, MIDI CHAN., CONFIG). Pro každou LED je v něm jen malé průhledné okénko.
- Pro displej je v pásu **červený filtr asi 36 × 18,5 mm** (odečteno z metru přiloženého zvenku na IMG_9237 a IMG_9238, přesnost zhruba ±1 mm; zevnitř vycházela šířka 38 mm). Černý pás je vysoký asi 25 mm. Před objednáním displeje přeměřit posuvkou.
- Okének pro LED je 11 (zevnitř od displeje 4 + 5 + 2), rozteč asi 12 mm, každé zhruba 4 × 1,5 mm.
- Pás je plastový díl vsazený do panelu; v rohu je vidět průhledný plastový čep, takže nejspíš není lepený. Jestli jde vyndat, není ověřeno.
- Držáky LED a displej jsou vysoké asi 10 až 12 mm, tolik je tedy od desky k pásu. Modul OLED musí na nové desce sedět ve stejné výšce.
- OLED 2,42" má aktivní plochu asi 55 × 27,5 mm a za stávající červené okénko se nevejde. Viz dopady na návrh.

### Konektory na hlavní desce (potisk)

| Označení | Pinů | Kam vede | Jistota |
|---|---|---|---|
| X19, X20 (potisk „14P“) | 14 | přední desky spínačů, svazky přes zaklapávací ferit | vidět (IMG_9211, IMG_9201) |
| X21, X22 (potisk „3P“) | 3 | senzory pedálů X10, X11; vodiče červený + 2 černé | vidět (IMG_9211) |
| X13, X14 (potisk „2P“) | 2 | dvě součástky u pedálů zalité tavným lepidlem, vodiče červený + černý | vidět; téměř jistě LED nad pedály (zvenku je u nápisů EXPRESSION PEDAL A a B po jednom okénku) |
| X18 (potisk „4P“) | 4 | destička MIDI (její konektor X7), vodiče červený + 3 černé. **Skutečná kolíková lišta v plastovém límci, rozpojitelná** | potvrzeno majitelem |
| X17 (potisk „4P“), u usměrňovače | 4 | destička zadních jacků (spínací výstupy relé K1, K2). Kolíková lišta v límci jako X18, rozpojitelná (IMG_9222) | potvrzeno majitelem, lišta vidět |
| pájecí body u D16 až D19 | 2 | sekundár transformátoru, žlutá kroucená dvojlinka | vidět |

**Na hlavní desce to nejsou rozpojitelné konektory.** Ověřeno nadzvednutím jednoho 3pinového (IMG_9199): vodiče mají nalisované kontakty, jejichž konce jsou zapájené přímo do desky, a bílý plastový díl je jen držák nasunutý na kontakty (provedení „board-in“). Svazek se od hlavní desky dá oddělit jen odpájením, nebo odstřižením. Výjimka je X18 (MIDI), kde je normální lišta se zástrčkou. Na přední desce (X8, potisk „14P“, IMG_9183) je bílý díl stejného typu, takže svazek je nejspíš zapájený i tam. U destiček senzorů, MIDI a jacků to ověřeno není.

Spoje jsou navíc zajištěné tavným lepidlem (jde dolů po kapce isopropylalkoholu).

## Typ a rozteč konektorů

- Přední desky: **14 pinů v jedné řadě** (14 pájecích plošek, 14 vodičů, z toho jeden červený). Vidět na IMG_9177.
- Rozteč: **2,0 mm, potvrzeno metrem** (IMG_9202): plastový držák 14pinového svazku je dlouhý 29,6 mm a 13 roztečí kontaktů měří asi 25,5 mm. Při rozteči 2,5 mm by držák měl přes 37 mm. Oba 14pinové svazky jsou stejné.
- První odhad z fotky plošek (IMG_9177) dával 1,95 mm: měřítko 23 px/mm podle vývodů mikrospínače a diody, 13 roztečí = 582 px.
- Rozteč 2,0 mm je rozteč otvorů v desce a plastového držáku. Výrobce a řadu z fotek určit nejde.
- 3pinové konektory senzorů mají stejnou rozteč jako 14pinové (porovnání pájecích bodů vedle sebe na IMG_9196).
- Vodiče mají potisk AWM 1007 (UL1007).

**K potvrzení jedním měřením:** vzdálenost středů první a poslední plošky 14pinového konektoru. Při 2,0 mm vyjde 26,0 mm, při 2,5 mm by to bylo 32,5 mm.

## Destička MIDI

- Dvě zásuvky DIN (X1, X2), optočlen H11L1 v pouzdře DIP-6 (IC1), konektor X7 se 4 vodiči k hlavní desce.
- Pájecí bod „TO RELAIS-I/O PCB“ s jedním černým vodičem přes toroid k destičce zadních jacků.
- Na destičce jsou vodiče X7 zapájené; rozpojitelný je až konec na hlavní desce (X18).
- Ze strany spojů (IMG_9222 až IMG_9224, deska BYJ 0918, DE005756) jsou osazené všechny pasivní součástky obou směrů:
  - R5 220 Ω a D13 (1N4148) u vstupu optočlenu, tedy obvod MIDI IN,
  - R6 4,7 kΩ, nejspíš pull-up výstupu H11L1,
  - R7 a R8 po 220 Ω, nejspíš oba odpory MIDI OUT,
  - C1 až C4 po 100 pF u zásuvek.
- Co z toho plyne (zapojení cest je odhad podle součástek a počtu vodičů, **potvrdit průchodností**):
  - Čtyři vodiče jsou nejspíš +5 V, GND, výstup optočlenu (MIDI IN) a vstup pro MIDI OUT.
  - Čtení cest ze zvětšené fotky spojů (IMG_9249), **nízká jistota**: červený vodič (kraj X7 u optočlenu) vede na pin 6 optočlenu (napájení) a na R6, tedy +5 V; vodič hned vedle červeného vede na pin 4 optočlenu (výstup, MIDI IN) a na druhý konec R6. Zbylé dva jsou GND a MIDI OUT, jejich pořadí z fotky určit nejde. Potvrzuje to, že pull-up R6 visí na stejném napájení jako odpory MIDI OUT.
  - Na nové desce **nebudou další odpory 220 Ω** pro MIDI OUT, jen budič na 5 V (74HCT125).
  - Destička se napájí 5 V, protože odpory MIDI OUT jsou počítané na 5 V. Pull-up R6 pak táhne výstup optočlenu k 5 V a ten **nesmí jít přímo na GPIO**. Na nové desce bude dělič: 10 kΩ v sérii a 22 kΩ z pinu na GND. S pull-upem 4,7 kΩ dá 3,0 V v klidu a pod 0,3 V při sepnutém optočlenu.

## Destička zadních jacků (RELAIS-I/O)

- Deska BYJ 0918, DE005757 (IMG_9257, IMG_9258). Dva jacky, konektor se 4 vodiči k X17 na hlavní desce, kondenzátory C5 a C6 po 100 pF.
- Uprostřed je pájecí bod „TO MIDI PCB“ s černým vodičem k bodu „TO RELAIS-I/O PCB“ na destičce MIDI. Na tento bod jsou připojené C5 a C6, je to tedy vztažná zem pro odrušovací kondenzátory.
- **Z fotky nejde rozhodnout**, jestli je tento bod spojený i přímo s objímkami jacků. Od toho závisí, jestli jsou spínací kontakty plovoucí. Rozhodne měření průchodnosti: objímka každého jacku proti černému vodiči a proti kostře.

## Přední desky spínačů

- Na desce je 6 mikrospínačů (podle rozteče vývodů 6 × 6 mm) a u každého skleněná dioda v sérii, D1 až D6. Potvrzuje to průzkum.
- LED jsou červené, kulaté, na dlouhých vývodech ohnutých k hraně desky. Na spodní desce LD3 až LD7, tedy 5 kusů.
- Desku drží distanční sloupky se šrouby a maticemi.
- Délka desky asi 39 cm, rozteč spínačů asi 65 až 70 mm (odhad podle přiloženého metru, **nutno změřit**).
- Ze strany spojů je vidět 14 samostatných cest od konektoru ke spínačům a LED, tedy přímé zapojení bez matice. Přiřazení pinů z fotek určit nejde, je potřeba měření průchodnosti podle `mereni.md`, část 3.

## Pedály

- Každý senzor je malá destička s výřezem, dvěma SMD odpory a 3pinovým konektorem. Tři vodiče jsou potvrzené.
- U každého pedálu je navíc dvouvodičová součástka zalitá lepidlem, připojená na X13 a X14.

## Napájení

- Uvnitř je síťová zásuvka s vypínačem (omotané černou páskou) a transformátor. Sekundár vede žlutou kroucenou dvojlinkou na usměrňovač na hlavní desce.
- Ochranný vodič je na kostře, žlutý vodič propojuje kostru s odnímatelným dnem.

## Dopady na návrh

1. **Svazky jsou do hlavní desky zapájené.** Postup:
   - Svazky od původní hlavní desky **odpájet, ne stříhat**. Zůstanou na nich nalisované kontakty s pájecími konci a dají se znovu použít.
   - Před odpájením si každý svazek označit (který konektor na desce, kde je červený vodič) a vyfotit.
   - Zkouška na drátech: po sundání bílého držáku jsou kontakty volné, každý na svém vodiči. Dají se připájet na obyčejnou kolíkovou lištu 2,54 mm (nebo proužek univerzální desky s lištou) a ta se zasune do nepájivého pole. Rozteč 2,0 mm tedy pro zkoušku nevadí a žádné protikusy se kupovat nemusí.
   - Nová deska, dvě možnosti: (a) otvory s roztečí 2,0 mm a svazky zapájené přímo, stejně jako v originále, bez nových součástek, ale deska nepůjde odpojit; (b) nové rozpojitelné konektory, což znamená nalisovat nové kontakty na zhruba 40 vodičů. Výchozí volba je (a), případně s konektory jen tam, kde to dává smysl.
2. **Nová deska na místě původní.** Hlavní deska je přišroubovaná pod horním panelem. Nosná deska může převzít její obrys (229 × 41 mm) a upevňovací otvory. Chybí přesné rozměry a poloha otvorů.
3. **Displej.** OLED 2,42" byl objednaný 18. 11. 2026 v poledne, dřív než se ukázalo, jak malé je původní okénko. **Platí tedy cesta (b)**; cesta (a) zůstává jako záloha, kdyby úprava panelu nevyšla:
   - (a) panel beze změny: menší OLED, který se vejde za červený filtr. Kandidát je 1,54" 128×64 SSD1309 I2C (aktivní plocha asi 35 × 17,5 mm, deska modulu 42,4 × 38 mm, stejný řadič jako 2,42", takže firmware se nemění). Proti okénku 36 × 18,5 mm zbývá jen asi 0,5 mm na každé straně, což je v rámci chyby odečtu, proto přeměřit posuvkou. Displej musí sedět těsně za filtrem (modul na dutinkové liště vychází zhruba na potřebných 10 až 12 mm), jinak při pohledu šikmo okraj okénka zakryje krajní řádky. Záložní volba je 1,3" (obraz asi 29,5 × 14,7 mm, řadič SH1106). Nejistota: jak čitelný bude bílý OLED přes červený filtr. Bílý nebo žlutý OLED bude přes filtr svítit červeně, modrý by vidět nebyl. Stávající okénka LED s popisky jdou využít pro stavové LED na nové desce.
   - (b) nový pás z kouřového plexi místo původního potištěného a za něj OLED 2,42". Zmizí původní popisky. Obraz displeje je 55 × 27,5 mm, pás je vysoký asi 25 mm: buď se otvor v plechu o pár milimetrů zvětší, nebo firmware nechá nahoře a dole 3 řádky pixelů nevyužité (krok pixelu 0,43 mm). K tomu chybí: jestli jde pás vyndat, výška otvoru v plechu pod ním a hloubka místa za ním. Pozor na umístění: střed původního okénka je jen 27 mm od konce desky a 12,5 mm od hrany s úhelníky, kdežto obraz OLED 2,42" je 55 × 27,5 mm a jeho modul je větší než šířka desky (41 mm). Vystředěný na původní okénko by modul přesahoval přes dlouhou hranu desky a seděl nad úhelníkem 1. Displej se proto buď posune směrem ke středu desky (pokud je otvor v plechu pod pásem souvislý), nebo se přichytí k panelu a s deskou spojí kablíkem.
4. **LED nad pedály** (X13, X14): dva další výstupy na MCP23017 (celkem 12 ze 16).
5. **Relé K1, K2.** Potvrzují, že spínací výstupy na zadních jackách jsou galvanicky oddělené kontakty. PhotoMOS AQY212EH je nahradí.
6. **Síťová část** (zásuvka, vypínač, transformátor) se při napájení z USB-C odpojí.

## Co ještě změřit

1. Jestli jsou svazky zapájené i na straně předních desek a senzorů. (Rozteč 14pinových svazků je potvrzená, 2,0 mm.)
   Změřit rozteč u 2pinových (X13, X14), 3pinových (X21, X22) a u lišty X18. U 3pinových vychází z fotky stejná jako u 14pinových.
2. Průchodnost pinů předních desek podle `mereni.md`, část 3.
3. Rozteče tří otvorů pro šrouby hlavní desky v horním panelu a rozteč nožek úhelníku (z fotek jsou polohy úhelníků jen s nejistotou 0,5 až 2,5 mm, viz tabulka u hlavní desky). Červené okénko displeje posuvkou (zatím 36 × 18,5 mm z fotky) a jestli jde pás z panelu vyndat.
4. Přiřazení 4 vodičů MIDI průchodností: který pin X18 vede na pin 6 (napájení), 5 (GND) a 4 (výstup) optočlenu H11L1 a který přes R7/R8 k zásuvce OUT. Přiřazení 4 vodičů X17 k jackům a kam vede vodič „TO RELAIS-I/O PCB“ (jestli spojuje objímky jacků se zemí).
5. Průměr LED a rozteč spínačů.

## Zdroje k displeji 1,54"

- [universal-solder: 1.54 inch OLED 128x64 I2C (white) SSD1309](https://www.universal-solder.ca/product/1-54-inch-oled-128x64-i2c-white-ssd1309/): deska 42,4 × 38 mm, plocha obrazu asi 35 × 17,5 mm, adresa 0x3C/0x3D.
- [GM electronic: OLED displej 1,54" 128x64, I2C, bílý, kód 775-214](https://www.gme.cz/v/1508852/oled-displej-154128x64-i2c-biely): 259 Kč, 18. 11. 2026 není skladem.
- [Drátek: SPI OLED 1,54" 128x64 bílý](https://dratek.cz/ukonceno/3203-spi-oled-lcd-1-54-displej-128x64-bily-3-3-5v.html): prodej ukončen, verze SPI.
