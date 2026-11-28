#!/usr/bin/env python3
"""Generátor schématu nosné desky FCB1010-S3 pro KiCad 7 a novější.

Zapojení je popsané tady v Pythonu (jeden zdroj pravdy), skript z něj vyrobí
fcb1010-s3.kicad_sch a expected-nets.json (zamýšlené přiřazení pin -> síť),
proti kterému se kontroluje netlist vyexportovaný KiCadem (check_netlist.py).

Spuštění: python3 gen_sch.py
"""
import json
import uuid

PROJECT = "fcb1010-s3"
ROOT_UUID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "fcb1010-s3.root"))
_counter = [0]


def uid():
    _counter[0] += 1
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"fcb1010-s3.{_counter[0]}"))


def f(v):
    return f"{round(v, 3):g}"


FONT = "(effects (font (size 1.27 1.27)))"
FONT_HIDE = "(effects (font (size 1.27 1.27)) hide)"

FP_R = "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"
FP_C = "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm"

# ------------------------------------------------------------------ knihovna symbolů
lib = {}          # name -> s-expr text
lib_pins = {}     # name -> {pin number: (x, y)} v souřadnicích symbolu (y nahoru)


def _props(ref, value):
    return (f'(property "Reference" "{ref}" (at 0 0 0) {FONT})'
            f'(property "Value" "{value}" (at 0 0 0) {FONT})'
            f'(property "Footprint" "" (at 0 0 0) {FONT_HIDE})'
            f'(property "Datasheet" "" (at 0 0 0) {FONT_HIDE})')


def _pin(num, name, x, y, ang, length=2.54, typ="passive", hide=False):
    h = " hide" if hide else ""
    return (f'(pin {typ} line (at {f(x)} {f(y)} {ang}) (length {f(length)}){h} '
            f'(name "{name}" {FONT}) (number "{num}" {FONT}))')


def two_pin(name, ref, graphics, p1, p2):
    base = name.split(":")[1]
    lib[name] = (f'(symbol "{name}" (pin_numbers hide) (pin_names (offset 0) hide) (in_bom yes) (on_board yes) '
                 f'{_props(ref, base)}'
                 f'(symbol "{base}_0_1" {graphics})'
                 f'(symbol "{base}_1_1" {_pin(1, "~", *p1, length=1.27)} {_pin(2, "~", *p2, length=1.27)}))')
    lib_pins[name] = {"1": p1[:2], "2": p2[:2]}


STROKE = "(stroke (width 0.254) (type default))"
NOFILL = "(fill (type none))"
two_pin("fcb:R_H", "R", f"(rectangle (start -2.54 1.016) (end 2.54 -1.016) {STROKE} {NOFILL})", (-3.81, 0, 0), (3.81, 0, 180))
two_pin("fcb:R_V", "R", f"(rectangle (start -1.016 2.54) (end 1.016 -2.54) {STROKE} {NOFILL})", (0, 3.81, 270), (0, -3.81, 90))
two_pin("fcb:C_V", "C",
        f"(polyline (pts (xy -2.032 0.635) (xy 2.032 0.635)) (stroke (width 0.4) (type default)) {NOFILL})"
        f"(polyline (pts (xy -2.032 -0.635) (xy 2.032 -0.635)) (stroke (width 0.4) (type default)) {NOFILL})",
        (0, 2.54, 270), (0, -2.54, 90))
# kolíky jsou u C_V dlouhé 1.905, aby dosáhly k deskám
lib["fcb:C_V"] = lib["fcb:C_V"].replace("(length 1.27)", "(length 1.905)")


def power(name, graphics, ang):
    base = name.split(":")[1]
    lib[name] = (f'(symbol "{name}" (power) (pin_names (offset 0) hide) (in_bom yes) (on_board yes) '
                 f'(property "Reference" "#PWR" (at 0 0 0) {FONT_HIDE})'
                 f'(property "Value" "{base}" (at 0 0 0) {FONT})'
                 f'(property "Footprint" "" (at 0 0 0) {FONT_HIDE})'
                 f'(property "Datasheet" "" (at 0 0 0) {FONT_HIDE})'
                 f'(symbol "{base}_0_1" {graphics})'
                 f'(symbol "{base}_1_1" {_pin(1, base, 0, 0, ang, length=0, typ="power_in", hide=True)}))')
    lib_pins[name] = {"1": (0, 0)}


