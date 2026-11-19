#!/usr/bin/python3
"""Načte výsledek autorouteru (fcb1010-s3.ses) do desky a vypíše, co zůstalo nezapojené.

Postup:
    /usr/bin/python3 gen_pcb.py --dsn
    java -jar freerouting.jar -de fcb1010-s3.dsn -do fcb1010-s3.ses -mp 20
    /usr/bin/python3 import_ses.py        (natáhne spoje, rozlije zem, pustí kontrolu pravidel -> drc.rpt)
KiCad 7 umí soubor .ses načíst jen z okna editoru, proto ho tady čteme sami.
"""
import os
import re

import pcbnew
from pcbnew import FromMM, VECTOR2I

HERE = os.path.dirname(os.path.abspath(__file__))
pcb = os.path.join(HERE, "fcb1010-s3.kicad_pcb")
board = pcbnew.LoadBoard(pcb)
for t in list(board.GetTracks()):
    board.Remove(t)

txt = open(os.path.join(HERE, "fcb1010-s3.ses"), encoding="utf-8").read()
tokens = re.findall(r'"[^"]*"|[()]|[^\s()]+', txt[txt.index("(network_out"):])


def parse(pos):
    out = []
    while pos < len(tokens):
        t = tokens[pos]
        if t == "(":
            sub, pos = parse(pos + 1)
            out.append(sub)
        elif t == ")":
            return out, pos + 1
        else:
            out.append(t.strip('"'))
            pos += 1
    return out, pos


tree, _ = parse(0)
network = tree[0]
UNIT = 10000.0          # (resolution um 10)
layers = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
segs = vias = 0
for net in network[1:]:
    if not isinstance(net, list) or net[0] != "net":
        continue
    ninfo = board.FindNet(net[1])
    assert ninfo is not None, net[1]
    for item in net[2:]:
        if item[0] == "wire":
            path = item[1]
            layer, width = layers[path[1]], float(path[2]) / UNIT
            pts = [float(v) for v in path[3:]]
            xy = [(pts[i] / UNIT, -pts[i + 1] / UNIT) for i in range(0, len(pts), 2)]
            for a, b in zip(xy, xy[1:]):
                if a == b:
                    continue
                tr = pcbnew.PCB_TRACK(board)
                tr.SetStart(VECTOR2I(FromMM(a[0]), FromMM(a[1])))
                tr.SetEnd(VECTOR2I(FromMM(b[0]), FromMM(b[1])))
                tr.SetWidth(FromMM(width))
                tr.SetLayer(layer)
                tr.SetNet(ninfo)
                board.Add(tr)
                segs += 1
        elif item[0] == "via":
            m = re.match(r"Via\[0-1\]_(\d+):(\d+)_um", item[1])
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(VECTOR2I(FromMM(float(item[2]) / UNIT), FromMM(-float(item[3]) / UNIT)))
            v.SetWidth(FromMM(int(m.group(1)) / 1000))
            v.SetDrill(FromMM(int(m.group(2)) / 1000))
            v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
            v.SetNet(ninfo)
            board.Add(v)
            vias += 1

# rozlitá zem na obou vrstvách
for z in list(board.Zones()):
    board.Remove(z)
bb = board.GetBoardEdgesBoundingBox()
gnd = board.FindNet("GND")
for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(gnd)
    z.SetLocalClearance(FromMM(0.3))
    z.SetMinThickness(FromMM(0.25))
    z.SetThermalReliefGap(FromMM(0.3))
    z.SetThermalReliefSpokeWidth(FromMM(0.5))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline()
    o.NewOutline()
    for x, y in ((bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()), (bb.GetRight(), bb.GetBottom()), (bb.GetLeft(), bb.GetBottom())):
        o.Append(x, y)
    board.Add(z)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())

board.BuildConnectivity()
conn = board.GetConnectivity()
length = sum(pcbnew.ToMM(t.GetLength()) for t in board.GetTracks() if t.Type() != pcbnew.PCB_VIA_T)
print(f"segmentů: {segs}, prokovů: {vias}, délka spojů: {length:.0f} mm")
print("nezapojených spojení:", conn.GetUnconnectedCount(False))
pcbnew.SaveBoard(pcb, board)
rpt = os.path.join(HERE, "drc.rpt")
pcbnew.WriteDRCReport(board, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
txt = open(rpt, encoding="utf-8").read()
kinds = {}
for m in re.finditer(r"^\[(\w+)\]", txt, re.M):
    kinds[m.group(1)] = kinds.get(m.group(1), 0) + 1
print("DRC:", kinds or "bez nálezů")
