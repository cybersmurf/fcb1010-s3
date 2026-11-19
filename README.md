# FCB1010-S3

Upgrade old fcb1010 to new era.

Přestavba nožního MIDI ovladače Behringer FCB1010 na ESP32-S3: původní hlavní deska a síťový zdroj ven, místo nich vlastní nosná deska s ESP32-S3-DevKitC-1.

*Rebuild of the Behringer FCB1010 MIDI foot controller around an ESP32-S3 (USB MIDI, 5-pin DIN MIDI, device profiles). Documentation is in Czech.*

## Co má umět

- **Ovladač DAW přes USB** (Logic Pro): transport, undo, cycle, metronom, pedály. USB MIDI bez ovladačů, napájení jedním kabelem USB-C.
- **Samostatný ovladač přes 5pinové MIDI**, hlavně pro Boss GX-700: volba patchů, pedály.
- **MIDI rozhraní USB ↔ DIN** pro počítač.
- Profily jako sestavy: jeden pedál může poslat více zpráv více přístrojům.
- Možnosti dalšího rozvoje: NUX MG-30 (jack TRS, USB host), Mackie Control s LED zpětnou vazbou, další profily.

## Stav (16. 11. 2026)

| Část | Stav |
|---|---|
| Koncepce a specifikace | hotová, verze 2 |
| Pinout a bloky nosné desky | verze 0.2, konektory předních desek neověřené |
| Firmware | verze 0.1: USB MIDI, 12 spínačů, 2 pedály, WS2812B. Sestaví se, **na hardwaru zatím neběžel** |
| Automatické kontroly | u každého pull requestu se pustí testy logiky a sestaví firmware |
| Měření vlastního kusu | čeká na otevření přístroje |
| Schéma a deska (KiCad) | nezačato |

## Obsah

| Cesta | Co tam je |
|---|---|
| [`docs/specifikace.md`](docs/specifikace.md) | co má přístroj umět, profily, směrování MIDI, stavba firmwaru, postup, rizika |
| [`docs/pinout.md`](docs/pinout.md) | přiřazení GPIO, konektory, bloky desky, displej |
| [`docs/obvody.md`](docs/obvody.md) | zapojení vstupů pedálů a spínačů, filtry, napájení, zem |
| [`docs/mereni.md`](docs/mereni.md) | měřicí protokol pro otevření přístroje |
| [`docs/nalezy-z-fotek.md`](docs/nalezy-z-fotek.md) | co je vidět na fotkách otevřeného přístroje (18. 11. 2026) |
| [`hardware/`](hardware/) | rozvržení nosné desky, schéma v PDF a [`hardware/kicad/`](hardware/kicad/) se schématem pro KiCad |
| [`docs/nakup.md`](docs/nakup.md) | nákupní seznam |
| [`docs/navrh.md`](docs/navrh.md) | první verze návrhu, co víme o vnitřku FCB, checklist měření |
| [`docs/pruzkum-vnitrni-zapojeni.md`](docs/pruzkum-vnitrni-zapojeni.md) | průzkum vnitřního zapojení FCB1010 s citacemi a mírou jistoty |
| [`docs/zdroje.md`](docs/zdroje.md) | všechny použité zdroje s výtahy |
| [`firmware/`](firmware/) | projekt pro PlatformIO (arduino-esp32 3.x) |

## Sestavení firmwaru

```
cd firmware
pio run
pio run -t upload
```

Podrobnosti v [`firmware/README.md`](firmware/README.md).

## Upozornění

- Uvnitř původního FCB1010 je síťové napětí. Měření za chodu jen s rozmyslem.
- Pinouty konektorů v dokumentaci pocházejí z cizích kusů a z fór. Před zapojením ověřit na vlastním přístroji.
- Licence zatím není určená.