power("fcb:GND", f"(polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27)) {STROKE} {NOFILL})", 270)
for _n in ("+3V3", "+5V", "AVDD"):
    power(f"fcb:{_n}", f"(polyline (pts (xy 0 0) (xy 0 1.27)) {STROKE} {NOFILL})(polyline (pts (xy -1.27 1.27) (xy 1.27 1.27)) {STROKE} {NOFILL})", 90)


def box(name, ref, left, right, width):
    """Obdélníkový symbol. left/right = seznam (číslo, název) shora dolů; None = mezera."""
    base = name.split(":")[1]
    rows = max(len(left), len(right))
    top = (rows - 1) / 2 * 2.54
    h2 = top + 2.54
    pins, pos = [], {}
    for side, plist in (("L", left), ("R", right)):
        for i, p in enumerate(plist):
            if p is None:
                continue
            num, pname = p
            y = top - i * 2.54
            if side == "L":
                x, ang = -(width / 2 + 2.54), 0
            else:
                x, ang = width / 2 + 2.54, 180
            pins.append(_pin(num, pname, x, y, ang))
            pos[str(num)] = (x, y)
    lib[name] = (f'(symbol "{name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes) {_props(ref, base)}'
                 f'(symbol "{base}_0_1" (rectangle (start {f(-width / 2)} {f(h2)}) (end {f(width / 2)} {f(-h2)}) {STROKE} (fill (type background))))'
                 f'(symbol "{base}_1_1" {" ".join(pins)}))')
    lib_pins[name] = pos
    return h2


# ------------------------------------------------------------------ schéma
items = []
expected = {}     # "REF.pin" -> síť
parts = {}        # REF -> hodnota a pouzdro
refcount = {}
pwr_n = [0]


def nextref(prefix):
    refcount[prefix] = refcount.get(prefix, 0) + 1
    return f"{prefix}{refcount[prefix]}"


def place(libname, x, y, ref, value, footprint="", nets=None, ref_at=(0, -3.0), val_at=(0, 3.0), hide_val=False):
    """Vloží symbol a vrátí slovník pin -> (X, Y) na listu."""
    pins = lib_pins[libname]
    pin_s = " ".join(f'(pin "{n}" (uuid {uid()}))' for n in pins)
    is_pwr = ref.startswith("#PWR")
    rx, ry = x + ref_at[0], y + ref_at[1]
    vx, vy = x + val_at[0], y + val_at[1]
    items.append(
        f'(symbol (lib_id "{libname}") (at {f(x)} {f(y)} 0) (unit 1) (in_bom {"no" if is_pwr else "yes"}) (on_board {"no" if is_pwr else "yes"}) (dnp no) (uuid {uid()})'
        f'(property "Reference" "{ref}" (at {f(rx)} {f(ry)} 0) {FONT_HIDE if is_pwr else FONT})'
        f'(property "Value" "{value}" (at {f(vx)} {f(vy)} 0) {FONT_HIDE if hide_val else FONT})'
        f'(property "Footprint" "{footprint}" (at {f(x)} {f(y)} 0) {FONT_HIDE})'
        f'(property "Datasheet" "" (at {f(x)} {f(y)} 0) {FONT_HIDE})'
        f'{pin_s}'
        f'(instances (project "{PROJECT}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1)))))')
    out = {n: (x + px, y - py) for n, (px, py) in pins.items()}
    if not is_pwr:
        parts[ref] = {"value": value, "footprint": footprint}
    if nets:
        for n, net in nets.items():
            if net is not None:
                expected[f"{ref}.{n}"] = net
    return out


def wire(*pts):
    for a, b in zip(pts, pts[1:]):
        items.append(f'(wire (pts (xy {f(a[0])} {f(a[1])}) (xy {f(b[0])} {f(b[1])})) (stroke (width 0) (type default)) (uuid {uid()}))')


