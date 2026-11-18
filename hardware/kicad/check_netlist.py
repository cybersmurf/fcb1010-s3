#!/usr/bin/env python3
"""Porovná netlist vyexportovaný KiCadem se zamýšleným zapojením z gen_sch.py.

Použití:
    kicad-cli sch export netlist -o fcb1010-s3.net fcb1010-s3.kicad_sch
    python3 check_netlist.py fcb1010-s3.net
Skončí chybou, pokud se některý pin liší, chybí, nebo je v netlistu navíc.
"""
import json
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "fcb1010-s3.net"
txt = open(path, encoding="utf-8").read()
expected = json.load(open("expected-nets.json", encoding="utf-8"))

actual = {}
for m in re.finditer(r'\(net \(code "?\d+"?\) \(name "([^"]*)"\)(.*?)(?=\(net \(code|\Z)', txt, re.S):
    name = m.group(1).lstrip("/")
    for ref, pin in re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', m.group(2)):
        actual[f"{ref}.{pin}"] = name

bad = 0
for k, net in sorted(expected.items()):
    got = actual.get(k)
    if got != net:
        bad += 1
        print(f"ROZDÍL {k}: má být {net!r}, v netlistu {got!r}")
for k in sorted(set(actual) - set(expected)):
    if actual[k].startswith("unconnected-"):
        continue
    bad += 1
    print(f"NAVÍC  {k}: v netlistu {actual[k]!r}, v zadání chybí")

nets = sorted(set(expected.values()))
print(f"pinů v zadání: {len(expected)}, v netlistu: {len(actual)}, sítí: {len(nets)}, rozdílů: {bad}")
sys.exit(1 if bad else 0)
