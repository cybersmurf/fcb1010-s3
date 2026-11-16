# FCB1010 → ESP32-S3: návrh

Stav k 16. 11. 2026 (večer, po průzkumu zdrojů). Firmware se sestaví, na hardwaru zatím neběžel. FCB se otevře nejdřív ve středu 18. 11.; údaje o vnitřku jsou z cizích kusů a na vlastním je potřeba je přeměřit. Podrobný průzkum se zdroji je v konverzaci (report „Behringer FCB1010: vnitřní zapojení a návrh ESP32-S3 desky“).

**Tento dokument je první verze návrhu. Aktuální zadání je v `specifikace.md` a aktuální piny a bloky desky v `pinout.md`; kde se liší, platí ony.** Hlavní změny: 5pinové MIDI a profil GX-700 jsou povinné, zadní jacky jsou vstupy AUX, displej OLED 2,42", základ LED jsou původní červené.

Další dokumenty: `pruzkum-vnitrni-zapojeni.md` (úplný report s citacemi), `zdroje.md` (všechny zdroje s výtahy), `firmware/` (zdrojové kódy).

## Cíl

Behringer FCB1010 jako nožní ovladač DAW (Logic Pro) přes jeden USB-C kabel: napájení i MIDI, bez síťového zdroje a bez MIDI rozhraní. NUX MG-30 zůstává samostatný multiefekt, FCB ho neovládá.

## Rozhodnutí

| Téma | Rozhodnutí | Důvod |
|---|---|---|
| DAW | Logic Pro | Kytara jde přes MG-30, takže hlavní výhoda LUNA (UAD v nahrávací cestě) se nevyužije. Logic umí Learn na libovolnou CC. |
| Mozek | ESP32-S3 DevKitC-1 v dutinkových lištách | Jen S3/S2 má nativní USB a tím USB MIDI bez ovladačů. Modul jde vyměnit. |
| Firmware | Vlastní, PlatformIO + arduino-esp32 3.x | PedalinoMini je od v4 closed source (licence 1 € na MAC adresu) a o Mackie Control nic neuvádí. |
| EurekaPROM / UnO | Ne | Řeší jen původní desku, kterou nahrazujeme. |
| Zapojení | Vlastní nosná PCB, žádné vrabčí hnízdo | Spolehlivost v krabici, do které se šlape. |
| Původní deska | Schovat, nic na ní neměnit | Úprava zůstane vratná. |

## Co víme o vnitřku FCB (z průzkumu; přeměřit na vlastním kusu)

- Dvě přední desky: spodní nese spínače 1–5 a DOWN, horní 6–10 a UP. Každá má 14pinový konektor.
- **Žádná matice na předních deskách.** Každý spínač i každá LED má vlastní vodič. Multiplex dělala až původní hlavní deska (doloženo kódem FCB1010-lib), nás se netýká.
- **Spínače:** společný vodič na desku, v sérii s každým spínačem dioda 1N4148. Čtení přes pull-up proti GND funguje (přestavba TEE1010 s Teensy 4.1 to tak dělá).
- **LED:** jen 10 kusů (UP a DOWN LED nemají), společná anoda, každá katoda zvlášť. Sériové odpory nejspíš nejsou na předních deskách.
- **Expression pedály:** IR LED + senzor a gradientní pásek, 3 vodiče (5 V, GND, signál), červený vodič = pin 1. Rozsah signálu odhadem 0,1–4,3 V.
- **Displej a indikační LED u něj jsou přímo na hlavní desce.** S její výměnou zmizí.
- Hlavní deska: procesor 80C32, EPROM 27C256 v IC13, 7805, 2 relé; drží na 3 sloupcích a šroubu přes chladič. Rozměry ani polohy otvorů nejsou nikde zveřejněné.
- Samostatná deska MIDI s optočlenem H11L1 a samostatná destička jacků Switch 1/2.
- Transformátor 9 V AC. O rozdílech mezi revizemi se nepodařilo najít nic doloženého.

### Pinout předních desek (měření jednoho kusu z Fractal fóra, cca 2010)

| Pin | Spodní deska | Horní deska |
|---|---|---|
| 1 (červený) | anoda LED 1, 2, 3 | anoda LED 6–10 |
| 2 | anoda LED 4, 5 | katoda LED 10 |
| 3 | katoda LED 5 | katoda LED 9 |
| 4 | katoda LED 4 | katoda LED 8 |
| 5 | katoda LED 3 | katoda LED 7 |
| 6 | katoda LED 2 | katoda LED 6 |
| 7 | katoda LED 1 | spínač 6 |
| 8 | spínač 1 | spínač 7 |
| 9 | spínač 2 | spínač 8 |
| 10 | spínač 3 | spínač 9 |
| 11 | spínač 4 | spínač 10 |
| 12 | spínač 5 | UP |
| 13 | DOWN | společný vodič spínačů |
| 14 | společný vodič spínačů | nezapojeno |

### Typ konektoru: nejasné