def junction(p):
    items.append(f'(junction (at {f(p[0])} {f(p[1])}) (diameter 0) (color 0 0 0 0) (uuid {uid()}))')


def label(net, p, side="R"):
    ang, just = (0, "left") if side == "R" else (180, "right")
    items.append(f'(label "{net}" (at {f(p[0])} {f(p[1])} {ang}) (fields_autoplaced) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid {uid()}))')


def noconn(p):
    items.append(f'(no_connect (at {f(p[0])} {f(p[1])}) (uuid {uid()}))')


def text(s, x, y, size=2.0, bold=False):
    b = " bold" if bold else ""
    s = s.replace('"', "'").replace("\n", "\\n")
    items.append(f'(text "{s}" (at {f(x)} {f(y)} 0) (effects (font (size {size} {size}){b}) (justify left bottom)) (uuid {uid()}))')


def pwr(kind, p):
    """Napájecí symbol na bod p."""
    pwr_n[0] += 1
    val_at = (0, 3.9) if kind == "GND" else (0, -2.6)
    place(f"fcb:{kind}", p[0], p[1], f"#PWR{pwr_n[0]:03d}", kind, val_at=val_at)


def R_h(x, y, value, n1, n2):
    ref = nextref("R")
    return ref, place("fcb:R_H", x, y, ref, value, FP_R, {"1": n1, "2": n2}, ref_at=(-2.6, -2.3), val_at=(2.6, -2.3))


def R_v(x, y, value, n1, n2):
    ref = nextref("R")
    return ref, place("fcb:R_V", x, y, ref, value, FP_R, {"1": n1, "2": n2}, ref_at=(3.6, -0.6), val_at=(3.9, 1.6))


def C_v(x, y, value, n1, n2):
    ref = nextref("C")
    return ref, place("fcb:C_V", x, y, ref, value, FP_C, {"1": n1, "2": n2}, ref_at=(4.0, -0.6), val_at=(4.6, 1.6))


def box_inst(libname, x, y, ref, value, footprint, nets, lstub=5.08, rstub=5.08, title_dy=None):
    """Vloží obdélníkový symbol a ke každému pinu dá popisek sítě (nebo křížek)."""
    pins = lib_pins[libname]
    ys = [p[1] for p in pins.values()]
    top = max(ys) + 2.54
    pos = place(libname, x, y, ref, value, footprint, nets, ref_at=(0, -top - 3.6), val_at=(0, -top - 1.4))
    for n, (px, py) in pos.items():
        net = nets.get(n)
        left = pins[n][0] < 0
        if net is None:
            noconn((px, py))
        elif net in ("GND", "+3V3", "+5V", "AVDD"):
            end = (px - 2.54, py) if left else (px + 2.54, py)
            wire((px, py), end)
            label(net, end, "L" if left else "R")
        else:
            end = (px - 2.54, py) if left else (px + 2.54, py)
            wire((px, py), end)
            label(net, end, "L" if left else "R")
    return pos


# ---------------------------------------------------------------- symboly bloků
DEVKIT_L = ["3V3", "3V3", "RST", "IO4", "IO5", "IO6", "IO7", "IO15", "IO16", "IO17", "IO18", "IO8", "IO3", "IO46",
            "IO9", "IO10", "IO11", "IO12", "IO13", "IO14", "5V", "GND"]
DEVKIT_R = ["GND", "TX", "RX", "IO1", "IO2", "IO42", "IO41", "IO40", "IO39", "IO38", "IO37", "IO36", "IO35", "IO0",
            "IO45", "IO48", "IO47", "IO21", "IO20", "IO19", "GND", "GND"]
box("fcb:ESP32-S3-DevKitC-1", "U", [(i + 1, n) for i, n in enumerate(DEVKIT_L)],
    [(i + 23, n) for i, n in enumerate(DEVKIT_R)], 30.48)

MCP_L = [(21, "GPA0"), (22, "GPA1"), (23, "GPA2"), (24, "GPA3"), (25, "GPA4"), (26, "GPA5"), (27, "GPA6"), (28, "GPA7"),
         None, (12, "SCL"), (13, "SDA"), (18, "~RESET"), (9, "VDD"), (10, "VSS")]
