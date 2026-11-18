#!/usr/bin/python3
"""Geometrická kontrola desky: pro každou síť spočítá, jestli jsou všechny pájecí body propojené spoji.

KiCad 7 neumí DRC z příkazové řádky, tohle je nezávislá náhrada pro kontrolu propojení.
"""
import os
import sys
import pcbnew
from pcbnew import ToMM

HERE = os.path.dirname(os.path.abspath(__file__))
b = pcbnew.LoadBoard(os.path.join(HERE, "fcb1010-s3.kicad_pcb"))


def dist_pt_seg(p, a, c):
    (px, py), (ax, ay), (cx, cy) = p, a, c
    dx, dy = cx - ax, cy - ay
    L2 = dx * dx + dy * dy
    t = 0 if L2 == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2))
    qx, qy = ax + t * dx, ay + t * dy
    return ((px - qx) ** 2 + (py - qy) ** 2) ** 0.5


bad = 0
total_nets = 0
for code in range(1, b.GetNetCount()):
    net = b.FindNet(code)
    if net is None:
        continue
    pads = [p for p in b.GetPads() if p.GetNetCode() == code]
    if len(pads) < 2:
        continue
    total_nets += 1
    segs, vias = [], []
    for t in b.GetTracks():
        if t.GetNetCode() != code:
            continue
        if t.Type() == pcbnew.PCB_VIA_T:
            vias.append((ToMM(t.GetPosition().x), ToMM(t.GetPosition().y), ToMM(t.GetWidth()) / 2))
        else:
            segs.append(((ToMM(t.GetStart().x), ToMM(t.GetStart().y)), (ToMM(t.GetEnd().x), ToMM(t.GetEnd().y)), t.GetLayer(), ToMM(t.GetWidth()) / 2))
    n = len(pads) + len(segs) + len(vias)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    P, S, V = 0, len(pads), len(pads) + len(segs)
    padbox = []
    for p in pads:
        bb = p.GetBoundingBox()
        padbox.append((ToMM(bb.GetLeft()), ToMM(bb.GetTop()), ToMM(bb.GetRight()), ToMM(bb.GetBottom())))
    for i, (a, c, layer, hw) in enumerate(segs):
        for j, (x0, y0, x1, y1) in enumerate(padbox):
            for pt in (a, c):
                if x0 - 0.01 <= pt[0] <= x1 + 0.01 and y0 - 0.01 <= pt[1] <= y1 + 0.01:
                    union(S + i, P + j)
        for k in range(i + 1, len(segs)):
            a2, c2, layer2, hw2 = segs[k]
            if layer2 != layer:
                continue
            tol = hw + hw2
            if min(dist_pt_seg(a, a2, c2), dist_pt_seg(c, a2, c2), dist_pt_seg(a2, a, c), dist_pt_seg(c2, a, c)) <= tol * 0.5:
                union(S + i, S + k)
        for k, (vx, vy, vr) in enumerate(vias):
            if dist_pt_seg((vx, vy), a, c) <= vr:
                union(S + i, V + k)
    for k, (vx, vy, vr) in enumerate(vias):
        for j, (x0, y0, x1, y1) in enumerate(padbox):
            if x0 <= vx <= x1 and y0 <= vy <= y1:
                union(V + k, P + j)
    groups = {}
    for j, p in enumerate(pads):
        groups.setdefault(find(P + j), []).append(f"{p.GetParent().GetReference()}.{p.GetNumber()}")
    if len(groups) > 1:
        bad += 1
        print(f"NEPROPOJENO {net.GetNetname()}: {sorted(groups.values(), key=len)}")
print(f"sítí s více pájecími body: {total_nets}, nepropojených: {bad}")
sys.exit(1 if bad else 0)
