// FCB1010-S3: firmware pro Behringer FCB1010 prestaveny na ESP32-S3.
// USB MIDI (class compliant), 12 spinacu, 2 expression pedaly, 12x WS2812B.
//
// Rezimy (volba pri zapnuti, uklada se do NVS):
//   drzet pedal 1        -> rezim CC  (momentove CC, Logic Learn)   [vychozi]
//   drzet pedal 2        -> rezim MCU (noty Mackie Control + LED zpetna vazba) [experimentalni]
//   drzet UP + DOWN      -> kalibrace expression pedalu
//
// Ladici vypis jde na UART0 (konektor "UART" na DevKitu), MIDI na konektor "USB".

#include <Arduino.h>
#include <Preferences.h>
#include <Adafruit_NeoPixel.h>
#include "USB.h"
#include "USBMIDI.h"
#include "tusb.h"
#include "config.h"
#include "txstate.h"

#if ARDUINO_USB_MODE
#error "USB musi bezet v rezimu OTG/TinyUSB (ARDUINO_USB_MODE=0), viz platformio.ini"
#endif

enum Mode : uint8_t { MODE_CC = 0, MODE_MCU = 1 };

static USBMIDI MIDI("FCB1010-S3");
static Adafruit_NeoPixel strip(NUM_LEDS, LED_STRIP_PIN, NEO_GRB + NEO_KHZ800);
static Preferences prefs;

static Mode mode = MODE_CC;

// --- spinace ---------------------------------------------------------------
struct SwitchState {
    bool pressed = false;
    uint32_t lastEdge = 0;  // millis() posledni prijate hrany
};
static SwitchState sw[NUM_SWITCHES];

// --- pedaly ----------------------------------------------------------------
struct PedalState {
    uint16_t calMin = 300;
    uint16_t calMax = 3700;
    float filtered = 0;
    float rawAtLastSend = -10000;
    int16_t lastValue = -1;
};
static PedalState pedal[NUM_PEDALS];

// --- LED -------------------------------------------------------------------
static bool ledFeedback[NUM_LEDS];  // stav poslany z DAW
static bool ledsDirty = true;

// ---------------------------------------------------------------------------
static inline bool readSwitchRaw(uint8_t i) {
    return digitalRead(SWITCH_PINS[i]) == LOW;
}

static uint16_t readPedalRaw(uint8_t i) {
    uint32_t sum = 0;
    for (uint8_t n = 0; n < PEDAL_OVERSAMPLE; n++) sum += analogRead(PEDAL_PINS[i]);
    return sum / PEDAL_OVERSAMPLE;
}

static void statusLed(uint8_t r, uint8_t g, uint8_t b) {
#ifdef RGB_BUILTIN
    if (STATUS_LED_ENABLED) rgbLedWrite(RGB_BUILTIN, r, g, b);
#endif
}

static uint32_t dim(uint32_t color, uint8_t shift) {
    // kazdy kanal zvlast, aby bity nepretekaly do sousedni barvy
    return (color >> shift) & ((0xFFu >> shift) * 0x010101UL);
}

static void renderLeds() {
    for (uint8_t i = 0; i < NUM_LEDS; i++) {
        uint32_t c = 0;
        if (sw[i].pressed) c = 0xFFFFFF;                  // stisk = bila
        else if (ledFeedback[i]) c = SWITCH_MAP[i].color; // stav z DAW
        else c = dim(SWITCH_MAP[i].color, 5);             // slaby orientacni svit
        strip.setPixelColor(i, c);
    }
    strip.show();
    ledsDirty = false;
}

// ---------------------------------------------------------------------------
// Odchozi USB MIDI
// Knihovni noteOn()/controlChange() zahazuji navratovou hodnotu zapisu, takze
// pri plnem vysilacim FIFO by se zprava ztratila a pusteni tlacitka by v DAW
// zustalo viset. Proto se drzi stav (lib/txstate): posilaji se rozdily mezi
// tim, co ma hostitel vedet, a tim, co uz prijal. Na rozdil od fronty se
// nemuze zaplnit.
// ---------------------------------------------------------------------------
static TxState tx;

struct ProfileEncoder {
    bool switchPacket(uint8_t i, bool pressed, MidiPacket &p) const {
        if (i >= NUM_SWITCHES) return false;
        const SwitchMap &m = SWITCH_MAP[i];
        if (mode == MODE_CC) {
            if (!pressed && !CC_SEND_RELEASE) return false;
            p = ccPacket(MIDI_CHANNEL, m.cc, pressed ? 127 : 0);
            return true;
        }
        if (m.mcuNote == 0xFF) return false;
        // MCU: tlacitko = Note On, stisk velocity 127, pusteni velocity 0 (kanal 1)
        p = noteOnPacket(1, m.mcuNote, pressed ? 127 : 0);
        return true;
    }
    bool pedalPacket(uint8_t i, uint8_t value, MidiPacket &p) const {
        if (i >= NUM_PEDALS) return false;
        if (mode == MODE_CC) {
            p = ccPacket(MIDI_CHANNEL, PEDAL_CC[i], value);
            return true;
        }
        if (i != 0) return false;
        // MCU: pedal A = master fader (pitch bend na kanalu 9, 14 bitu). Experimentalni.
        p = pitchBendPacket(9, (uint16_t)((uint32_t)value * 16383UL / 127UL));
        return true;
    }
};

