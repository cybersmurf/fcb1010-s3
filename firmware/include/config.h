// Konfigurace FCB1010-S3: piny, mapa MIDI, ladici konstanty.
// Vsechno, co se bude menit po stredecnim mereni, je v tomhle souboru.
#pragma once
#include <Arduino.h>

// ---------------------------------------------------------------------------
// Piny (ESP32-S3-DevKitC-1)
// Nepouzivat: 0, 3, 45, 46 (strapping), 19/20 (nativni USB), 43/44 (UART0),
//             35-37 (oktalova PSRAM u modulu N8R8/N16R8), 38/48 (RGB LED na desce)
// ---------------------------------------------------------------------------
constexpr uint8_t NUM_SWITCHES = 12;

// index 0..9 = pedaly 1..10, 10 = UP, 11 = DOWN
// Spinac spina proti GND, pin ma interni pull-up (aktivni v nule).
constexpr uint8_t SWITCH_PINS[NUM_SWITCHES] = {
    4, 5, 6, 7, 15,     // pedaly 1-5 (spodni rada)
    16, 17, 18, 8, 11,  // pedaly 6-10 (horni rada)
    41, 42              // UP, DOWN
};
constexpr uint8_t SW_UP = 10;
constexpr uint8_t SW_DOWN = 11;

// Expression pedaly: ADC1 (GPIO1 = ADC1_CH0, GPIO2 = ADC1_CH1).
// Signal senzoru 0-5 V jde pres delic 2k2 / 3k3 (max. 3,0 V na pinu, v linearnim rozsahu ADC).
constexpr uint8_t NUM_PEDALS = 2;
constexpr uint8_t PEDAL_PINS[NUM_PEDALS] = {1, 2};
constexpr bool PEDAL_INVERT[NUM_PEDALS] = {false, false};

// WS2812B: jedna LED na spinac, poradi stejne jako SWITCH_PINS.
constexpr uint8_t LED_STRIP_PIN = 12;
constexpr uint8_t NUM_LEDS = NUM_SWITCHES;
constexpr uint8_t LED_BRIGHTNESS = 40;  // 0-255; nizsi = mensi odber i presvit do senzoru

// Stavova RGB LED primo na DevKitu. V hotovem FCB vypnout (false) nebo prelepit:
// sviti do optickych senzoru pedalu.
constexpr bool STATUS_LED_ENABLED = true;

// Rezervovano podle pinout.md v0.2 (v kodu zatim nepouzito):
//   GPIO13 = MIDI OUT (UART1 TX), GPIO14 = MIDI IN (UART1 RX),
//   GPIO21 = I2C SDA, GPIO47 = I2C SCL (MCP23017, OLED),
//   GPIO9 = AUX 1, GPIO10 = AUX 2 (zadni jacky)

// ---------------------------------------------------------------------------
// MIDI
// ---------------------------------------------------------------------------
constexpr uint8_t MIDI_CHANNEL = 1;  // 1-16

// Rezim CC: momentove CC (stisk = 127, pusteni = 0) pro Logic "Learn".
// Kdyz Logic pri uceni zlobi kvuli hodnote 0, nastav na false.
constexpr bool CC_SEND_RELEASE = true;

struct SwitchMap {
    const char *name;   // jen pro ladici vypis a popisky
    uint8_t cc;         // rezim CC
    uint8_t mcuNote;    // rezim MCU (Mackie Control), 0xFF = nic
    uint32_t color;     // 0xRRGGBB, barva LED pri zpetne vazbe z DAW
};

// CC 20-31 jsou v MIDI specifikaci nedefinovana, takze s nicim nekoliduji.
// Cisla not MCU jsou overena proti dvema popisum protokolu (TouchMCU,
// libMackieControl); proti Logicu zatim nezkouseno.
constexpr SwitchMap SWITCH_MAP[NUM_SWITCHES] = {
    {"Record",    20, 95, 0xFF0000},
    {"Play",      21, 94, 0x00FF00},
    {"Stop",      22, 93, 0xFFFFFF},
    {"Undo",      23, 81, 0xFF8000},
    {"Rewind",    24, 91, 0x0040FF},
    {"Cycle",     25, 86, 0xFFFF00},
    {"Click",     26, 89, 0x00FFFF},
    {"Forward",   27, 92, 0x0040FF},
    {"Punch",     28, 87, 0xFF00FF},
    {"Replace",   29, 88, 0xFF00FF},
    {"Up/Save",   30, 80, 0x808080},
    {"Down/Mark", 31, 84, 0x808080},
};

// Expression pedaly v rezimu CC (CC 85/86 jsou take nedefinovana).
constexpr uint8_t PEDAL_CC[NUM_PEDALS] = {85, 86};

// ---------------------------------------------------------------------------
// Ladeni
// ---------------------------------------------------------------------------
constexpr uint32_t DEBOUNCE_MS = 20;       // po zmene stavu se spinac na tuhle dobu "zamkne"
constexpr uint32_t PEDAL_PERIOD_MS = 4;    // perioda cteni pedalu
constexpr uint8_t PEDAL_OVERSAMPLE = 8;    // pocet vzorku ADC na jedno cteni
constexpr float PEDAL_SMOOTHING = 0.25f;   // EMA: 1.0 = bez filtru, mensi = hladsi a pomalejsi
constexpr float PEDAL_EDGE_MARGIN = 0.04f; // mrtva zona na obou koncich drahy (podil rozsahu)
constexpr uint32_t CALIBRATION_MS = 6000;  // delka kalibrace pedalu po zapnuti