- Report usuzuje na jednořadý krimpovací konektor s jednotlivými vodiči (rozteč 2,54 / 2,5 / 2,0 mm).
- Deska FCBInfinity (mackatack, 2012) má pro přední desky osazené dvouřadé lišty 2×7 (označené LOWER a UPPER) a pro pedály 1×3. Není ale jisté, jestli do nich šly původní kabely, nebo si autor nakrimpoval vlastní.
- Rozhodne měření ve středu. Deska FCBInfinity má vlastní rozměr 160 × 40 mm, jako šablona původní desky se použít nedá.

## Bloky nosné desky

Dvouvrstvá deska, součástky THT, rozměry a montážní otvory podle původní hlavní desky. KiCad, výroba JLCPCB.

**1. Modul.** 2× dutinková lišta 1×22, rozteč 2,54 mm, pro ESP32-S3-DevKitC-1. Pozor: rozteč řad se u klonů liší, změřit na konkrétním kusu.

**2. Vstupy spínačů (12×).** Dva 14pinové konektory podle originálu. Společný vodič spínačů na GND, každý spínač na vlastní GPIO s interním pull-upem, 100 nF na GND, footprint pro volitelný externí pull-up. Kvůli sériové diodě je úroveň při stisku asi 0,4–0,5 V, mez pro logickou nulu je kolem 0,8 V. Externí pull-up proto raději slabý (47 kΩ), nebo žádný.

**3. Vstupy pedálů (2×).** Konektor 3 piny: 5 V, GND, signál. Senzor zůstane na 5 V (předřadný odpor IR LED je na 5 V počítaný). Dělič 10 kΩ (signál → pin) a 15 kΩ (pin → GND), 100 nF na GND u pinu: 4,3 V dá 2,6 V, tedy v rozsahu ADC do 2,9 V. Když senzor dá víc než asi 4,7 V, použít 10 kΩ + 12 kΩ. Nízkoohmový dělič (2k2/3k3) by zatížil výstup senzoru a zkreslil křivku.

**4. LED.** Dvě varianty, obě ať mají na desce footprint:

- *Původní LED (10 ks, červené):* MCP23017 na I2C (GPIO21/47), anody na 3,3 V, každá katoda přes 120–150 Ω na pin expandéru (svítí při LOW). Žádná mechanická práce, ale jen jedna barva a UP/DOWN bez LED.
- *WS2812B (12 ks):* 74AHCT125 jako převodník 3,3 → 5 V, sériový odpor 330 Ω, elektrolyt 470 µF, konektor 3 piny. Barvy podle funkce, ale je potřeba LED mechanicky usadit a odstínit od senzorů pedálů. Firmware zatím počítá s touhle variantou.

**5. USB.** Panelový USB-C na zadní stěně, krátkým kabelem do konektoru „USB“ na DevKitu. Konektor „UART“ zůstane přístupný uvnitř pro nahrávání.

**6. Rezervy (footprinty, neosazovat).** DIN MIDI OUT (GPIO13; při 3,3V logice 33 Ω z 3,3 V na pin 4 a 10 Ω z TX na pin 5, ověřeno ve specifikaci MIDI CA-033; 2× 220 Ω platí jen pro 5 V), displej 3× 7segment s MAX7219 nebo OLED, I2C header pro OLED (GPIO21/47), header s volnými GPIO, 2 relé pro původní jacky Switch 1/2.

## Pinout (ESP32-S3-DevKitC-1)

| Funkce | GPIO |
|---|---|
| Pedály 1–5 | 4, 5, 6, 7, 15 |
| Pedály 6–10 | 16, 17, 18, 8, 9 |
| UP, DOWN | 10, 11 |
| Expression A, B | 1, 2 (ADC1) |
| WS2812 data | 12 |
| Rezerva DIN MIDI OUT | 13 |
| Rezerva I2C SDA, SCL | 21, 47 |
| Nativní USB D−, D+ | 19, 20 (jen přes konektor USB) |

Nepoužívat: 0, 3, 45, 46 (strapping), 43, 44 (UART0), 35–37 (PSRAM u modulů N8R8/N16R8), 38/48 (RGB LED na desce).

## Napájení

Vše z USB (5 V, limit 500 mA). Odhad: ESP32-S3 bez Wi-Fi do 100 mA, 12× WS2812 při jasu 40/255 do 120 mA, IR LED senzorů do 50 mA. Rezerva je dostatečná. Uvnitř už nebude síťové napětí.

## Mapa MIDI

Režim CC, kanál 1. Funkce jsou jen doporučení, v Logicu se přiřadí přes Learn.

| Spínač | CC | Doporučená funkce |
|---|---|---|
| 1 | 20 | Record |
| 2 | 21 | Play/Stop |
| 3 | 22 | Stop / návrat na začátek |
| 4 | 23 | Undo |
| 5 | 24 | Zahodit nahrávku a vrátit se |
| 6 | 25 | Cycle |
| 7 | 26 | Metronom |
| 8 | 27 | Capture as Recording |
| 9 | 28 | Předchozí marker |
| 10 | 29 | Další marker |
| UP | 30 | volné |
| DOWN | 31 | volné |
| Expression A | 85 | hlasitost poslechu |
| Expression B | 86 | wah / parametr pluginu |

