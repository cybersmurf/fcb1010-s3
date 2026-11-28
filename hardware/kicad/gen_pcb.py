#!/usr/bin/python3
"""Návrh desky FCB1010-S3: rozmístění součástek podle parts.json a expected-nets.json.

Spouští se systémovým Pythonem s modulem pcbnew (KiCad 7):
    /usr/bin/python3 gen_pcb.py            -> fcb1010-s3.kicad_pcb (nezapojeno, jen rozmístění a sítě)
Souřadnice v mm: počátek je roh desky u displeje na straně úhelníků, pohled ze strany součástek,
x roste ke stabilizátoru, y od hrany s úhelníky k hraně se svazky.
"""
import json
import os
import sys

import pcbnew
from pcbnew import FromMM, ToMM, VECTOR2I

HERE = os.path.dirname(os.path.abspath(__file__))
LIBS = "/usr/share/kicad/footprints"
OWN = os.path.join(HERE, "fcb1010.pretty")
BX, BY = 40.0, 60.0            # posun desky na listu
L, W = 229.0, 41.0
POWER = {"GND": 0.6, "+5V": 0.6, "AVDD": 0.4, "AVDD_IN": 0.4, "+3V3": 0.4}   # širší spoje, mm
EDGE_GAP = 0.6                 # nejmenší vzdálenost spoje od hrany desky

parts = json.load(open(os.path.join(HERE, "parts.json"), encoding="utf-8"))
expected = json.load(open(os.path.join(HERE, "expected-nets.json"), encoding="utf-8"))
nets_of = {}
for k, net in expected.items():
    ref, pin = k.split(".")
    nets_of.setdefault(ref, {})[pin] = net


def find2(a, b, kind="R"):
    """Dvoupólová součástka (R nebo C) mezi sítěmi a (pin 1) a b (pin 2)."""
    hit = [r for r, p in nets_of.items() if r[0] == kind and p.get("1") == a and p.get("2") == b]
    assert len(hit) == 1, (a, b, hit)
    return hit[0]


# ------------------------------------------------------------------ vlastní pouzdra
os.makedirs(OWN, exist_ok=True)


def write_fp(name, body):
    open(os.path.join(OWN, name + ".kicad_mod"), "w", encoding="utf-8").write(
        f'(footprint "{name}" (version 20221018) (generator fcb1010_gen) (layer "F.Cu")\n  (attr through_hole)\n{body})\n')


TXT = '(effects (font (size 1 1) (thickness 0.15)))'
pads = []
for i in range(22):
    x = -26.67 + i * 2.54
    shape = "rect" if i == 0 else "circle"
    pads.append(f'  (pad "{i + 1}" thru_hole {shape} (at {x:.2f} 12.7) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask"))')
    pads.append(f'  (pad "{i + 23}" thru_hole circle (at {x:.2f} -12.7) (size 1.7 1.7) (drill 1.0) (layers "*.Cu" "*.Mask"))')
write_fp("ESP32-S3-DevKit_2x22_RM25.4mm",
         f'  (fp_text reference "REF**" (at -20 0) (layer "F.SilkS") {TXT})\n'
         f'  (fp_text value "ESP32-S3-DevKit" (at 4 0) (layer "F.Fab") {TXT})\n'
         '  (fp_rect (start -32 -14) (end 32 14) (stroke (width 0.15) (type solid)) (fill none) (layer "F.SilkS"))\n'
         '  (fp_rect (start -32.3 -14.3) (end 32.3 14.3) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))\n'
         '  (fp_text user "USB" (at 29 0 90) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
         '  (fp_text user "ANT" (at -29.5 0 90) (layer "F.SilkS") (effects (font (size 1 1) (thickness 0.15))))\n'
         + "\n".join(pads) + "\n")
write_fp("Uhelnik",
         f'  (fp_text reference "REF**" (at 0 3.2) (layer "F.SilkS") {TXT})\n'
         f'  (fp_text value "uhelnik" (at 0 -3.2) (layer "F.Fab") {TXT})\n'
         '  (fp_rect (start -4.3 -2) (end 4.3 2) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))\n'
         '  (pad "1" thru_hole oval (at -2.9 0) (size 2.0 3.4) (drill oval 1.3 2.1) (layers "*.Cu" "*.Mask"))\n'
         '  (pad "1" thru_hole oval (at 2.9 0) (size 2.0 3.4) (drill oval 1.3 2.1) (layers "*.Cu" "*.Mask"))\n')

# ------------------------------------------------------------------ rozmístění
PL = {}   # ref -> (x, y, natočení ve stupních)


def put(ref, x, y, rot=0):
    assert ref in parts, ref
    assert ref not in PL, ref
    PL[ref] = (x, y, rot)


