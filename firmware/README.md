# FCB1010-S3 firmware

Firmware pro Behringer FCB1010 přestavěný na ESP32-S3: USB MIDI (bez ovladačů), 12 spínačů, 2 expression pedály, 12× WS2812B.

Verze 0.1. Neumí zatím 5pinové MIDI, profil GX-700, původní LED přes MCP23017 ani displej; plán je v `../docs/specifikace.md`, piny v `../docs/pinout.md`.

Stav: **sestavení ověřeno** (PlatformIO, arduino-esp32 3.3.12, deska `esp32-s3-devkitc-1`). **Na hardwaru zatím neběželo.**

## Sestavení a nahrání

```
pio run                 # sestavit
pio run -t upload       # nahrát (kabel v konektoru "UART")
pio device monitor      # ladicí výpis, 115200 Bd
```

DevKitC-1 má dva USB konektory:

- **UART**: nahrávání a ladicí výpis
- **USB**: nativní USB, tady se deska přihlásí Macu jako MIDI zařízení `FCB1010-S3`

Na Macu ji uvidíš v Audio MIDI Setup → MIDI Studio.

## Zkouška na nepájivém poli (bez FCB)

1. Tlačítko mezi GPIO4 a GND = pedál 1 (Record, CC 20). Druhé mezi GPIO5 a GND = pedál 2.
2. Potenciometr 10k mezi 3V3 a GND, jezdec na GPIO1 = expression pedál A (CC 85). Bez kalibrace pojede jen zhruba, viz níže.
3. Stavová LED na desce: oranžová = start, červená = počítač desku nevidí, zelená = režim CC, modrá = režim MCU.

## Volba režimu při zapnutí

Podrž při připojení napájení, volba se uloží:

| Podržet | Akce |
|---|---|
| pedál 1 | režim CC (výchozí) |
| pedál 2 | režim MCU, experimentální |
| UP + DOWN | kalibrace pedálů: 6 s šlapej oba pedály z dorazu na doraz |

## Režim CC a Logic

Každý spínač pošle při stisku CC s hodnotou 127 a při puštění 0 (kanál 1, CC 20–31). Pedály posílají CC 85 a 86.

V Logicu: Logic Pro → Control Surfaces → Learn Assignment for…, vyber příkaz a šlápni na pedál. Kdyby Logic při učení zlobil kvůli hodnotě 0 při puštění, nastav v `include/config.h` `CC_SEND_RELEASE = false`.

## Režim MCU (experimentální)

Spínače posílají noty Mackie Control a Logic vrací stav tlačítek, který se zobrazí na LED. Neověřeno:

- jestli Logic přijme zařízení bez úvodního SysEx handshake,
- pedál A jako master fader (pitch bend na kanálu 9) bez "touch" noty.

## Kde co je

- `include/config.h`: piny, mapa CC/not, barvy LED, ladicí konstanty
- `src/main.cpp`: logika
- `platformio.ini`: USB režim OTG (`ARDUINO_USB_MODE=0`), bez něj se MIDI neobjeví

## Známá omezení

- Spínače se čtou každý na vlastním pinu proti GND. Jestli jsou desky spínačů ve FCB zapojené maticově, přepíše se jen `readSwitchRaw()`.
- Debounce hlásí hranu okamžitě a pak spínač na 20 ms zamkne. Krátká rušivá špička by se tedy projevila jako stisk; na PCB proto počítáme s RC filtrem.
