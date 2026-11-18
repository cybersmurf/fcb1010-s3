# FCB1010-S3: nálezy z otevřeného přístroje (18. 11. 2026)

Zdroj: 20 fotek otevřeného přístroje (IMG_9150 až IMG_9199). Nic z toho zatím není měřené multimetrem. U každého bodu je uvedeno, jestli je to **vidět** (jisté), **odhad z fotky**, nebo **neověřeno**.

## Identifikace přístroje

| Co | Nález | Jistota |
|---|---|---|
| Hlavní deska | potisk „CONTROLLER & DISPLAY“, BEHRINGER MODEL FCB1010/01, kód desky končí REVG (revize G), výrobce desky BYJ, kód 0920, DE005755, RoHS | vidět |
| Spodní deska spínačů | „LOWER STEP PCB“, BEHRINGER MODEL FCB1010/03, BYJ 0918 | vidět |
| Destičky senzorů pedálů | označení X10 a X11, BYJ-3 E230225, kódy 0822 a zřejmě 0845 | vidět |
| Firmware | štítek na EPROM „FCB1010 V2.501E“, tedy 2.5.1E | vidět |
| Stáří | kódy 0918, 0920, 0822 vypadají na rok a týden výroby desek (2008 až 2009) | odhad |

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
- Rozměr desky zhruba 21 × 3,5 cm. Je to hrubý odhad podle šířky displeje, **nutno změřit**.

### Konektory na hlavní desce (potisk)

| Označení | Pinů | Kam vede | Jistota |
|---|---|---|---|
| bez čitelného označení, 2 ks | 14 | přední desky spínačů, svazky přes zaklapávací ferit | vidět |
| X20, X21 (potisk „3P“) | 3 | senzory pedálů X10, X11; vodiče červený + 2 černé | vidět (čísla X20/X21 částečně čitelná) |
| X13, X14 (potisk „2P“) | 2 | dvě součástky u pedálů zalité tavným lepidlem, vodiče červený + černý | vidět; účel neověřen, nejspíš LED u pedálů |
| „4P“ | 4 | destička se zásuvkami MIDI, přes ferit | vidět |
| další bílý konektor u EPROM | 3 až 4 | destička zadních jacků, přes toroid | odhad |
| pájecí body u D16 až D19 | 2 | sekundár transformátoru, žlutá kroucená dvojlinka | vidět |

Konektory jsou zajištěné tavným lepidlem. Před rozpojením ho je potřeba odstranit (jde to po kapce isopropylalkoholu).

## Typ a rozteč konektorů

- Přední desky: **14 pinů v jedné řadě** (14 pájecích plošek, 14 vodičů, z toho jeden červený). Vidět na IMG_9177.
- Rozteč: **2,0 mm** (odhad z fotky, ne 2,5 ani 2,54 mm). Postup: na IMG_9177 jsou ve stejné rovině dvě známé míry, vývody mikrospínače 6,5 × 4,5 mm a dioda s roztečí 7,62 mm. Obě dávají měřítko 23 px/mm. Třináct roztečí konektoru měří 582 px, tedy 25,3 mm, což je 1,95 mm na rozteč.
- Odpovídá to řadě JST PH nebo kompatibilní (délka pouzdra vychází na necelých 15 roztečí, PH má u 14 pinů 29,9 mm). Výrobce konektoru z fotek určit nejde.
- 3pinové konektory senzorů mají stejnou rozteč jako 14pinové (porovnání pájecích bodů vedle sebe na IMG_9196).
- Vodiče mají potisk AWM 1007 (UL1007).

**K potvrzení jedním měřením:** vzdálenost středů první a poslední plošky 14pinového konektoru. Při 2,0 mm vyjde 26,0 mm, při 2,5 mm by to bylo 32,5 mm.

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

1. **Konektory 2,0 mm.** Nepasují do nepájivého pole ani na lišty 2,54 mm. Na nové desce bude footprint 1×14 s roztečí 2,0 mm. Pro zkoušku na drátech je potřeba redukce: buď koupit protikusy řady PH a ověřit, že do sebe zapadnou, nebo vypájet původní konektory z hlavní desky (ta se stejně nahrazuje) a použít je na redukci i na nové desce.
2. **Nová deska na místě původní.** Hlavní deska je přišroubovaná pod horním panelem a displej je za okénkem. Nosná deska může převzít obrys a upevňovací otvory původní desky a OLED umístit do okénka. K tomu chybí rozměry: obrys desky, poloha otvorů, poloha a velikost okénka.
3. **LED u pedálů.** Pokud X13 a X14 opravdu vedou k LED, přibudou dva výstupy na MCP23017 (celkem 12 ze 16).
4. **Relé K1, K2.** Potvrzují, že spínací výstupy na zadních jackách jsou galvanicky oddělené kontakty. PhotoMOS AQY212EH je nahradí.
5. **Síťová část** (zásuvka, vypínač, transformátor) se při napájení z USB-C odpojí.

## Co ještě změřit

1. Vzdálenost středů první a poslední plošky 14pinového konektoru (potvrzení rozteče).
2. Průchodnost pinů předních desek podle `mereni.md`, část 3.
3. Rozměry hlavní desky, polohu upevňovacích otvorů a okénka. Nejlíp deska položená na čtverečkovaném papíře, focená kolmo shora.
4. Co je připojené na X13 a X14.
5. Průměr LED a rozteč spínačů.
