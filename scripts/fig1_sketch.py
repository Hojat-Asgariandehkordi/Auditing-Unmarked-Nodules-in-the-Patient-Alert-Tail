"""Layout sketch for the BioRender method-overview illustration of Fig. 1.

This is the reference image given to BioRender (exact counts, positions and arrows);
it is not used in the paper. Output: figures/biorender/sketch_layout.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Ellipse

OUT = Path(__file__).resolve().parent.parent / "figures" / "biorender" / "sketch_layout.png"
BLUE, ORANGE, PURPLE, NAVY, GREY = "#17669f", "#a65c12", "#7b3294", "#17293a", "#8a959c"

fig, ax = plt.subplots(figsize=(14, 4.0))
ax.set_xlim(0, 140)
ax.set_ylim(0, 40)
ax.axis("off")


def band(x0, x1, title, col):
    ax.add_patch(FancyBboxPatch((x0, 1), x1 - x0, 36, boxstyle="round,pad=0,rounding_size=1.5", fc=col, ec="none"))
    ax.text((x0 + x1) / 2, 35.2, title, ha="center", va="top", fontsize=13, weight="bold", color=NAVY)


def arrow(x0, y0, x1, y1, col=NAVY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.8, color=col, mutation_scale=14))


def label(x, y, t, **kw):
    ax.text(x, y, t, ha="center", va="top", fontsize=10, color=NAVY, **kw)


band(1, 84, "1  Training: which candidates to audit (445 patients)", "#e8f0f6")
band(85, 116, "2  Calibration (175)", "#f1eaf5")
band(117, 139, "3  Test (265)", "#e8f4ee")

# --- CT slice with 6 candidates, one omitted nodule (purple ring)
ax.add_patch(Ellipse((10, 19), 15, 19, fc="#2b2b2b", ec="none"))
ax.add_patch(Ellipse((6.8, 19.5), 5.5, 13, fc="#6d6d6d", ec="none"))
ax.add_patch(Ellipse((13.2, 19.5), 5.5, 13, fc="#6d6d6d", ec="none"))
for (x, y) in [(6, 23), (7.5, 15), (12.5, 24), (14, 17), (11.8, 13.5)]:
    ax.add_patch(Circle((x, y), 0.9, fc="none", ec="#f6d860", lw=1.6))
ax.add_patch(Circle((6.2, 18.5), 1.1, fc="none", ec=PURPLE, lw=3))
label(10, 8.6, "chest CT with 6 candidates\n(purple: nodule missed by reader A)")

# --- two weak readers
for i, (name, y) in enumerate([("Reader A", 27), ("Reader B", 16)]):
    ax.add_patch(Circle((24, y + 2.3), 1.4, fc=NAVY))
    ax.add_patch(FancyBboxPatch((22, y - 2), 4, 3, boxstyle="round,pad=0,rounding_size=1", fc=NAVY))
    ax.text(24, y - 2.8, name, ha="center", va="top", fontsize=10, color=NAVY)
ax.text(27, 29.5, "2 marks", fontsize=9, color=NAVY)
ax.text(27, 18.6, "3 marks", fontsize=9, color=NAVY)
ax.text(24, 9.6, "disagree on 1", fontsize=9, color=NAVY, ha="center")
arrow(17.8, 19, 21.2, 22)

# --- frozen pilot detector ranks candidates
ax.add_patch(FancyBboxPatch((36, 15), 7, 9, boxstyle="round,pad=0,rounding_size=1", fc="white", ec=GREY, lw=1.5, ls="--"))
ax.text(39.5, 20.8, "*", fontsize=26, ha="center", va="center", color="#4a90c2")
label(39.5, 14.2, "frozen pilot\ndetector")
arrow(31, 21, 35.6, 20)

# --- ranked list with audit-probability bars
ax.text(52, 30.4, "rank -> audit probability", fontsize=10, ha="center", color=NAVY)
heights = [9, 7.5, 2.2, 6.5, 1.2, 0.8, 0.6, 0.5]  # rank 1, 2, ..., disputed at rank 4
for r, h in enumerate(heights):
    y = 28.5 - r * 2.6
    ax.add_patch(Rectangle((46, y - 0.8), 2.4, 1.6, fc="white", ec=GREY))
    ax.text(47.2, y, str(r + 1), fontsize=8, ha="center", va="center")
    ax.add_patch(Rectangle((49, y - 0.7), h, 1.4, fc=BLUE, ec="none"))
ax.text(52, 5.6, "... + 250 unremarkable candidates per scan (tiny bars)", fontsize=8.5, ha="center", color=GREY)
arrow(43.4, 20, 45.6, 20)

# --- audit with magnifier on 3 sampled rows
ax.add_patch(Circle((64, 24), 2.2, fc="white", ec=NAVY, lw=2.5))
ax.plot([65.5, 67.5], [22.4, 20], color=NAVY, lw=3)
label(64.5, 18.0, "expert audit\n(3 sampled)")
arrow(59.5, 24, 61.5, 24)

# --- frozen 3D encoder + trainable linear head on corrected labels
ax.add_patch(FancyBboxPatch((72, 18), 4.5, 10, boxstyle="round,pad=0,rounding_size=1", fc="white", ec=GREY, lw=1.5, ls="--"))
ax.text(74.2, 23, "*", fontsize=22, ha="center", va="center", color="#4a90c2")
ax.add_patch(FancyBboxPatch((77.8, 20), 3.2, 6, boxstyle="round,pad=0,rounding_size=1", fc="#fbe3d0", ec=ORANGE, lw=1.5))
ax.text(79.4, 23, "^", fontsize=18, ha="center", va="center", color=ORANGE)
label(76.5, 16.8, "frozen encoder\n+ trained head")
arrow(68, 23, 71.6, 23)

# --- calibration: 10 negative patients, 3 tallest purple; two thresholds
bars = [6, 8, 9.5, 11, 12, 13, 14.5, 18, 21, 24]  # y0=6 so tops are 6+h
purple = {6, 7, 9}
for i, h in enumerate(bars):
    x = 87.5 + i * 2.6
    ax.add_patch(Rectangle((x, 6), 1.8, h, fc=PURPLE if i in purple else NAVY, ec="none"))
ax.plot([86.5, 114], [27, 27], color=GREY, ls="--", lw=2)
ax.text(86.8, 27.6, "threshold: 2nd largest of all", fontsize=8.5, color=GREY, ha="left", va="bottom")
ax.plot([86.5, 114], [19, 19], color=BLUE, ls="--", lw=2)
ax.text(86.8, 19.6, "after removing purple: 2nd largest", fontsize=8.5, color=BLUE, ha="left", va="bottom")
label(100.5, 5.2, "max score per negative patient\n(purple: official-consensus nodule)")
arrow(83.4, 23, 86.2, 23)

# --- test: omission found under the lower threshold
ax.add_patch(Ellipse((124, 21), 8, 11, fc="#2b2b2b", ec="none"))
ax.add_patch(Circle((122.5, 21), 1.0, fc="none", ec=BLUE, lw=2.5))
ax.add_patch(Rectangle((132, 6), 2.2, 17, fc=BLUE, ec="none"))
ax.plot([130.5, 136], [27, 27], color=GREY, ls="--", lw=2)
ax.plot([130.5, 136], [19, 19], color=BLUE, ls="--", lw=2)
label(124.5, 13.2, "test omission:\nmissed at grey,\nfound at blue")
arrow(114.6, 21, 119.6, 21)

OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=110, bbox_inches="tight", facecolor="white")
print("wrote", OUT)