def vert(a, b, x, y_a, y_b, kind="R"):
    """Dvoupólová součástka svisle: pin se sítí a na y_a, pin se sítí b na y_b."""
    ref = find2(a, b, kind)
    put(ref, x, y_a, -90 if y_b > y_a else 90)


def horiz(a, b, x_a, x_b, y):
    ref = find2(a, b)
    put(ref, x_a, y, 0 if x_b > x_a else 180)


# svazky předních desek; pin 1 (červený vodič) je na konci dál od displeje, stejně jako na původní desce (IMG_9456)
# polohy podle fotek strany součástek s metrem zaháknutým za hranu desky (IMG_9526 až IMG_9549):
# pouzdra X20 12,5 až 42,5 mm, X19 46,5 až 76,2 mm, X22 83 až 91 mm, X21 94,5 až 102,5 mm od hrany u displeje
put("J1", 40.3, 38.5, -90)
put("J2", 74.3, 38.5, -90)
# pedály
put("J4", 89.0, 38.5, -90)
put("J3", 100.5, 38.5, -90)
# LED pedálů a displej
put("J13", 3.0, 21.0, 0)
put("J14", 3.0, 28.0, 0)
put("J5", 8.4, 9.0, 0)

# vstupy spínačů: sloupce nad svazkem, shora kondenzátor, 470 Ω, 47 kΩ
for names, x0 in ((["SW1", "SW2", "SW3", "SW4", "SW5", "SW_DOWN"], 21.0), (["SW6", "SW7", "SW8", "SW9", "SW10", "SW_UP"], 54.0)):
    for i, nm in enumerate(names):
        x = x0 + i * 3.0
        vert(nm, "GND", x, 8.2, 3.2, "C")
        vert(f"{nm}_RAW", nm, x, 20.76, 10.6)
        vert("SW_PULL", f"{nm}_RAW", x, 33.26, 23.1)
