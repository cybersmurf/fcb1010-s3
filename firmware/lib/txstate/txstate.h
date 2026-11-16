// Odchozi stav ovladace pro USB MIDI, bez zavislosti na Arduinu (testuje se na PC).
//
// Misto fronty udalosti se drzi STAV: co ma hostitel vedet (want) a co uz mu
// bylo doruceno (sent). flush() posila jen rozdily a zpravu povazuje za dorucenou
// az ve chvili, kdy ji zapisovac prijal.
//
// Proc ne fronta: fronta ma konecnou delku. Kdyz hostitel prestane cist a fronta
// se zaplni, musi se neco zahodit, a pokud je to pusteni tlacitka, zustane v DAW
// viset. Stav se zaplnit nemuze: ma pevne jeden zaznam na spinac a pedal a po
// obnoveni spojeni se vzdy srovna se skutecnosti.
//
// Cena: stisk a pusteni, ktere oba probehnou behem vypadku hostitele, se neodeslou
// vubec. Za bezneho provozu se kazda hrana odesle hned v dalsim pruchodu smycky.
#pragma once
#include <stdint.h>

struct MidiPacket {
    uint8_t header;  // USB MIDI: cislo kabelu (horni 4 bity) a CIN (dolni 4 bity)
    uint8_t b1;      // stavovy bajt
    uint8_t b2;
    uint8_t b3;
};

// channel je 1-16
inline MidiPacket ccPacket(uint8_t channel, uint8_t cc, uint8_t value) {
    return {0x0B, (uint8_t)(0xB0 | ((channel - 1) & 0x0F)), (uint8_t)(cc & 0x7F), (uint8_t)(value & 0x7F)};
}
inline MidiPacket noteOnPacket(uint8_t channel, uint8_t note, uint8_t velocity) {
    return {0x09, (uint8_t)(0x90 | ((channel - 1) & 0x0F)), (uint8_t)(note & 0x7F), (uint8_t)(velocity & 0x7F)};
}
inline MidiPacket pitchBendPacket(uint8_t channel, uint16_t value14) {
    return {0x0E, (uint8_t)(0xE0 | ((channel - 1) & 0x0F)), (uint8_t)(value14 & 0x7F), (uint8_t)((value14 >> 7) & 0x7F)};
}

class TxState {
public:
    static constexpr uint8_t MAX_SWITCHES = 16;
    static constexpr uint8_t MAX_PEDALS = 4;

    void setSwitch(uint8_t i, bool pressed) {
        if (i < MAX_SWITCHES) swWant_[i] = pressed;
    }
    void setPedal(uint8_t i, uint8_t value) {
        if (i < MAX_PEDALS) pedWant_[i] = value;
    }

    // Prohlasi aktualni stav za doruceny, nic neposila. Vola se, dokud neni
    // hostitel pripojeny: po pripojeni se mu neposlou stare udalosti ani
    // poloha pedalu, ktera by v DAW necekane pohnula parametrem.
    void sync() {
        for (uint8_t i = 0; i < MAX_SWITCHES; i++) swSent_[i] = swWant_[i];
        for (uint8_t i = 0; i < MAX_PEDALS; i++) pedSent_[i] = pedWant_[i];
    }

    bool pending() const {
        for (uint8_t i = 0; i < MAX_SWITCHES; i++) if (swSent_[i] != swWant_[i]) return true;
        for (uint8_t i = 0; i < MAX_PEDALS; i++) if (pedSent_[i] != pedWant_[i]) return true;
        return false;
    }

    // Posle rozdily. Spinace maji prednost pred pedaly.
    //   enc.switchPacket(i, pressed, packet) -> false = pro tento prechod se nic neposila
    //   enc.pedalPacket(i, value, packet)    -> false = pro tento pedal se nic neposila
    //   write(packet)                        -> false = zapis odmitnut (plne FIFO)
    // Vraci true, kdyz je vse doruceno. Pri odmitnutem zapisu skonci a zbytek
    // zustane cekat na dalsi volani.
    template <class Encoder, class Writer>
    bool flush(const Encoder &enc, Writer &&write) {
        for (uint8_t i = 0; i < MAX_SWITCHES; i++) {
            if (swSent_[i] == swWant_[i]) continue;
            const bool want = swWant_[i];
            MidiPacket p;
            if (enc.switchPacket(i, want, p) && !write(p)) return false;
            swSent_[i] = want;
        }
        for (uint8_t i = 0; i < MAX_PEDALS; i++) {
            if (pedSent_[i] == pedWant_[i]) continue;
            const int16_t want = pedWant_[i];
            MidiPacket p;
            if (enc.pedalPacket(i, (uint8_t)want, p) && !write(p)) return false;
            pedSent_[i] = want;
        }
        return true;
    }

private:
    bool swWant_[MAX_SWITCHES] = {};
    bool swSent_[MAX_SWITCHES] = {};
    int16_t pedWant_[MAX_PEDALS] = {-1, -1, -1, -1};  // -1 = jeste nezmereno
    int16_t pedSent_[MAX_PEDALS] = {-1, -1, -1, -1};
};