Režim MCU (Mackie Control) je ve firmwaru připravený jako experimentální: LED by ukazovaly stav Record/Cycle z Logicu a ovladač by fungoval i v LUNA. Čísla not ve firmwaru (80–95) průzkum potvrdil. Zbývá doplnit odpověď na SysEx handshake (dotaz `00` → odpověď `01`, `02` → `03`, hlavička `F0 00 00 66 14`) a fader touch (nota 112) před pitch bendem master faderu.

## Seznam dílů

- ESP32-S3-DevKitC-1 (1 kus leží v práci; druhý jako záloha)
- pásek WS2812B, 12 LED (podle rozteče pedálů možná jednotlivé LED na drátech)
- 74AHCT125, patice DIP-14
- panelový USB-C konektor s kabelem
- dutinkové lišty 2,54 mm, konektory podle FCB (zjistí se ve středu)
- odpory 150 Ω, 330 Ω, 10 kΩ, 12 kΩ, 15 kΩ, 47 kΩ; kondenzátory 100 nF, 470 µF
- MCP23017 (varianta s původními LED)
- na zkoušky: nepájivé pole, 2 tlačítka, potenciometr 10 kΩ

## Checklist na středu (podle toho, co nejvíc blokuje PCB)

1. **Konektory předních desek:** fotka zblízka s měřítkem. Jednořadý, nebo dvouřadý? Posuvkou vzdálenost os krajních pinů, nápis výrobce na pouzdře, kolíky nebo dutinky na desce.
2. **Pinout podle tabulky výše** ověřit multimetrem v režimu diody (anody, katody, společný vodič, orientace diod u spínačů).
3. **Odpory LED:** jsou na přední desce, nebo ne? Barva a průměr LED.
4. **Pedály:** rozteč a pořadí vodičů; při zapnutém originálu změřit napájení senzoru a signál na obou dorazech. Pozor, uvnitř je síťové napětí.
5. Ostatní konektory hlavní desky: MIDI deska, jacky Switch, transformátor.
6. **Obrys hlavní desky a montážní body:** fotka kolmo s pravítkem nebo sken 1:1 jako podklad do KiCadu; souřadnice otvorů od dvou hran, výška sloupků.
7. Zadní panel: rozměr otvoru po síťové zásuvce (tam přijde USB-C), tloušťka plechu.
8. **Destička MIDI:** fotky obou stran, kde jsou odpory 220 Ω a pull-up optočlenu, kolik vodičů vede do hlavní desky. Totéž destička jacků Switch 1/2.
9. Horní panel kolem displeje: rozměry okénka a volné místo kolem něj pro větší výřez (2,42" OLED).
10. Revize: štítek na EPROM, číslo desky, datové kódy součástek.


## Otevřené otázky

- Typ a rozteč konektorů (středa).
- Původní LED přes MCP23017, nebo WS2812B?
- Displej: bez něj, 7segment s MAX7219, nebo OLED?
- Zachovat DIN MIDI a relé Switch 1/2? Pro DAW nejsou potřeba.
- Vypájet konektory z původní desky (jistota, že sedí), nebo koupit nové a původní desku nechat netknutou?

## Zdroje

- [FCB1010 mit modernem Mikrocontroller bestücken (musiker-board.de)](https://www.musiker-board.de/threads/fcb1010-mit-modernem-mikrocontroller-bestuecken.756515/)
- [PedalinoMini (GitHub)](https://github.com/alf45tar/PedalinoMini)
- [Using MCU Control Surfaces with LUNA (UA)](https://help.uaudio.com/hc/en-us/articles/4406796987540)
- [ESP_MIDI: class-compliant MIDI na ESP32-S3 (GitHub)](https://gh.r-mj.com/collaborative-music-lab/ESP_MIDI)
- [Foot controler FCB1010 (pikobus.webnode.cz)](https://pikobus.webnode.cz/upg/foot-controler-fcb1010/)
- [FCB1010 re-house project, pinout předních desek (Fractal forum)](https://forum.fractalaudio.com/threads/fcb1010-re-house-project.24421/page-3)
- [The Behringer FCB1010 pedal board (Practical Usage)](https://practicalusage.com/the-behringer-fcb1010-pedal-board/)
- [FCB1010 reverse engineering for Arduino (Daniele Veratti)](https://www.danieleveratti.com/behringer-fcb-1010-reverse-engineering-for-arduino/)
- [FCBInfinity (GitHub, mackatack)](https://github.com/mackatack/FCBInfinity) a [blog](https://mackatackblog.wordpress.com/)
- [FCB1010 mods (el34world)](https://el34world.com/Misc/Music/FCB_1.htm)
- [MIDI 1.0 Electrical Specification Update CA-033](https://www.midi.org/wp-content/uploads/wpforo/default_attachments/1709416667-ca33-MIDI-10-Electrical-Specification-Update.pdf)
- [Mackie Control protocol (TouchMCU)](https://github.com/NicoG60/TouchMCU/blob/main/doc/mackie_control_protocol.md)