static bool writeUsbPacket(const MidiPacket &p) {
    midiEventPacket_t e = {p.header, p.b1, p.b2, p.b3};
    return MIDI.writePacket(&e);  // false = FIFO plne, zkusi se v dalsim pruchodu
}

// ---------------------------------------------------------------------------
// Udalosti
// ---------------------------------------------------------------------------
static void onSwitch(uint8_t i, bool pressed) {
    Serial.printf("SW %2u %-10s %s\n", i + 1, SWITCH_MAP[i].name, pressed ? "DOWN" : "up");
    tx.setSwitch(i, pressed);
    ledsDirty = true;
}

static void onPedal(uint8_t i, uint8_t value) {
    Serial.printf("PEDAL %c = %u\n", 'A' + i, value);
    tx.setPedal(i, value);
}

// Zpetna vazba z DAW: MCU posila stav LED tlacitek jako Note On (velocity 0 = zhasnuto).
// V rezimu CC se stejne chova CC se shodnym cislem, kdyby ho nekdo chtel posilat.
static void pollMidiIn() {
    midiEventPacket_t p;
    while (MIDI.readPacket(&p)) {
        const uint8_t status = p.byte1 & 0xF0;
        const bool isNote = (status == 0x90 || status == 0x80);
        const bool isCc = (status == 0xB0);
        if (!isNote && !isCc) continue;
        const bool on = (status != 0x80) && p.byte3 > 0;

        for (uint8_t i = 0; i < NUM_SWITCHES; i++) {
            const bool match = (mode == MODE_MCU) ? (isNote && SWITCH_MAP[i].mcuNote == p.byte2)
                                                  : (isCc && SWITCH_MAP[i].cc == p.byte2);
            if (match && ledFeedback[i] != on) {
                ledFeedback[i] = on;
                ledsDirty = true;
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Smycky
// ---------------------------------------------------------------------------
static void scanSwitches(uint32_t now) {
    for (uint8_t i = 0; i < NUM_SWITCHES; i++) {
        const bool raw = readSwitchRaw(i);
        // Hrana se hlasi okamzite (nulova latence), potom se spinac na DEBOUNCE_MS zamkne.
        // Rozdil bez znamenka je spravne i po preteceni millis() (49,7 dne).
        if (raw != sw[i].pressed && (uint32_t)(now - sw[i].lastEdge) >= DEBOUNCE_MS) {
            sw[i].pressed = raw;
            sw[i].lastEdge = now;
            onSwitch(i, raw);
        }
    }
}

static void scanPedals() {
    for (uint8_t i = 0; i < NUM_PEDALS; i++) {
        PedalState &p = pedal[i];
        const float raw = readPedalRaw(i);
        p.filtered += (raw - p.filtered) * PEDAL_SMOOTHING;

        const float span = (float)p.calMax - (float)p.calMin;
        if (span < 100) continue;  // nezkalibrovano nebo odpojeny senzor
        const float lo = p.calMin + span * PEDAL_EDGE_MARGIN;
        const float hi = p.calMax - span * PEDAL_EDGE_MARGIN;
        float t = (p.filtered - lo) / (hi - lo);
        t = constrain(t, 0.0f, 1.0f);
        if (PEDAL_INVERT[i]) t = 1.0f - t;
        const int16_t value = (int16_t)lroundf(t * 127.0f);

        if (value == p.lastValue) continue;
        // Hystereze proti kmitani mezi dvema sousednimi hodnotami;
        // krajni hodnoty 0 a 127 projdou vzdy, aby pedal dojel na doraz.
        const float step = (hi - lo) / 127.0f;
        const bool edge = (value == 0 || value == 127);
        if (!edge && fabsf(p.filtered - p.rawAtLastSend) < step * 0.75f) continue;

        p.lastValue = value;
        p.rawAtLastSend = p.filtered;
        onPedal(i, (uint8_t)value);
    }
}

// ---------------------------------------------------------------------------
// Start: volba rezimu, kalibrace, NVS
// ---------------------------------------------------------------------------
static void loadSettings() {
    prefs.begin("fcb1010", false);
    mode = (Mode)prefs.getUChar("mode", MODE_CC);
    for (uint8_t i = 0; i < NUM_PEDALS; i++) {
        char key[8];
        snprintf(key, sizeof(key), "min%u", i);
        pedal[i].calMin = prefs.getUShort(key, pedal[i].calMin);
        snprintf(key, sizeof(key), "max%u", i);
        pedal[i].calMax = prefs.getUShort(key, pedal[i].calMax);
    }
}

static void calibratePedals() {
    Serial.println("KALIBRACE: seslapni oba pedaly nekolikrat z dorazu na doraz");
    uint16_t lo[NUM_PEDALS], hi[NUM_PEDALS];
    for (uint8_t i = 0; i < NUM_PEDALS; i++) { lo[i] = 4095; hi[i] = 0; }

    const uint32_t start = millis();
    while (millis() - start < CALIBRATION_MS) {
        for (uint8_t i = 0; i < NUM_PEDALS; i++) {
            const uint16_t v = readPedalRaw(i);
            lo[i] = min(lo[i], v);
            hi[i] = max(hi[i], v);
        }
        const bool blink = ((millis() - start) / 250) % 2;
        statusLed(0, 0, blink ? 40 : 0);
        strip.fill(blink ? 0x000040 : 0);
        strip.show();
        delay(5);
    }

    for (uint8_t i = 0; i < NUM_PEDALS; i++) {
        if (hi[i] - lo[i] < 400) {
            Serial.printf("  pedal %c: rozsah %u-%u je prilis maly, nechavam puvodni\n", 'A' + i, lo[i], hi[i]);
            continue;
        }
        pedal[i].calMin = lo[i];
        pedal[i].calMax = hi[i];
        char key[8];
        snprintf(key, sizeof(key), "min%u", i);
        prefs.putUShort(key, lo[i]);
        snprintf(key, sizeof(key), "max%u", i);
        prefs.putUShort(key, hi[i]);
        Serial.printf("  pedal %c: %u-%u ulozeno\n", 'A' + i, lo[i], hi[i]);
    }
}

void setup() {
    Serial.begin(115200);

    for (uint8_t i = 0; i < NUM_SWITCHES; i++) pinMode(SWITCH_PINS[i], INPUT_PULLUP);
    analogReadResolution(12);
    for (uint8_t i = 0; i < NUM_PEDALS; i++) analogSetPinAttenuation(PEDAL_PINS[i], ADC_11db);

    strip.begin();
    strip.setBrightness(LED_BRIGHTNESS);
    strip.clear();
    strip.show();
    statusLed(40, 20, 0);  // oranzova = startuje

    loadSettings();
    delay(50);  // ustaleni pull-upu pred ctenim startovnich kombinaci

    if (readSwitchRaw(SW_UP) && readSwitchRaw(SW_DOWN)) {
        calibratePedals();
    } else if (readSwitchRaw(0)) {
        mode = MODE_CC;
        prefs.putUChar("mode", mode);
    } else if (readSwitchRaw(1)) {
        mode = MODE_MCU;
        prefs.putUChar("mode", mode);
    }
    Serial.printf("FCB1010-S3 start, rezim %s\n", mode == MODE_CC ? "CC" : "MCU");

    // Spinace drzene pri startu nesmi po nabehu poslat MIDI udalost.
    const uint32_t bootTime = millis();
    for (uint8_t i = 0; i < NUM_SWITCHES; i++) {
        sw[i].pressed = readSwitchRaw(i);
        sw[i].lastEdge = bootTime - DEBOUNCE_MS;  // prvni stisk projde hned
    }
    for (uint8_t i = 0; i < NUM_PEDALS; i++) pedal[i].filtered = readPedalRaw(i);

    USB.manufacturerName("FCB1010-S3 project");
    USB.productName("FCB1010-S3");
    MIDI.begin();
    USB.begin();
}

void loop() {
    static uint32_t lastSwitchScan = 0, lastPedalScan = 0, lastLedRender = 0;
    static int8_t lastMounted = -1;  // -1 = jeste nevyhodnoceno, at se stav ukaze i bez zmeny
    const uint32_t now = millis();

    if (now != lastSwitchScan) {  // 1 kHz
        lastSwitchScan = now;
        scanSwitches(now);
    }
    if (now - lastPedalScan >= PEDAL_PERIOD_MS) {
        lastPedalScan = now;
        scanPedals();
    }

    pollMidiIn();

    const bool mounted = tud_mounted();
    // Bez hostitele se stav jen srovna, aby se po pripojeni neposilaly stare udalosti.
    if (mounted) tx.flush(ProfileEncoder{}, writeUsbPacket);
    else tx.sync();
    if ((int8_t)mounted != lastMounted) {
        lastMounted = (int8_t)mounted;
        Serial.println(mounted ? "USB pripojeno" : "USB odpojeno");
        // zelena = CC, modra = MCU, cervena = pocitac ho nevidi
        if (!mounted) statusLed(40, 0, 0);
        else if (mode == MODE_CC) statusLed(0, 30, 0);
        else statusLed(0, 0, 40);
        if (!mounted) memset(ledFeedback, 0, sizeof(ledFeedback));
        ledsDirty = true;
    }

    if (ledsDirty && now - lastLedRender >= 10) {
        lastLedRender = now;
        renderLeds();
    }
}
