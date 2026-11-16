// Testy odchoziho stavu (lib/txstate). Bezi na PC: pio test -e native
#include <unity.h>
#include <vector>
#include "txstate.h"

namespace {

// Hostitel: pamatuje si, co mu doslo, a umi "prestat cist" (plne FIFO).
struct FakeHost {
    bool accepting = true;
    int budget = -1;  // kolik zapisu jeste prijme, -1 = bez omezeni
    std::vector<MidiPacket> received;
    bool noteDown[128] = {};
    int ccValue[128];

    FakeHost() { for (int &v : ccValue) v = -1; }

    bool write(const MidiPacket &p) {
        if (!accepting) return false;
        if (budget == 0) return false;
        if (budget > 0) budget--;
        received.push_back(p);
        const uint8_t type = p.b1 & 0xF0;
        if (type == 0x90) noteDown[p.b2] = p.b3 > 0;
        if (type == 0xB0) ccValue[p.b2] = p.b3;
        return true;
    }
};

// Rezim MCU: spinac i = nota 80 + i, pedal 0 = CC 85 (pro jednoduchost testu).
struct McuEncoder {
    bool switchPacket(uint8_t i, bool pressed, MidiPacket &p) const {
        p = noteOnPacket(1, 80 + i, pressed ? 127 : 0);
        return true;
    }
    bool pedalPacket(uint8_t i, uint8_t value, MidiPacket &p) const {
        p = ccPacket(1, 85 + i, value);
        return true;
    }
};

// Rezim CC bez zpravy pri pusteni.
struct PressOnlyEncoder {
    bool switchPacket(uint8_t i, bool pressed, MidiPacket &p) const {
        if (!pressed) return false;
        p = ccPacket(1, 20 + i, 127);
        return true;
    }
    bool pedalPacket(uint8_t, uint8_t, MidiPacket &) const { return false; }
};

bool flushTo(TxState &tx, FakeHost &host) {
    return tx.flush(McuEncoder{}, [&](const MidiPacket &p) { return host.write(p); });
}

}  // namespace

void setUp() {}
void tearDown() {}

void test_press_and_release_are_sent_in_order() {
    TxState tx;
    FakeHost host;
    tx.setSwitch(3, true);
    TEST_ASSERT_TRUE(flushTo(tx, host));
    tx.setSwitch(3, false);
    TEST_ASSERT_TRUE(flushTo(tx, host));

    TEST_ASSERT_EQUAL(2, host.received.size());
    TEST_ASSERT_EQUAL_HEX8(0x90, host.received[0].b1);
    TEST_ASSERT_EQUAL(83, host.received[0].b2);
    TEST_ASSERT_EQUAL(127, host.received[0].b3);
    TEST_ASSERT_EQUAL(0, host.received[1].b3);
    TEST_ASSERT_FALSE(host.noteDown[83]);
}

void test_release_survives_rejected_write() {
    TxState tx;
    FakeHost host;
    tx.setSwitch(0, true);
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_TRUE(host.noteDown[80]);

    host.accepting = false;  // hostitel prestal cist
    tx.setSwitch(0, false);
    for (int n = 0; n < 1000; n++) TEST_ASSERT_FALSE(flushTo(tx, host));
    TEST_ASSERT_TRUE(tx.pending());
    TEST_ASSERT_TRUE(host.noteDown[80]);  // hostitel o pusteni jeste nevi

    host.accepting = true;
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_FALSE(host.noteDown[80]);
    TEST_ASSERT_FALSE(tx.pending());
}

// Scenar z recenze: hostitel prijal stisk, pak prestal cist a uzivatel dal
// slape na vsechno. Zadne mnozstvi udalosti nesmi zpusobit ztratu pusteni.
void test_no_stuck_button_after_any_amount_of_activity_while_blocked() {
    TxState tx;
    FakeHost host;
    for (uint8_t i = 0; i < 12; i++) tx.setSwitch(i, true);
    TEST_ASSERT_TRUE(flushTo(tx, host));
    for (uint8_t i = 0; i < 12; i++) TEST_ASSERT_TRUE(host.noteDown[80 + i]);

    host.accepting = false;
    for (int cycle = 0; cycle < 10000; cycle++) {
        for (uint8_t i = 0; i < 12; i++) {
            tx.setSwitch(i, false);
            flushTo(tx, host);
            tx.setSwitch(i, true);
            flushTo(tx, host);
        }
    }
    for (uint8_t i = 0; i < 12; i++) tx.setSwitch(i, false);  // vse pusteno

    host.accepting = true;
    const size_t before = host.received.size();
    TEST_ASSERT_TRUE(flushTo(tx, host));
    for (uint8_t i = 0; i < 12; i++) TEST_ASSERT_FALSE(host.noteDown[80 + i]);
    TEST_ASSERT_EQUAL(12, host.received.size() - before);  // presne jedno pusteni na spinac
}

