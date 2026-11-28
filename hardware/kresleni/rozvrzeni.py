"""Rozvržení nosné desky FCB1010-S3, verze 0.1 (návrh k připomínkám).

Souřadnice v mm. Počátek je roh u displeje na straně úhelníků:
x roste podél desky směrem ke stabilizátoru, y od hrany s úhelníky k hraně se svazky.
Spuštění: python3 rozvrzeni.py  ->  ../rozvrzeni-desky.png a .svg
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

L, W = 229.0, 41.0                      # změřeno
BRACKETS = [(4.4, 0.7), (115.2, 0.7), (211.8, 0.7)]   # střed x, nejistota; z otisku na čtverečkovaném papíře
HOLES = [(9.6, 2.6), (2.0, 35.5)]       # kulaté otvory u displeje
WIN = (27.0, 12.5, 36.0, 18.5)          # původní okénko displeje: střed x, y, šířka, výška
OLED_ACTIVE = (55.0, 27.5)              # obraz OLED 2,42"
LED_GROUPS = [(56.5, 111.0, 4, "4 zelené"), (115.5, 196.0, 5, "5 zelených"), (199.0, 222.5, 2, "2 červené")]

# pájecí řady svazků na hraně se svazky (střed x, počet pinů, rozteč, název)
HARNESS = [
    (24.3, 14, 2.0, "X20\n14 vodičů\npřední deska"),
    (57.0, 14, 2.0, "X19\n14 vodičů\npřední deska"),
    (82.0, 3, 2.0, "X22\npedál"),
    (93.0, 3, 2.0, "X21\npedál"),
    (129.0, 4, 2.5, "X18\nMIDI\n(lišta)"),
    (205.5, 4, 2.5, "X17\njacky\n(lišta)"),
]

C_BOARD, C_EDGE = "#e8f0ea", "#2d5a3d"
C_UNSURE = "#c0392b"


def board(ax, title):
    ax.add_patch(Rectangle((0, 0), L, W, fc=C_BOARD, ec=C_EDGE, lw=1.6, zorder=1))
    ax.set_xlim(-12, L + 12)
    ax.set_ylim(W + 21, -15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(-12, -11, title, fontsize=11, fontweight="bold", va="top")


def part(ax, x, y, w, h, label, fc="#ffffff", ec="#333333", fs=6.5, ls="-", z=3, rot=0):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=0.9, ls=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=z + 1, rotation=rot)


def dim(ax, x0, x1, y, text, fs=6.5):
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#555"))
    ax.text((x0 + x1) / 2, y - 1.0, text, ha="center", va="bottom", fontsize=fs, color="#333")


def mounting(ax, mirror=False):
    mx = (lambda x: L - x) if mirror else (lambda x: x)
    for i, (x, tol) in enumerate(BRACKETS, 1):
        ax.add_patch(FancyBboxPatch((mx(x) - 3 - tol, 0.8), 6 + 2 * tol, 5.4, boxstyle="round,pad=0.2",
                                    fc="#f6d7d2", ec=C_UNSURE, lw=0.8, zorder=4))
        ax.text(mx(x), 3.5, f"Ú{i}", ha="center", va="center", fontsize=6, color=C_UNSURE, zorder=5)
        ax.text(mx(x), -1.2, f"{x:g} ±{tol:g}", ha="center", va="bottom", fontsize=5.8, color=C_UNSURE)
    for x, y in HOLES:
        ax.add_patch(Circle((mx(x), y), 1.1, fc="white", ec=C_EDGE, lw=0.8, zorder=5))


fig, (a, b) = plt.subplots(2, 1, figsize=(15, 9.0))

# ---------------------------------------------------------------- strana součástek
board(a, "A  Strana součástek (dovnitř přístroje). Hrana s úhelníky nahoře, konec u displeje vlevo.")
mounting(a)
dim(a, 0, L, -6.5, "229 mm (změřeno)")
a.annotate("", (L + 5, 0), (L + 5, W), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#555"))
a.text(L + 6.5, W / 2, "41", fontsize=6.5, va="center")

for x, n, pitch, name in HARNESS:
    w = (n - 1) * pitch + 3.0
    a.add_patch(Rectangle((x - w / 2, 36.2), w, 3.6, fc="#fff3c4", ec="#8a6d00", lw=0.8, zorder=3))
    for k in range(n):
        a.add_patch(Circle((x - (n - 1) * pitch / 2 + k * pitch, 38.0), 0.55, fc="#8a6d00", ec="none", zorder=4))
    a.text(x, 41.8, name, ha="center", va="top", fontsize=6.0)
part(a, 0.8, 20.0, 4.6, 12.0, "X13 X14\nLED\npedálů", fc="#fff3c4", ec="#8a6d00", fs=5.2)

# DevKit v paticích, USB směrem ke konci u stabilizátoru
part(a, 137.0, 4.5, 64.0, 28.0, "ESP32-S3 DevKit v paticích 2×22\n64 × 28 mm, řady 25,4 mm (ověřit podle kusu)", fc="#dfe9f7", ec="#1f4e8c", fs=7)
part(a, 201.0, 12.5, 7.0, 12.0, "2× USB-C", fc="#b9cdea", ec="#1f4e8c", fs=5.2, rot=90)
a.annotate("kabel na zadní panel", (208.0, 18.5), (216.5, 27.0), fontsize=5.6, color="#1f4e8c",
           arrowprops=dict(arrowstyle="-", lw=0.6, color="#1f4e8c"))

part(a, 12.0, 8.0, 35.6, 7.6, "U2 MCP23017 (DIP-28)\nbudí původní LED", fc="#fde9d9", ec="#b35c00")
part(a, 12.0, 18.5, 70.0, 12.5, "12× vstup spínače: 47 kΩ, 470 Ω, 100 nF\n10× odpor LED 150 Ω", fc="#f4f4f4", ec="#777", ls="--")
part(a, 52.0, 8.0, 38.0, 8.0, "U4 LDO 4,0 V + 2× vstup pedálu\n10 kΩ / 15 kΩ, 470 nF, 1 kΩ, 100 nF", fc="#f4f4f4", ec="#777", ls="--", fs=6)
part(a, 94.0, 18.5, 19.0, 7.6, "U3 74HCT125\n(DIP-14)", fc="#fde9d9", ec="#b35c00", fs=6)
part(a, 122.5, 18.0, 12.5, 10.0, "MIDI IN\n10 kΩ / 22 kΩ", fc="#f4f4f4", ec="#777", ls="--", fs=5.6)
part(a, 205.0, 27.5, 5.2, 7.2, "K1", fc="#fde9d9", ec="#b35c00", fs=5.6)
part(a, 211.5, 27.5, 5.2, 7.2, "K2", fc="#fde9d9", ec="#b35c00", fs=5.6)
a.text(219.0, 31.0, "PhotoMOS\nAQY212EH", fontsize=5.4, va="center")
part(a, 96.0, 8.0, 14.0, 7.5, "BOOT\nRESET", fc="#f4f4f4", ec="#777", fs=5.6)

# ---------------------------------------------------------------- strana k panelu
board(b, "B  Strana k hornímu panelu (zrcadlově: konec u displeje vpravo). Co je vidět okénkem.")
mounting(b, mirror=True)
cx, cy, ww, wh = WIN
b.add_patch(Rectangle((L - cx - ww / 2, cy - wh / 2), ww, wh, fc="#f2c1bb", ec=C_UNSURE, lw=1.0, zorder=3))
b.text(L - cx, cy, "původní červené\nokénko 36 × 18,5 mm\n(z fotek)", ha="center", va="center", fontsize=5.8, color=C_UNSURE, zorder=8)
ow, oh = OLED_ACTIVE
b.add_patch(Rectangle((L - cx - ow / 2, cy - oh / 2), ow, oh, fc="none", ec="#1f4e8c", lw=1.2, ls="--", zorder=6))
b.text(L - cx - ow / 2 - 1.5, 28.5, "čárkovaně: obraz OLED 2,42\" 55 × 27,5 mm\nvystředěný na původní okénko.\nPřesahuje hranu desky a kryje Ú1.", ha="right", va="top", fontsize=6, color="#1f4e8c")

for x0, x1, n, name in LED_GROUPS:
    b.add_patch(Rectangle((L - x1, 10.0), x1 - x0, 6.0, fc="#e3e3e3", ec="#666", lw=0.8, zorder=3))
    for k in range(n):
        xc = x1 - 6.0 - k * ((x1 - x0 - 12.0) / (n - 1))
        b.add_patch(Rectangle((L - xc - 2.2, 11.4), 4.4, 3.2, fc="#c0392b" if n == 2 else "#3d9a4a", ec="none", zorder=4))
    b.text(L - (x0 + x1) / 2, 17.2, f"{name} (stavové LED, rozteč asi 12,7 mm)", ha="center", va="top", fontsize=5.8)
b.text(0, W + 5.5, "Stavové LED a displej jsou asi 10 až 12 mm nad deskou, těsně pod černým pásem panelu. "
       "Ú1 až Ú3 = úhelníky se závitem, polohy středů z otisku na čtverečkovaném papíře (±0,7 mm).",
       fontsize=6.6, va="top")
b.text(0, W + 10.5, "FCB1010-S3, rozvržení nosné desky v0.2 (18. 11. 2026). Návrh k připomínkám, ne výrobní podklad.",
       fontsize=6.6, va="top", color="#555")

fig.tight_layout()
fig.savefig("../rozvrzeni-desky.png", dpi=170)
fig.savefig("../rozvrzeni-desky.svg")
print("ok")
