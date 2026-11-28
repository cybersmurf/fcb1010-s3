"""Schéma opakovaných obvodů nosné desky FCB1010-S3 (návrh, hodnoty podle docs/obvody.md a docs/pinout.md).

Spuštění: python3 obvody.py  ->  ../schema-obvodu.png a .svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import schemdraw.logic as logic

schemdraw.config(fontsize=10, lw=1.4)
fig, axes = plt.subplots(2, 3, figsize=(16, 9.2))
axes = axes.ravel()


def start(ax, title):
    ax.set_title(title, fontsize=11, fontweight="bold", loc="left", pad=16)
    return schemdraw.Drawing(canvas=ax)


# 1 --------------------------------------------------------------- vstup spínače
d = start(axes[0], "1  Vstup spínače (12×)")
d += elm.Dot(open=True).label("svazek X19/X20\nspínač + dioda\nproti GND", loc="left")
d += elm.Line().right().length(1.2)
d += (n1 := elm.Dot())
d += elm.Resistor().up().label("47 kΩ")
d += elm.Vdd().label("3V3")
d += elm.Resistor().right().at(n1.center).label("470 Ω")
d += (n2 := elm.Dot())
d += elm.Capacitor().down().label("100 nF")
d += elm.Ground()
d += elm.Line().right().at(n2.center).length(1.2)
d += elm.Dot(open=True).label("GPIO", loc="right")
d.draw(show=False)

# 2 --------------------------------------------------------------- vstup pedálu
d = start(axes[1], "2  Vstup expression pedálu (2×)")
d += elm.Dot(open=True).label("X21/X22\nsignál\nsenzoru", loc="left")
d += elm.Resistor().right().label("10 kΩ")
d += (n1 := elm.Dot())
d += elm.Resistor().down().label("15 kΩ")
d += elm.Ground()
d += elm.Line().right().at(n1.center).length(2.4)
d += (n1b := elm.Dot())
d += elm.Capacitor().down().label("470 nF", loc="bottom")
d += elm.Ground()
d += elm.Resistor().right().at(n1b.center).label("1 kΩ")
d += (n2 := elm.Dot())
d += elm.Capacitor().down().label("100 nF", loc="bottom")
d += elm.Ground()
d += elm.Line().right().at(n2.center).length(1.0)
d += elm.Dot(open=True).label("GPIO1 / 2\n(ADC)", loc="right")
d.draw(show=False)

# 3 --------------------------------------------------------------- původní LED
d = start(axes[2], "3  Původní LED přes MCP23017 (10 + 2×)")
d += elm.Vdd().label("3V3")
d += elm.Line().down().length(0.8)
d += elm.LED().down().label("LED na\npřední desce", loc="bottom")
d += elm.Resistor().down().label("150 Ω", loc="bottom")
d += elm.Line().right().length(1.5)
d += elm.Dot(open=True).label("MCP23017\nGPA / GPB\n(svítí při LOW)", loc="right")
d.draw(show=False)

# 4 --------------------------------------------------------------- MIDI IN
d = start(axes[3], "4  MIDI IN (optočlen je na původní destičce)")
d += elm.Dot(open=True).label("X18\nvýstup\nH11L1", loc="left")
d += elm.Line().right().length(1.2)
d += (n0 := elm.Dot())
d += elm.Resistor().up().label("R6 4,7 kΩ\n(na destičce)")
d += elm.Vdd().label("5 V")
d += elm.Resistor().right().at(n0.center).label("10 kΩ")
d += (n1 := elm.Dot())
d += elm.Resistor().down().label("22 kΩ")
d += elm.Ground()
d += elm.Line().right().at(n1.center).length(1.2)
d += elm.Dot(open=True).label("GPIO14\n3,0 V v klidu", loc="right")
d.draw(show=False)

# 5 --------------------------------------------------------------- MIDI OUT
d = start(axes[4], "5  MIDI OUT (odpory 220 Ω jsou na destičce)")
d += elm.Dot(open=True).label("GPIO13\n(3,3 V)", loc="left")
d += elm.Line().right().length(1.0)
d += logic.Buf().label("74HCT125\nnapájení 5 V", loc="bottom")
d += elm.Line().right().length(1.0)
d += elm.Dot(open=True).label("X18\nMIDI OUT\n(5 V)", loc="right")
d.draw(show=False)

# 6 --------------------------------------------------------------- spínací výstup
d = start(axes[5], "6  Spínací výstup na zadní jack (2×)")
d += elm.Dot(open=True).label("GPIO39 / 40", loc="left")
d += elm.Resistor().right().label("330 Ω")
d += (oc := elm.Optocoupler().anchor("anode").label("AQY212EH\n(PhotoMOS)", loc="bottom"))
d += elm.Ground().at(oc.cathode)
d += elm.Line().right().at(oc.collector).length(1.2)
d += elm.Dot(open=True).label("X17 a", loc="right")
d += elm.Line().right().at(oc.emitter).length(1.2)
d += elm.Dot(open=True).label("X17 b\n(plovoucí kontakt)", loc="right")
d.draw(show=False)

for ax in axes:
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ax.set_xlim(cx - 6.6, cx + 6.6)
    ax.set_ylim(cy - 4.1, cy + 4.1)
    ax.set_aspect("equal")
    ax.axis("off")
fig.suptitle("FCB1010-S3: opakované obvody nosné desky, návrh v0.1 (18. 11. 2026). Zapojení X18 a X17 čeká na potvrzení měřením.",
             fontsize=10, x=0.01, ha="left", color="#444")
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig("../schema-obvodu.png", dpi=150)
fig.savefig("../schema-obvodu.svg")
print("ok")