# odpory LED
for leds, x0 in (([5, 4, 3, 2, 1], 12.0), ([10, 9, 8, 7, 6], 45.0)):
    for i, n in enumerate(leds):
        x = x0 + (i // 2) * 3.0
        y = 3.5 if i % 2 == 0 else 16.0
        vert(f"LK{n}", f"LED{n}_K", x, y, y + 10.16)
vert("LKPA", "LEDPA_K", 18.0, 16.0, 26.16)
vert("LKPB", "LEDPB_K", 51.0, 16.0, 26.16)

# expandér a drobné konektory nad ním
put("U2", 75.0, 17.8, 90)
put("J6", 76.0, 3.5, 90)
put("J8", 86.0, 3.5, 90)
put("J12", 98.0, 3.5, 90)

# vstupy pedálů pod expandérem
vert("PED_B_RAW", "PED_B_F", 74.0, 33.16, 23.0)
vert("PED_B_F", "GND", 77.0, 23.0, 33.16)
vert("PED_B_F", "PED_B", 87.6, 33.16, 23.0)
vert("PED_A_RAW", "PED_A_F", 98.0, 33.16, 23.0)
vert("PED_A_F", "GND", 101.0, 23.0, 33.16)
vert("PED_A_F", "PED_A", 104.0, 33.16, 23.0)

# napájení senzorů
put("U4", 111.7, 18.5, 0)
vert("+5V", "AVDD_IN", 110.8, 23.0, 33.16)

# budič a MIDI
put("U3", 119.5, 17.62, 90)
put("J7", 137.0, 38.5, -90)      # X18: střed pouzdra asi 134 mm
vert("MIDI_IN_5V", "MIDI_RX", 120.5, 33.66, 23.5)
vert("MIDI_RX", "GND", 123.5, 23.5, 33.66)
vert("+3V3", "MIDI_TX", 133.6, 21.5, 31.66)

# DevKit a věci pod ním
put("U1", 168.67, 18.5, 0)
# Pod DevKitem nesmí být nic: JP1 a JP2 jsou nad budičem U3, JP3 u stabilizátoru senzorů, JP4 a J9
# na konci desky u výstupů, odpory a kondenzátory ve dvou řadách mezi DevKitem a hranou se svazky.
put("JP1", 121.5, 3.5, 90)
put("JP2", 129.5, 3.5, 90)
put("JP3", 129.5, 26.5, 0)          # u stabilizátoru senzorů
put("JP4", 221.0, 9.0, 0)
put("J9", 212.0, 30.5, 90)
horiz("+3V3", "SDA", 141.0, 151.16, 35.0)
horiz("+3V3", "SCL", 153.6, 163.76, 35.0)
horiz("+3V3", "MCP_RST", 166.2, 176.36, 35.0)
horiz("LED_DATA_5V", "LED_DATA_OUT", 178.8, 188.96, 35.0)
horiz("AUX1_RAW", "AUX1", 149.0, 159.16, 38.6)
horiz("AUX2_RAW", "AUX2", 161.6, 171.76, 38.6)

# spínací výstupy
# výstupy (piny 3, 4) míří doleva ke konektoru J11, vstupy doprava
put("K1", 212.62, 24.54, 180)
put("K2", 224.62, 24.54, 180)
vert("OUT1", "K1_A", 215.0, 8.5, 18.66)
vert("OUT2", "K2_A", 227.0, 8.5, 18.66)
put("J11", 210.3, 38.5, -90)    # X17: střed pouzdra asi 207 mm

# úhelníky
put("H1", 4.4, 4.0, 0)
put("H2", 115.2, 4.0, 0)
put("H3", 211.8, 4.0, 0)

# kondenzátory, které find2 nerozliší (více kusů mezi stejnými sítěmi), ručně podle hodnoty
caps = {}
for r, p in nets_of.items():
    if r[0] == "C":
        caps.setdefault((parts[r]["value"], p["1"], p["2"]), []).append(r)
for key, refs in caps.items():
    refs.sort(key=lambda r: int(r[1:]))


def cap(value, a, x, y, rot, idx=0):
    put(caps[(value, a, "GND")][idx], x, y, rot)


cap("100n", "+3V3", 111.3, 9.0, -90)            # C1 u U2
cap("100n", "+5V", 126.5, 22.0, 0)             # C2 u U3
cap("10u", "+3V3", 141.0, 38.6, 0)
cap("10u", "+5V", 191.8, 35.0, 0)
cap("10u", "AVDD_IN", 114.0, 23.0, -90)
cap("10u", "AVDD", 117.0, 23.0, -90)
cap("470n", "PED_B_F", 80.6, 23.0, -90)
cap("100n", "PED_B", 84.2, 23.0, -90)
cap("470n", "PED_A_F", 107.0, 23.0, -90)
cap("100n", "PED_A", 107.0, 30.2, -90)

missing = sorted(set(parts) - set(PL))
assert not missing, f"nerozmístěno: {missing}"

# ------------------------------------------------------------------ deska
board = pcbnew.BOARD()
ds = board.GetDesignSettings()
nc = ds.m_NetSettings.m_DefaultNetClass
nc.SetClearance(FromMM(0.2))
nc.SetTrackWidth(FromMM(0.3))
nc.SetViaDiameter(FromMM(0.8))
nc.SetViaDrill(FromMM(0.4))


def P(x, y):
    return VECTOR2I(FromMM(BX + x), FromMM(BY + y))


edge = pcbnew.PCB_SHAPE(board)
edge.SetShape(pcbnew.SHAPE_T_RECT)
edge.SetStart(P(0, 0))
edge.SetEnd(P(L, W))
edge.SetLayer(pcbnew.Edge_Cuts)
edge.SetWidth(FromMM(0.1))
board.Add(edge)

netobj = {}
for net in sorted(set(expected.values())):
    n = pcbnew.NETINFO_ITEM(board, net)
    board.Add(n)
    netobj[net] = n

fps = {}
for ref, (x, y, rot) in sorted(PL.items()):
    lib, name = parts[ref]["footprint"].split(":")
    libdir = OWN if lib == "fcb1010" else os.path.join(LIBS, lib + ".pretty")
    fp = pcbnew.FootprintLoad(libdir, name)
    assert fp is not None, (ref, lib, name)
    fp.SetReference(ref)
    fp.SetValue(parts[ref]["value"])
    fp.SetPosition(P(x, y))
    fp.SetOrientationDegrees(rot)
    for pad in fp.Pads():
        net = nets_of.get(ref, {}).get(pad.GetNumber())
        if net:
            pad.SetNet(netobj[net])
    board.Add(fp)
    fps[ref] = fp

# středicí otvory u displeje
for i, (x, y) in enumerate(((9.6, 2.6), (2.0, 35.5))):
    fp = pcbnew.FootprintLoad(os.path.join(LIBS, "MountingHole.pretty"), "MountingHole_2.2mm_M2")
    fp.SetReference(f"MH{i + 1}")
    fp.Reference().SetVisible(False)
    fp.SetPosition(P(x, y))
    board.Add(fp)

# ------------------------------------------------------------------ popisky na potisku
def label(text, x, y, size=0.8, rot=0):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetLayer(pcbnew.F_SilkS)
    t.SetPosition(P(x, y))
    t.SetTextSize(VECTOR2I(FromMM(size), FromMM(size)))
    t.SetTextThickness(FromMM(size * 0.15))
    t.SetTextAngleDegrees(rot)
    board.Add(t)


label("SW 1-5 DOWN", 27.3, 40.3)
label("SW 6-10 UP", 61.3, 40.3)
label("PED B", 87.0, 36.4, 0.8)
label("PED A", 98.5, 36.4, 0.8)
label("MIDI X18", 134.0, 36.4)
label("JACK X17", 207.3, 36.4)
label("WS2812", 78.5, 1.2)
label("AUX", 88.5, 1.2)
label("BOOT RST", 100.5, 1.2)
label("OLED", 8.4, 18.6)
label("LED A", 3.4, 19.2)
label("LED B", 3.4, 31.2)
label("FCB1010-S3 v0.3", 190.0, 2.0, 1.2)
label("cybersmurf/fcb1010-s3", 190.0, 4.2, 0.8)

# ------------------------------------------------------------------ kontrola překryvů
def bbox(fp):
    xs, ys = [], []
    for pad in fp.Pads():
        b = pad.GetBoundingBox()
        xs += [ToMM(b.GetLeft()) - BX, ToMM(b.GetRight()) - BX]
        ys += [ToMM(b.GetTop()) - BY, ToMM(b.GetBottom()) - BY]
    return min(xs), min(ys), max(xs), max(ys)


boxes = {r: bbox(fp) for r, fp in fps.items()}
problems = 0
refs = sorted(boxes)
SKIP_UNDER = set()                      # pod DevKitem nesmí být nic
for i, a in enumerate(refs):
    ax0, ay0, ax1, ay1 = boxes[a]
    if ax0 < 0.3 or ay0 < 0.3 or ax1 > L - 0.3 or ay1 > W - 0.3:
        print(f"MIMO DESKU {a}: {ax0:.1f},{ay0:.1f} .. {ax1:.1f},{ay1:.1f}")
        problems += 1
    for b in refs[i + 1:]:
        if a in SKIP_UNDER or b in SKIP_UNDER:
            continue
        bx0, by0, bx1, by1 = boxes[b]
        m = 0.35
        if ax0 - m < bx1 and bx0 - m < ax1 and ay0 - m < by1 and by0 - m < ay1:
            print(f"PŘEKRYV {a} ({ax0:.1f},{ay0:.1f}..{ax1:.1f},{ay1:.1f}) × {b} ({bx0:.1f},{by0:.1f}..{bx1:.1f},{by1:.1f})")
            problems += 1
# pájecí body DevKitu nesmí kolidovat s ničím
u1 = fps["U1"]
for pad in u1.Pads():
    px, py = ToMM(pad.GetPosition().x) - BX, ToMM(pad.GetPosition().y) - BY
    for b in refs:
        if b == "U1":
            continue
        bx0, by0, bx1, by1 = boxes[b]
        if bx0 - 1.3 < px < bx1 + 1.3 and by0 - 1.3 < py < by1 + 1.3:
            print(f"PŘEKRYV pin U1.{pad.GetNumber()} ({px:.1f},{py:.1f}) × {b}")
            problems += 1

out = os.path.join(HERE, "fcb1010-s3.kicad_pcb")
pcbnew.SaveBoard(out, board)
print(f"součástek: {len(fps)}, sítí: {len(netobj)}, problémů rozmístění: {problems}")
if "--dsn" in sys.argv:
    dsn = os.path.join(HERE, "fcb1010-s3.dsn")
    ok = pcbnew.ExportSpecctraDSN(board, dsn)
    # Úprava zadání pro autorouter: napájecí sítě širší a hranice pro spoje 0,6 mm od okraje desky.
    import re
    t = open(dsn, encoding="utf-8").read()
    x0, x1, y0, y1 = (BX + EDGE_GAP) * 1000, (BX + L - EDGE_GAP) * 1000, (BY + EDGE_GAP) * 1000, (BY + W - EDGE_GAP) * 1000
    t, n = re.subn(r"\(boundary\s*\(path pcb 0[^)]*\)\s*\)",
                   f"(boundary\n      (path pcb 0  {x1:.0f} -{y1:.0f}  {x0:.0f} -{y1:.0f}  {x0:.0f} -{y0:.0f}  {x1:.0f} -{y0:.0f}  {x1:.0f} -{y1:.0f})\n    )", t)
    assert n == 1
    m = re.search(r"\(class kicad_default \"\"(.*?)\(circuit", t, re.S)
    names = m.group(1).split()
    rest = [x for x in names if x not in POWER]
    cls = lambda nm, nets, w: (f'(class {nm} ' + " ".join(nets) + f'\n      (circuit\n        (use_via Via[0-1]_800:400_um)\n      )\n'
                               f'      (rule\n        (width {w})\n        (clearance 200.1)\n      )\n    )')
    t, n = re.subn(r"\(class kicad_default.*?\n    \)", lambda _: "\n    ".join([cls("kicad_default", rest, 300)] + [cls(f"power{int(w * 1000)}", [x for x in names if POWER.get(x) == w], int(w * 1000)) for w in sorted(set(POWER.values()))]), t, flags=re.S)
    assert n == 1
    open(dsn, "w", encoding="utf-8").write(t)
    print("DSN:", ok)