MCP_R = [(1, "GPB0"), (2, "GPB1"), (3, "GPB2"), (4, "GPB3"), (5, "GPB4"), (6, "GPB5"), (7, "GPB6"), (8, "GPB7"),
         None, (15, "A0"), (16, "A1"), (17, "A2"), (20, "INTA"), (19, "INTB")]
box("fcb:MCP23017", "U", MCP_L, MCP_R, 25.4)

box("fcb:74HCT125", "U",
    [(2, "1A"), (1, "~1OE"), (5, "2A"), (4, "~2OE"), (9, "3A"), (10, "~3OE"), (12, "4A"), (13, "~4OE")],
    [(3, "1Y"), None, (6, "2Y"), None, (8, "3Y"), None, (11, "4Y"), (14, "VCC"), (7, "GND")], 20.32)
box("fcb:AQY212EH", "K", [(1, "A"), (2, "K")], [(4, "S1"), (3, "S2")], 15.24)
box("fcb:MCP1702-4002", "U", [(2, "VIN"), (1, "GND")], [(3, "VOUT")], 17.78)
for n in (2, 3, 4, 7, 14):
    box(f"fcb:CONN_{n}", "J", [(i + 1, str(i + 1)) for i in range(n)], [], 7.62)
box("fcb:JUMPER_3", "JP", [(1, "A"), (2, "C"), (3, "B")], [], 7.62)
box("fcb:JUMPER_2", "JP", [(1, "A"), (2, "B")], [], 7.62)
box("fcb:MOUNT", "H", [(1, "1")], [], 7.62)

HDR = "Connector_PinHeader_2.54mm:PinHeader_1x{:02d}_P2.54mm_Vertical"
HDR2 = "Connector_PinHeader_2.00mm:PinHeader_1x{:02d}_P2.00mm_Vertical"
XH4 = HDR2.format(4)      # lišty X17 a X18 mají rozteč 2,0 mm (změřeno z fotek 24. 11. 2026)

# ================================================================== zapojení
text("FCB1010-S3: nosná deska, schéma v0.1 (18. 11. 2026)", 12, 14, 3.0, True)
text("Generováno skriptem hardware/kicad/gen_sch.py. Zapojení J1 a J2 (14 vodičů) je převzaté z cizího kusu a NENÍ ověřené měřením.\n"
     "Deska se nesmí vyrábět, dokud se neověří zkouškou na drátech. Propojky JP1 a JP2 dovolují obrátit polaritu čtení spínačů.", 12, 22, 1.6)

SW_GPIO = [4, 5, 6, 7, 15, 16, 17, 18, 8, 11]          # spínače 1 až 10
gpio_net = {f"IO{g}": f"SW{i + 1}" for i, g in enumerate(SW_GPIO)}
gpio_net.update({"IO41": "SW_UP", "IO42": "SW_DOWN", "IO1": "PED_A", "IO2": "PED_B", "IO9": "AUX1", "IO10": "AUX2",
                 "IO12": "LED_DATA", "IO13": "MIDI_TX", "IO14": "MIDI_RX", "IO21": "SDA", "IO47": "SCL",
                 "IO39": "OUT1", "IO40": "OUT2", "IO0": "BOOT", "RST": "EN", "3V3": "+3V3", "5V": "+5V", "GND": "GND"})

# ---- U1 DevKit
text("ESP32-S3 DevKit (v paticích 2×22)", 62, 34, 1.8, True)
nets = {}
for i, n in enumerate(DEVKIT_L):
    nets[str(i + 1)] = gpio_net.get(n)
for i, n in enumerate(DEVKIT_R):
    nets[str(i + 23)] = gpio_net.get(n)
box_inst("fcb:ESP32-S3-DevKitC-1", 86, 72, "U1", "ESP32-S3 DevKit N16R8 (piny ověřit podle kusu)",
         "fcb1010:ESP32-S3-DevKit_2x22_RM25.4mm", nets)

