# FCB1010-S3: měřicí protokol

Vyplnit při otevření přístroje. Pořadí je podle toho, co nejvíc blokuje návrh desky. Sloupec „čekáme“ je z cizího kusu (Fractal fórum), sloupec „naměřeno“ doplnit.

## 0. Bezpečnost

- Před otevřením vytáhnout síťový kabel. Uvnitř je síťové napětí u zásuvky, vypínače, pojistky a na primáru transformátoru.
- Části 1 až 6 se dělají **bez napájení**. Pod napětím je jen část 7, a tam se měří jen na nízkonapěťové straně (5 V).

## 1. Fotky

Kolmo, ostře, s pravítkem v záběru tam, kde jde o rozměr.

- [ ] celý vnitřek po sejmutí dna
- [ ] hlavní deska shora (celá) a detail každého konektoru
- [ ] hlavní deska zespodu (po vyjmutí, stačí později)
- [ ] obě přední desky se spínači, z obou stran, a jejich konektory a kabely
- [ ] destička senzoru u obou pedálů, z obou stran
- [ ] destička MIDI z obou stran
- [ ] destička jacků Switch 1/2 z obou stran
- [ ] zadní panel zevnitř i zvenku
- [ ] horní panel kolem displeje zevnitř i zvenku
- [ ] štítek na EPROM a potisk hlavní desky (číslo desky, revize)

## 2. Konektory předních desek (blokuje desku nejvíc)

| Otázka | Spodní deska | Horní deska |
|---|---|---|
| Počet pinů | | |
| Jedna řada, nebo dvě? | | |
| Vzdálenost os krajních pinů (mm, posuvkou) | | |
| Kabel: plochý, nebo jednotlivé vodiče? | | |
| Na hlavní desce: kolíky, nebo dutinky? | | |
| Zámek nebo klíč, nápis výrobce na pouzdře | | |
| Kabel jde vytáhnout, nebo je zapájený? | | |

Pomůcka pro 14 pinů v jedné řadě: 33,0 mm = rozteč 2,54; 32,5 mm = rozteč 2,5; 26,0 mm = rozteč 2,0.

## 3. Pinout předních desek

Multimetr v režimu diody. Pin 1 má být u červeného vodiče. Měří se na odpojeném konektoru přední desky.

Jak poznat: LED při správné polaritě slabě svítí (červený hrot na anodu). Spínač se projeví až při stisku a jen v jednom směru, protože má v sérii diodu.

### Spodní deska (1–5, DOWN)

| Pin | Čekáme | Naměřeno |
|---|---|---|
| 1 | anoda LED 1, 2, 3 | |
| 2 | anoda LED 4, 5 | |
| 3 | katoda LED 5 | |
| 4 | katoda LED 4 | |
| 5 | katoda LED 3 | |
| 6 | katoda LED 2 | |
| 7 | katoda LED 1 | |
| 8 | spínač 1 | |
| 9 | spínač 2 | |
| 10 | spínač 3 | |
| 11 | spínač 4 | |
| 12 | spínač 5 | |
| 13 | DOWN | |
| 14 | společný vodič spínačů | |

### Horní deska (6–10, UP)

| Pin | Čekáme | Naměřeno |
|---|---|---|
| 1 | anoda LED 6–10 | |
| 2 | katoda LED 10 | |
| 3 | katoda LED 9 | |
| 4 | katoda LED 8 | |
| 5 | katoda LED 7 | |
| 6 | katoda LED 6 | |
| 7 | spínač 6 | |
| 8 | spínač 7 | |
| 9 | spínač 8 | |
| 10 | spínač 9 | |
| 11 | spínač 10 | |
| 12 | UP | |
| 13 | společný vodič spínačů | |
| 14 | nezapojeno | |

### Doplňující otázky

| Otázka | Odpověď |
|---|---|
| Směr diody u spínače: který hrot musí být na pinu spínače, aby při stisku vedl? (červený / černý) | |
| Úbytek na spínači při stisku podle multimetru (V) | |
| Je na přední desce u LED odpor? Odpor mezi pinem anody a vývodem LED (Ω) | |
| Barva a průměr LED (3 / 5 mm) | |
| Mají UP a DOWN vlastní LED? | |

## 4. Pedály

| Otázka | Pedál A | Pedál B |
|---|---|---|
| Počet vodičů a barvy v pořadí od pinu 1 | | |
| Rozteč konektoru (mm) | | |
| Součástky na destičce senzoru (stačí fotka) | | |

## 5. Ostatní desky a mechanika

| Otázka | Odpověď |
|---|---|
| Destička MIDI: kolik vodičů vede do hlavní desky, rozteč | |
| Destička MIDI: jsou na ní odpory 220 Ω? Kolik? | |
| Destička MIDI: je na ní odpor mezi výstupem optočlenu a napájením (pull-up)? | |
| Destička jacků: kolik vodičů, je objímka jacku spojená s kostrou? (prozvonit) | |
| Displej: je napevno na hlavní desce? | |
| Hlavní deska: rozměry (mm) | |
| Montážní body: souřadnice od levého dolního rohu desky (mm), průměr otvoru | |
| Výška distančních sloupků (mm) | |
| Otvor po síťové zásuvce v zadním panelu (mm × mm), tloušťka plechu | |
| Okénko displeje: rozměr (mm × mm), je zabarvené? | |
| Volné místo na horním panelu kolem okénka pro výřez asi 60 × 32 mm | |

## 6. Revize

| Otázka | Odpověď |
|---|---|
| Štítek na EPROM (verze firmwaru) | |
| Číslo a revize desky podle potisku | |
| Datové kódy na velkých čipech (např. 0312 = 12. týden 2003) | |
| Transformátor: klasický, nebo spínaný zdroj? | |

## 7. Měření pod napětím (jen strana 5 V)

Přístroj zapnutý, černý hrot na zem (kovový chladič stabilizátoru nebo GND na konektoru pedálu). Na síťovou část nesahat.

| Veličina | Pedál A | Pedál B |
|---|---|---|
| Napájení senzoru (V) | | |
| Signál, pata na doraz (V) | | |
| Signál, špička na doraz (V) | | |
| Signál se zátěží 10 kΩ proti zemi, špička na doraz (V) | | |

| Veličina | Hodnota |
|---|---|
| Napětí 5 V větve (V) | |
| Co ukáže displej při zapnutí (případně verze) | |

Měření senzoru při 4,0 V a 3,3 V a jeho odběr se udělají později na stole s DevKitem, ne v přístroji.
