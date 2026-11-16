# FCB1010-S3: obvody vstupů a napájení (verze 0.1)

Stav k 16. 11. 2026. Návrh na úrovni zapojení a hodnot, podklad pro schéma. Upřesňuje `pinout.md`, kde byl u každého vstupu jen jeden kondenzátor 100 nF. Hodnoty u senzorů pedálů jsou předběžné, dokud nejsou změřené.

## Proč jeden kondenzátor nestačí

Kondenzátor 100 nF u pinu ADC doporučuje přímo Espressif a s děličem 10k/15k tvoří dolní propust se zlomem asi 265 Hz. Jako ochrana proti rušení to funguje, ale tři věci neřeší:

1. **Napájení senzoru.** Senzor pedálu má být napájený z 5 V z USB a ADC měří proti vlastní vnitřní referenci. Každý pokles 5 V se proto objeví v naměřené hodnotě. Pokles o 50 mV (rozsvícení LED, odpor kabelu) udělá 1 % rozsahu, tedy víc než jeden krok CC. Tohle je nejspíš příčina kolísání hodnot, které hlásil uživatel v německém vlákně.
2. **Šířka pásma.** Pedál se nohou nepohne rychleji než několikrát za sekundu. Propust na 265 Hz pustí k ADC síťový brum i jeho násobky. Stačí zlom kolem 50 Hz.
3. **Spínače.** Kondenzátor přímo na vodiči ke spínači se při stisku vybíjí přes kontakt bez omezení proudu a vstup nemá definovaný pull-up.

## Vstup expression pedálu

```
USB 5V --[FB]--+--[ LDO, nastavitelné ]--+-- AVDD (4,0 V) --> senzory pedálů
               |                         |
             10µF                    10µF + 100nF

senzor OUT --[10k]--+--[1k]--+--> GPIO1 / GPIO2
                    |        |
                  [15k]    100nF
                    |        |
                  470nF     GND
                    |
                   GND
```

| Prvek | Hodnota | K čemu |
|---|---|---|
| Feritová perlička + 10 µF | – | oddělí senzorovou větev od rušení na 5 V |
| LDO s nastavitelným výstupem | 4,0 V | stabilní napájení senzorů nezávislé na úbytcích na USB; při 4,0 V zůstává rezerva i pro USB na spodní hranici 4,5 V |
| Dělič 10 kΩ / 15 kΩ | poměr 0,6 | 4,0 V → 2,4 V; i kdyby se na vstup dostalo 5 V, vyjde 3,0 V |
| 470 nF za děličem | zlom 56 Hz | hlavní filtr; časová konstanta 2,8 ms |
| 1 kΩ + 100 nF u pinu | zlom 1,6 kHz | vf rušení, zásobník náboje pro vzorkování ADC, omezení proudu do pinu |

Výstupní napětí LDO určují dva odpory. Pokud měření ukáže, že senzory fungují dobře i při 3,3 V, změní se jen ty dva odpory. Dělič může zůstat stejný.

Proč ne operační zesilovač: zdroj s vnitřním odporem 6 kΩ a kondenzátorem u pinu ADC stačí a pro 127 kroků CC není vyšší přesnost potřeba. Kdyby se někdy posílalo 14bitově, dává smysl externí převodník na I2C (ADS1115), ne zesilovač.

### Zpracování ve firmwaru

| Krok | Nastavení | Poznámka |
|---|---|---|
| Čtení | `analogReadMilliVolts`, průměr z 8 vzorků | používá tovární kalibraci ADC |
| Perioda | 4 ms | |
| Exponenciální filtr | α = 0,25, časová konstanta 14 ms | |
| Kalibrace | minimum a maximum uložené v NVS | původní firmware to dělal stejně |
| Mrtvé zóny | 4 % na obou koncích | pedál spolehlivě dojede na 0 a 127 |
| Hystereze | 0,75 kroku | hodnota nekmitá mezi dvěma sousedními |

Jeden krok CC odpovídá asi 20 mV na pinu. Celkové zpoždění od pohybu po odeslání vychází kolem 30 až 40 ms, pro pedál nepostřehnutelné.

## Vstup spínače

```
3V3 --[47k]--+
             |
J1/J2 pin --[470R]--+--> GPIO
                    |
                  100nF
                    |
                   GND
```

| Prvek | Hodnota | K čemu |
|---|---|---|
| Externí pull-up | 47 kΩ | definovaná klidová úroveň, proud při stisku 70 µA |
| Sériový odpor | 470 Ω | omezí vybíjecí proud kondenzátoru přes kontakt a chrání pin před výbojem z kabelu |
| Kondenzátor u pinu | 100 nF | náběh 4,7 ms přes pull-up, doběh 47 µs přes sériový odpor |

Úroveň při stisku: úbytek na sériové diodě 1N4148 při 70 µA je asi 0,45 až 0,5 V a ESP32-S3 zaručuje logickou nulu do 0,82 V. Rezerva je asi 0,3 V. Proto slabý pull-up: s 10 kΩ by úbytek na diodě a sériovém odporu vyšel těsně u hranice.

Kdyby rezerva v praxi nestačila, řešením je přemostit diody na předních deskách. Bez původního multiplexu už nemají funkci.

Stisk se hlásí hned na první hraně a pak se vstup na 20 ms zamkne. Filtr na vstupu zajistí, že krátká rušivá špička hranu nevyvolá.

## Napájení

| Věc | Řešení |
|---|---|
| Vstup | jen USB-C, 5 V |
| Kondenzátory na 5 V | USB dovoluje při připojení nejvýše 10 µF přímo na napájení. Velký elektrolyt pro WS2812B (470 µF) proto musí být za omezením náběhového proudu (odpor nebo spínač s pozvolným náběhem). Ve variantě s původními LED není potřeba. |
| Logika 3,3 V | ze stabilizátoru na DevKitu |
| Senzory pedálů | vlastní větev AVDD, viz výše |
| MCP23017, OLED | 3,3 V, u každého 100 nF |
| 74AHCT125 | 5 V, 100 nF |

## Zem a stínění

- Kostra spojená s GND desky v jednom bodě, u konektoru USB.
- Zem senzorů pedálů vedená zvlášť až k LDO, ne společně s proudem LED.
- Spínací výstupy na zadní jacky jsou plovoucí (PhotoMOS), objímka jacku izolovaná od kostry.
- RGB LED na DevKitu vypnutá nebo přelepená, OLED a případné WS2812B nesmí svítit do štěrbin senzorů.

## Co k tomu změřit

1. Proud, který senzor pedálu odebírá při 5 V (kvůli výběru LDO).
2. Výstupní napětí senzoru na obou dorazech při napájení 5 V, 4,0 V a 3,3 V. Stačí laboratorní zdroj nebo tři odpory.
3. Vnitřní odpor výstupu senzoru: změřit napětí naprázdno a se zátěží 10 kΩ.
4. Úbytek na diodě u spínače při proudu kolem 70 µA (multimetr v režimu diody měří při větším proudu, skutečný úbytek bude nižší).