# ---- U2 MCP23017
text("Expandér pro LED (I2C 0x20)", 158, 34, 1.8, True)
mcp = {"21": "LK1", "22": "LK2", "23": "LK3", "24": "LK4", "25": "LK5", "26": "LKPA", "27": "GPA6", "28": "GPA7",
       "1": "LK6", "2": "LK7", "3": "LK8", "4": "LK9", "5": "LK10", "6": "LKPB", "7": "GPB6", "8": "GPB7",
       "12": "SCL", "13": "SDA", "18": "MCP_RST", "9": "+3V3", "10": "GND", "15": "GND", "16": "GND", "17": "GND",
       "20": None, "19": None}
box_inst("fcb:MCP23017", 182, 62, "U2", "MCP23017-E/SP", "Package_DIP:DIP-28_W7.62mm_Socket", mcp)

# ---- odpory LED: síť LKn (expandér) -> LEDn_K (katoda na svazku)
text("Odpory LED (svítí při LOW)", 236, 34, 1.8, True)
led_pairs = [(f"LK{i}", f"LED{i}_K") for i in range(1, 11)] + [("LKPA", "LEDPA_K"), ("LKPB", "LEDPB_K")]
for i, (a, b) in enumerate(led_pairs):
    y = 41 + i * 6.35
    ref, p = R_h(262, y, "150", a, b)
    wire(p["1"], (p["1"][0] - 2.54, y)); label(a, (p["1"][0] - 2.54, y), "L")
    wire(p["2"], (p["2"][0] + 2.54, y)); label(b, (p["2"][0] + 2.54, y), "R")

# ---- svazky předních desek
text("Svazky předních desek (pájené, rozteč 2,0 mm)", 312, 34, 1.8, True)
j1 = ["+3V3", "+3V3", "LED5_K", "LED4_K", "LED3_K", "LED2_K", "LED1_K", "SW1_RAW", "SW2_RAW", "SW3_RAW", "SW4_RAW",
      "SW5_RAW", "SW_DOWN_RAW", "SW_COM"]
j2 = ["+3V3", "LED10_K", "LED9_K", "LED8_K", "LED7_K", "LED6_K", "SW6_RAW", "SW7_RAW", "SW8_RAW", "SW9_RAW",
      "SW10_RAW", "SW_UP_RAW", "SW_COM", None]
box_inst("fcb:CONN_14", 345, 62, "J1", "spodní přední deska", HDR2.format(14), {str(i + 1): n for i, n in enumerate(j1)})
box_inst("fcb:CONN_14", 392, 62, "J2", "horní přední deska", HDR2.format(14), {str(i + 1): n for i, n in enumerate(j2)})

# ---- 74HCT125
text("Budič 5 V: MIDI OUT a data pro WS2812B", 150, 100, 1.8, True)
hct = {"2": "MIDI_TX", "1": "GND", "3": "MIDI_OUT_5V", "5": "LED_DATA", "4": "GND", "6": "LED_DATA_5V",
       "9": "GND", "10": "+5V", "8": None, "12": "GND", "13": "+5V", "11": None, "14": "+5V", "7": "GND"}
box_inst("fcb:74HCT125", 182, 124, "U3", "SN74HCT125N", "Package_DIP:DIP-14_W7.62mm_Socket", hct)

# ---- MIDI (svazek X18 k původní destičce)
text("MIDI: původní destička (X18)", 236, 124, 1.8, True)
box_inst("fcb:CONN_4", 262, 140, "J7", "MIDI destička X18", XH4,
         {"1": "+5V", "2": "MIDI_IN_5V", "3": "MIDI_OUT_5V", "4": "GND"})
