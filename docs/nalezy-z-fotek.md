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
- 3× 74HC273D (jeden z nich IC3), 74HC373, SRAM GoldStar GM76C256, EPROM v pouzdře DIP-28.
- 2× relé Bestar BT-5S, cívka 5 V (K1, K2). To jsou původní spínací výstupy na zadní jacky.
- Stabilizátor v pouzdře TO-220 (potisk KIA …05A, tedy 7805), usměrňovací diody D16 až D19, dva elektrolyty.
- Displej a stavové LED jsou na straně spojů a koukají tónovaným okénkem v horním panelu:
  - sedmisegmentový displej: znak ±1 a dvoumístný modul E1-2056AUR1 (výška číslic 0,56"),
  - 2 červené a 9 zelených obdélníkových LED ve dvou černých držácích.
- Všechno to zmizí spolu s deskou, jak předpokládal návrh.
- Rozměr desky asi 23 až 23,5 × 4 cm (odečteno z přiloženého metru na IMG_9172, IMG_9206 a IMG_9208; část přes lupu, takže přesnost zhruba ±5 mm). Přesně až posuvkou na vyndané desce.
- Rozmístění podél desky podle metru: červené LED 1,5 až 3 cm, první držák zelených LED 4 až 10,5 cm, druhý 11,7 až 17 cm, displej 18,3 až 22 cm.
- Vedle LED a displeje je na desce řada tranzistorů T1 až T18 s odpory (spínání číslic, segmentů a LED).

### Okénko v horním panelu

- Zvenku je to černý potištěný pás dlouhý asi 23 cm s popisky (SWITCH 1, SWITCH 2, SELECT, NUMBER, VALUE 1, VALUE 2, DIRECT SELECT, MIDI FUNCTION, MIDI CHAN., CONFIG). Pro každou LED je v něm jen malé průhledné okénko.
- Pro displej je v pásu **červený filtr široký asi 38 mm** (z metru přiloženého zevnitř, IMG_9215). Výšku ze šikmých fotek určit nejde, podle původního displeje (číslice 0,56") bude kolem 15 až 20 mm, **nutno změřit pravítkem zvenku**.
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
| X18 (potisk „4P“) | 4 | **skutečná kolíková lišta v plastovém límci, rozpojitelná**; na IMG_9211 a IMG_9203 je prázdná, kam vedla zástrčka, je potřeba potvrdit | vidět |
| X17, u EPROM a usměrňovače | 3 až 4 | bílý konektor s vodiči k zadním destičkám (MIDI X7 nebo jacky), přes toroid | odhad |
| pájecí body u D16 až D19 | 2 | sekundár transformátoru, žlutá kroucená dvojlinka | vidět |

**Na hlavní desce to nejsou rozpojitelné konektory.** Ověřeno nadzvednutím jednoho 3pinového (IMG_9199): vodiče mají nalisované kontakty, jejichž konce jsou zapájené přímo do desky, a bílý plastový díl je jen držák nasunutý na kontakty (provedení „board-in“). Svazek se od hlavní desky dá oddělit jen odpájením, nebo odstřižením. Na přední desce (X8, potisk „14P“, IMG_9183) je bílý díl stejného typu, takže svazek je nejspíš zapájený i tam. U destiček senzorů, MIDI a jacků to ověřeno není.

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
- Odpovídá to návrhu: H11L1 zůstane na původní destičce, k nové desce půjdou 4 vodiče (nejspíš napájení, zem, výstup optočlenu a MIDI OUT; přiřazení je potřeba změřit).

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
2. **Nová deska na místě původní.** Hlavní deska je přišroubovaná pod horním panelem. Nosná deska může převzít její obrys (asi 23 × 4 cm) a upevňovací otvory. Chybí přesné rozměry a poloha otvorů.
3. **Displej, dvě cesty.** Rozhodnutí až po změření okénka, **do té doby OLED neobjednávat**:
   - (a) panel beze změny: menší OLED, který se vejde za červený filtr. Kandidát je 1,54" 128×64 SSD1309 I2C (aktivní plocha asi 35 × 17,5 mm, deska modulu 42,4 × 38 mm, stejný řadič jako 2,42", takže firmware se nemění). Šířkou se do 38 mm vejde, výška závisí na změření okénka. Nejistota: jak čitelný bude přes červený filtr. Bílý nebo žlutý OLED bude přes filtr svítit červeně, modrý by vidět nebyl. Stávající okénka LED s popisky jdou využít pro stavové LED na nové desce.
   - (b) nový pás z kouřového plexi místo původního potištěného a za něj OLED 2,42". Zmizí původní popisky.
4. **LED nad pedály** (X13, X14): dva další výstupy na MCP23017 (celkem 12 ze 16).
5. **Relé K1, K2.** Potvrzují, že spínací výstupy na zadních jackách jsou galvanicky oddělené kontakty. PhotoMOS AQY212EH je nahradí.
6. **Síťová část** (zásuvka, vypínač, transformátor) se při napájení z USB-C odpojí.

## Co ještě změřit

1. Jestli jsou svazky zapájené i na straně předních desek a senzorů. (Rozteč 14pinových svazků je potvrzená, 2,0 mm.)
   Změřit rozteč u 2pinových (X13, X14), 3pinových (X21, X22) a u lišty X18. U 3pinových vychází z fotky stejná jako u 14pinových.
2. Průchodnost pinů předních desek podle `mereni.md`, část 3.
3. Přesné rozměry hlavní desky a polohu upevňovacích otvorů (vyndaná deska na čtverečkovaném papíře, focená kolmo shora). Výšku červeného okénka displeje (pravítkem zvenku) a jestli jde pás z panelu vyndat.
4. Kam vede zástrčka z X18 a kam svazek z X17; přiřazení 4 vodičů destičky MIDI (X7).
5. Průměr LED a rozteč spínačů.