void test_partial_acceptance_resumes_where_it_stopped() {
    TxState tx;
    FakeHost host;
    for (uint8_t i = 0; i < 6; i++) tx.setSwitch(i, true);
    host.budget = 2;  // FIFO vezme jen dva pakety
    TEST_ASSERT_FALSE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(2, host.received.size());

    host.budget = -1;
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(6, host.received.size());  // zadny duplikat, zadna ztrata
    for (uint8_t i = 0; i < 6; i++) TEST_ASSERT_TRUE(host.noteDown[80 + i]);
}

void test_pedal_sends_only_latest_value_after_block() {
    TxState tx;
    FakeHost host;
    tx.setPedal(0, 10);
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(10, host.ccValue[85]);

    host.accepting = false;
    for (int v = 11; v <= 100; v++) {
        tx.setPedal(0, (uint8_t)v);
        flushTo(tx, host);
    }
    host.accepting = true;
    const size_t before = host.received.size();
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(1, host.received.size() - before);
    TEST_ASSERT_EQUAL(100, host.ccValue[85]);
}

void test_sync_sends_nothing() {
    TxState tx;
    FakeHost host;
    tx.setSwitch(2, true);  // drzeny spinac a poloha pedalu pred pripojenim USB
    tx.setPedal(1, 64);
    tx.sync();
    TEST_ASSERT_FALSE(tx.pending());
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(0, host.received.size());

    tx.setSwitch(2, false);  // prvni skutecna zmena po pripojeni se posle
    TEST_ASSERT_TRUE(flushTo(tx, host));
    TEST_ASSERT_EQUAL(1, host.received.size());
}

void test_transition_without_message_is_not_retried() {
    TxState tx;
    FakeHost host;
    auto flush = [&] { return tx.flush(PressOnlyEncoder{}, [&](const MidiPacket &p) { return host.write(p); }); };
    tx.setSwitch(1, true);
    TEST_ASSERT_TRUE(flush());
    tx.setSwitch(1, false);  // pusteni se v tomto rezimu neposila
    TEST_ASSERT_TRUE(flush());
    TEST_ASSERT_FALSE(tx.pending());
    TEST_ASSERT_EQUAL(1, host.received.size());
    TEST_ASSERT_EQUAL(21, host.received[0].b2);
}

void test_packet_builders() {
    MidiPacket p = ccPacket(1, 20, 127);
    TEST_ASSERT_EQUAL_HEX8(0x0B, p.header);
    TEST_ASSERT_EQUAL_HEX8(0xB0, p.b1);
    p = noteOnPacket(16, 95, 127);
    TEST_ASSERT_EQUAL_HEX8(0x09, p.header);
    TEST_ASSERT_EQUAL_HEX8(0x9F, p.b1);
    p = pitchBendPacket(9, 16383);
    TEST_ASSERT_EQUAL_HEX8(0x0E, p.header);
    TEST_ASSERT_EQUAL_HEX8(0xE8, p.b1);
    TEST_ASSERT_EQUAL(127, p.b2);
    TEST_ASSERT_EQUAL(127, p.b3);
    p = pitchBendPacket(9, 8192);
    TEST_ASSERT_EQUAL(0, p.b2);
    TEST_ASSERT_EQUAL(64, p.b3);
}

int main(int, char **) {
    UNITY_BEGIN();
    RUN_TEST(test_press_and_release_are_sent_in_order);
    RUN_TEST(test_release_survives_rejected_write);
    RUN_TEST(test_no_stuck_button_after_any_amount_of_activity_while_blocked);
    RUN_TEST(test_partial_acceptance_resumes_where_it_stopped);
    RUN_TEST(test_pedal_sends_only_latest_value_after_block);
    RUN_TEST(test_sync_sends_nothing);
    RUN_TEST(test_transition_without_message_is_not_retried);
    RUN_TEST(test_packet_builders);
    return UNITY_END();
}