# dělič MIDI IN
x, y = 290, 136
label("MIDI_IN_5V", (x - 5.08, y), "L")
ref, p = R_h(x, y, "10k", "MIDI_IN_5V", "MIDI_RX")
wire((x - 5.08, y), p["1"])
b = (x + 7.62, y)
wire(p["2"], b, (x + 12.7, y)); label("MIDI_RX", (x + 12.7, y), "R"); junction(b)
ref, p = R_v(b[0], y + 7.62, "22k", "MIDI_RX", "GND")
wire(b, p["1"]); pwr("GND", p["2"])
# pull-up MIDI_TX (klid = log. 1, proud smyčkou neteče ani při startu)
x, y = 330, 144
ref, p = R_v(x, y, "10k", "+3V3", "MIDI_TX")
pwr("+3V3", p["1"])
wire(p["2"], (x, y + 6.35), (x + 5.08, y + 6.35)); label("MIDI_TX", (x + 5.08, y + 6.35), "R")

# ---- spínací výstupy
text("Spínací výstupy na zadní jacky (X17), plovoucí", 312, 100, 1.8, True)
for i, (o, s1, s2) in enumerate((("OUT1", "JACK_A_TIP", "JACK_A_SLEEVE"), ("OUT2", "JACK_B_TIP", "JACK_B_SLEEVE"))):
    y = 112 + i * 17
    ref, p = R_h(325, y - 1.27, "330", o, f"K{i + 1}_A")
    wire(p["1"], (p["1"][0] - 2.54, y - 1.27)); label(o, (p["1"][0] - 2.54, y - 1.27), "L")
    k = place("fcb:AQY212EH", 345, y, f"K{i + 1}", "AQY212EH", "Package_DIP:DIP-4_W7.62mm",
              {"1": f"K{i + 1}_A", "2": "GND", "4": s1, "3": s2}, ref_at=(0, -6.4), val_at=(0, 5.6))
    wire(p["2"], k["1"]); label(f"K{i + 1}_A", (p["2"][0] + 0.635, p["2"][1]), "R")
    wire(k["2"], (k["2"][0] - 2.54, k["2"][1])); label("GND", (k["2"][0] - 2.54, k["2"][1]), "L")
    for n, net in (("4", s1), ("3", s2)):
        wire(k[n], (k[n][0] + 2.54, k[n][1])); label(net, (k[n][0] + 2.54, k[n][1]), "R")
box_inst("fcb:CONN_4", 400, 120, "J11", "jacky X17", XH4,
         {"1": "JACK_A_TIP", "2": "JACK_A_SLEEVE", "3": "JACK_B_TIP", "4": "JACK_B_SLEEVE"})

# ---- ostatní konektory a propojky
text("Ostatní konektory a propojky", 12, 118, 1.8, True)
col = [
    ("fcb:CONN_4", "J5", "OLED I2C", HDR.format(4), {"1": "GND", "2": "+3V3", "3": "SCL", "4": "SDA"}),
    ("fcb:CONN_3", "J6", "WS2812B", HDR.format(3), {"1": "+5V", "2": "LED_DATA_OUT", "3": "GND"}),
    ("fcb:CONN_4", "J8", "AUX vstupy", HDR.format(4), {"1": "AUX1_RAW", "2": "AUX2_RAW", "3": "+3V3", "4": "GND"}),
    ("fcb:CONN_7", "J9", "volné", HDR.format(7), {"1": "GPA6", "2": "GPA7", "3": "GPB6", "4": "GPB7", "5": "+3V3", "6": "+5V", "7": "GND"}),
    ("fcb:CONN_3", "J12", "BOOT/RESET na panel", HDR.format(3), {"1": "BOOT", "2": "EN", "3": "GND"}),
]
y = 132
for libn, ref, val, fp, nets in col:
    n = len(nets)
    box_inst(libn, 38, y + (n - 1) * 1.27, ref, val, fp, nets)
    y += n * 2.54 + 11
col2 = [
    ("fcb:CONN_2", "J13", "LED pedálu A (X13)", HDR2.format(2), {"1": "+3V3", "2": "LEDPA_K"}),
    ("fcb:CONN_2", "J14", "LED pedálu B (X14)", HDR2.format(2), {"1": "+3V3", "2": "LEDPB_K"}),
    ("fcb:JUMPER_3", "JP1", "SW_COM: A=GND, B=3V3", HDR.format(3), {"1": "GND", "2": "SW_COM", "3": "+3V3"}),
    ("fcb:JUMPER_3", "JP2", "SW_PULL: A=3V3, B=GND", HDR.format(3), {"1": "+3V3", "2": "SW_PULL", "3": "GND"}),
    ("fcb:JUMPER_2", "JP4", "kostra - GND", HDR.format(2), {"1": "CHASSIS", "2": "GND"}),
    ("fcb:MOUNT", "H1", "úhelník 1", "fcb1010:Uhelnik", {"1": "CHASSIS"}),
    ("fcb:MOUNT", "H2", "úhelník 2", "fcb1010:Uhelnik", {"1": "CHASSIS"}),
    ("fcb:MOUNT", "H3", "úhelník 3", "fcb1010:Uhelnik", {"1": "CHASSIS"}),
]
y = 132
for libn, ref, val, fp, nets in col2:
    n = len(nets)
    box_inst(libn, 92, y + (n - 1) * 1.27, ref, val, fp, nets)
    y += n * 2.54 + 10.5

# ---- drobnosti: I2C pull-upy, reset expandéru, data WS2812B, AUX, blokovací kondenzátory
text("I2C, reset expandéru, výstup dat, AUX, blokování", 128, 154, 1.8, True)
x0, y0 = 136, 176
for i, (val, top, net) in enumerate((("4k7", "+3V3", "SDA"), ("4k7", "+3V3", "SCL"), ("10k", "+3V3", "MCP_RST"))):
    x = x0 + i * 22
    ref, p = R_v(x, y0, val, top, net)
    pwr("+3V3", p["1"])
    wire(p["2"], (x, y0 + 6.35), (x + 3.81, y0 + 6.35)); label(net, (x + 3.81, y0 + 6.35), "R")
for i, (val, a, b) in enumerate((("330", "LED_DATA_5V", "LED_DATA_OUT"), ("470", "AUX1_RAW", "AUX1"), ("470", "AUX2_RAW", "AUX2"))):
    y = 164 + i * 7.62
    ref, p = R_h(226, y, val, a, b)
    wire(p["1"], (p["1"][0] - 2.54, y)); label(a, (p["1"][0] - 2.54, y), "L")
    wire(p["2"], (p["2"][0] + 2.54, y)); label(b, (p["2"][0] + 2.54, y), "R")
for i, (val, rail) in enumerate((("100n", "+3V3"), ("100n", "+5V"), ("10u", "+3V3"), ("10u", "+5V"))):
    x = 262 + i * 14
    ref, p = C_v(x, 172, val, rail, "GND")
    pwr(rail, p["1"]); pwr("GND", p["2"])
text("U2        U3", 259, 163, 1.2)

# ---- napájení senzorů pedálů
text("Napájení senzorů pedálů (U4 volitelný, JP3 = přemostění)", 322, 154, 1.8, True)
x, y = 336, 172
ref, p = R_h(x, y, "10R", "+5V", "AVDD_IN")
wire(p["1"], (x - 7.62, y)); pwr("+5V", (x - 7.62, y))
n1 = (x + 7.62, y)
wire(p["2"], n1); junction(n1); label("AVDD_IN", (n1[0] + 1.27, y), "R")
ref, c = C_v(n1[0], y + 6.35, "10u", "AVDD_IN", "GND"); wire(n1, c["1"]); pwr("GND", c["2"])
u = place("fcb:MCP1702-4002", 366, y + 1.27, "U4", "MCP1702-4002E/TO", "Package_TO_SOT_THT:TO-92_Inline",
          {"2": "AVDD_IN", "1": "GND", "3": "AVDD"}, ref_at=(0, -7.6), val_at=(0, -5.4))
wire(n1, u["2"])
wire(u["1"], (u["1"][0] - 2.54, u["1"][1]), (u["1"][0] - 2.54, u["1"][1] + 5.08)); pwr("GND", (u["1"][0] - 2.54, u["1"][1] + 5.08))
n2 = (388, y)
wire(u["3"], n2); junction(n2)
ref, c = C_v(n2[0], y + 6.35, "10u", "AVDD", "GND"); wire(n2, c["1"]); pwr("GND", c["2"])
wire(n2, (398, y)); pwr("AVDD", (398, y))
# přemostění
jp = box_inst("fcb:JUMPER_2", 366, 191, "JP3", "bez U4: spojit", HDR.format(2), {"1": "AVDD_IN", "2": "AVDD"})

# ---- vstupy pedálů
text("Vstupy expression pedálů (svazky X21, X22, pájené, rozteč 2,0 mm; pořadí vodičů ověřit)", 128, 206, 1.8, True)
for i, ch in enumerate("AB"):
    y = 226
    x = 150 + i * 135
    box_inst("fcb:CONN_3", x - 14, y + 2.54, f"J{3 + i}", f"pedál {ch}", HDR2.format(3),
             {"1": "AVDD", "2": f"PED_{ch}_RAW", "3": "GND"})
    xa = x + 22
    label(f"PED_{ch}_RAW", (xa - 5.08, y), "L")
    ref, p = R_h(xa, y, "10k", f"PED_{ch}_RAW", f"PED_{ch}_F")
    wire((xa - 5.08, y), p["1"])
    n1 = (xa + 7.62, y); n1b = (xa + 20.32, y)
    wire(p["2"], n1, n1b); junction(n1); junction(n1b)
    label(f"PED_{ch}_F", (n1[0] + 1.27, y), "R")
    ref, r = R_v(n1[0], y + 7.62, "15k", f"PED_{ch}_F", "GND"); wire(n1, r["1"]); pwr("GND", r["2"])
    ref, c = C_v(n1b[0], y + 6.35, "470n", f"PED_{ch}_F", "GND"); wire(n1b, c["1"]); pwr("GND", c["2"])
    ref, p2 = R_h(xa + 33.02, y, "1k", f"PED_{ch}_F", f"PED_{ch}")
    wire(n1b, p2["1"])
    n2 = (xa + 40.64, y)
    wire(p2["2"], n2, (xa + 45.72, y)); junction(n2); label(f"PED_{ch}", (xa + 45.72, y), "R")
    ref, c = C_v(n2[0], y + 6.35, "100n", f"PED_{ch}", "GND"); wire(n2, c["1"]); pwr("GND", c["2"])

# ---- vstupy spínačů
text("Vstupy spínačů (12×): 47 kΩ na SW_PULL, 470 Ω do série, 100 nF na GND", 432, 34, 1.8, True)
names = [f"SW{i}" for i in range(1, 11)] + ["SW_UP", "SW_DOWN"]
for i, nm in enumerate(names):
    x = 452 + (i % 2) * 70
    y = 54 + (i // 2) * 31
    a = (x, y)
    label(f"{nm}_RAW", (x - 5.08, y), "L")
    ref, p = R_h(x + 7.62, y, "470", f"{nm}_RAW", nm)
    wire((x - 5.08, y), a, p["1"]); junction(a)
    ref, r = R_v(x, y - 7.62, "47k", "SW_PULL", f"{nm}_RAW")
    wire(a, r["2"])
    label("SW_PULL", (x, r["1"][1]), "R")
    b = (x + 15.24, y)
    wire(p["2"], b, (x + 20.32, y)); junction(b); label(nm, (x + 20.32, y), "R")
    ref, c = C_v(b[0], y + 6.35, "100n", nm, "GND"); wire(b, c["1"]); pwr("GND", c["2"])

# ------------------------------------------------------------------ zápis
out = [f'(kicad_sch (version 20230121) (generator fcb1010_gen)', f'(uuid {ROOT_UUID})', '(paper "User" 594 280)',
       '(title_block (title "FCB1010-S3 nosná deska") (date "2026-11-18") (rev "0.1") (comment 1 "Návrh, zapojení svazků neověřeno"))',
       '(lib_symbols ' + "\n".join(lib.values()) + ')']
out += items
out.append('(sheet_instances (path "/" (page "1")))')
out.append(')')
open("fcb1010-s3.kicad_sch", "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump(expected, open("expected-nets.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)
json.dump(parts, open("parts.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False, sort_keys=True)
print("symbolů:", sum(1 for i in items if i.startswith("(symbol")), "pinů s danou sítí:", len(expected))
