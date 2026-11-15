"""Figure 1: BioRender method overview (a) above the two data panels (b, c).

The art is BioRender figure 5186a2a8dbee86b88aec68cb ("H1", round 2). BioRender draws its
own sans-serif lettering and is not exact about counts or line positions, so this script

  1. erases every BioRender label (fill with the light background inside the box),
  2. repairs the science: removes the 7th candidate circle (the CT shows 6), removes the
     pale score segment above the grey test threshold, fades the third excluded
     (purple) patient icon, and erases the calibration/test threshold lines,
  3. redraws the threshold lines exactly (top row: top of the 2nd tallest bar; bottom
     row: top of the 2nd tallest remaining navy bar) and the corrected-label arrow,
  4. typesets every label in Times from the single LAYOUT table below.

All coordinates are in pixels of the 1024-px BioRender preview; they are scaled to the
full-resolution export automatically. Input (first that exists):
  figures/biorender/overview_H1.png (full resolution), figures/biorender/overview_H1_preview.jpg
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

from style import C, TEXT_W, save, FIG
import fig_teaser as T

PREVIEW_W = 1024.0
SRC = [FIG / "biorender" / "overview_H1.png", FIG / "biorender" / "overview_H1_preview.jpg"]
CROP = (10, 100, 1014, 474)          # content band of the art (x0, y0, x1, y1)

# ---- BioRender lettering to erase (x0, y0, x1, y1) ---------------------------------
INSIDE = {(224, 322, 279, 355), (314, 219, 330, 331), (318, 376, 370, 431), (405, 386, 453, 419)}
ERASE = [
    (186, 117, 304, 154), (546, 116, 700, 149), (855, 117, 923, 149),   # card titles
    (193, 209, 251, 228), (257, 209, 315, 228),                         # Reader A / B
    (224, 322, 279, 355),                                               # frozen detector
    (381, 168, 455, 192), (345, 200, 444, 220),                         # expert audit, audit probability
    (314, 219, 330, 331),                                               # row numbers 1-6
    (318, 376, 370, 431),                                               # frozen 3D CNN encoder
    (405, 386, 453, 419),                                               # trained head
    (672, 178, 734, 197), (638, 337, 735, 353),                         # calibration labels
    (914, 214, 958, 234), (942, 238, 1003, 255), (958, 291, 1000, 309), (904, 334, 970, 366),  # test labels
    (926, 233, 947, 263),                                               # pale score segment above grey line
]
# old dashed threshold lines: each column is refilled from the row just above (or below) the
# strip, which continues vertical bars and flat background without smudging
STRIPS = [((510, 192, 739, 201), "above"), ((510, 351, 739, 360), "above"),
          ((908, 254, 1004, 261), "above"), ((908, 329, 1004, 336), "below")]
EXTRA_CIRCLE = (139, 266, 7)          # 7th candidate circle on the CT slice (x, y, radius)
FADE_ICON = (518, 412, 540, 444)      # bottom-row icon of the tallest (purple) patient

# ---- exact threshold geometry (preview px) -------------------------------------------
CAL_X = (513, 736)
T_TOP = 175      # top of the 2nd tallest bar, top row
T_BOTTOM = 360   # top of the 2nd tallest remaining navy bar (bar 5), bottom row
TEST_X = (911, 1001)
TEST_GREY, TEST_BLUE = 257, 332

NAVY, MUTED = C["first"], C["muted"]
LAYOUT = [  # text, x, y, size, ha, colour
    ("Training: which candidates to audit", 245, 128, 8.6, "center", NAVY),
    ("445 patients", 245, 147, 6.8, "center", MUTED),
    ("Calibration: who sets the threshold", 622, 128, 8.6, "center", NAVY),
    ("175 patients", 622, 147, 6.8, "center", MUTED),
    ("Test", 889, 128, 8.6, "center", NAVY),
    ("265 patients", 889, 147, 6.8, "center", MUTED),
    ("reader A", 222, 219, 6.9, "center", NAVY),
    ("reader B", 286, 219, 6.9, "center", NAVY),
    ("frozen\ndetector", 251, 338, 6.6, "center", NAVY),
    ("expert audit", 384, 181, 6.9, "left", NAVY),
    (r"audit probability $\pi_i$", 394, 210, 6.9, "center", NAVY),
    ("frozen\n3D\nencoder", 343, 404, 6.2, "center", NAVY),
    ("trained\nhead $g$", 429, 402, 6.6, "center", NAVY),
    ("corrected\nlabels $z_i$", 424, 357, 6.3, "right", NAVY),
    ("threshold $T$", 735, 166, 6.7, "right", MUTED),
    ("excluding official positives", 624, 304, 6.5, "center", C["official"]),
    ("lower threshold", 735, 350, 6.7, "right", C["paired"]),
    ("threshold", 1001, 248, 6.5, "right", MUTED),
    ("lower threshold", 1001, 343, 6.5, "right", C["paired"]),
    ("found", 981, 302, 6.7, "center", C["paired"]),
] + [(str(i + 1), 322, y, 6.4, "center", NAVY) for i, y in enumerate([228, 247, 266, 285, 303, 322])]


def load_art():
    for p in SRC:
        if p.exists():
            return np.asarray(Image.open(p).convert("RGB")).copy(), p
    raise FileNotFoundError(SRC)


def clean(img, s):
    S = lambda v: int(round(v * s))
    lum = img.mean(axis=2)
    for box in ERASE:
        x0, y0, x1, y1 = (S(v) for v in box)
        if box in INSIDE:
            patch, L = img[y0:y1, x0:x1], lum[y0:y1, x0:x1]
            fill = np.median(patch[L >= np.percentile(L, 70)], axis=0)
        else:
            p = max(2, S(3))
            ring = np.concatenate([img[y0 - p:y0, x0:x1].reshape(-1, 3), img[y1:y1 + p, x0:x1].reshape(-1, 3),
                                   img[y0:y1, x0 - p:x0].reshape(-1, 3), img[y0:y1, x1:x1 + p].reshape(-1, 3)])
            fill = np.median(ring, axis=0)
        img[y0:y1, x0:x1] = fill.astype(np.uint8)
    for (x0, y0, x1, y1), src in STRIPS:
        x0, y0, x1, y1 = S(x0), S(y0), S(x1), S(y1)
        row = img[y0 - 1, x0:x1] if src == "above" else img[y1, x0:x1]
        img[y0:y1, x0:x1] = row[None, :, :]
    mask = np.zeros(img.shape[:2], np.uint8)
    cx, cy, r = EXTRA_CIRCLE
    cv2.circle(mask, (S(cx), S(cy)), S(r), 255, -1)
    img = cv2.inpaint(img, mask, max(3, S(4)), cv2.INPAINT_TELEA)
    x0, y0, x1, y1 = (S(v) for v in FADE_ICON)
    bg = np.median(img[S(300):S(312), S(505):S(512)].reshape(-1, 3), axis=0)
    img[y0:y1, x0:x1] = (0.72 * bg + 0.28 * img[y0:y1, x0:x1]).astype(np.uint8)
    return img


def draw_overview(ax, img, s):
    x0, y0, x1, y1 = CROP
    S = lambda v: int(round(v * s))
    ax.imshow(img[S(y0):S(y1), S(x0):S(x1)], extent=(x0, x1, y1, y0), interpolation="lanczos")
    ax.set_xlim(x0, x1)
    ax.set_ylim(y1, y0)
    ax.axis("off")
    for y, col in ((T_TOP, MUTED), (T_BOTTOM, C["paired"])):
        ax.plot(CAL_X, [y, y], color=col, lw=1.1, ls=(0, (4, 2.5)), zorder=3)
    for y, col in ((TEST_GREY, MUTED), (TEST_BLUE, C["paired"])):
        ax.plot(TEST_X, [y, y], color=col, lw=1.1, ls=(0, (4, 2.5)), zorder=3)
    ax.annotate("", xy=(432, 382), xytext=(432, 334),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=0.8, mutation_scale=7), zorder=3)
    for t, x, y, size, ha, col in LAYOUT:
        ax.text(x, y, t, fontsize=size, ha=ha, va="center", color=col, linespacing=0.95, zorder=4)


def main():
    img, src = load_art()
    s = img.shape[1] / PREVIEW_W
    img = clean(img, s)
    x0, y0, x1, y1 = CROP
    art_h = TEXT_W * (y1 - y0) / (x1 - x0)
    bottom_h = 1.68
    fig = plt.figure(figsize=(TEXT_W, art_h + bottom_h + 0.32))
    H = art_h + bottom_h + 0.32
    ax = fig.add_axes([0, (bottom_h + 0.17) / H, 1, art_h / H])
    draw_overview(ax, img, s)
    fig.text(0.004, (bottom_h + 0.17 + art_h) / H + 0.004, r"$\bf{(a)}$ Method overview", fontsize=8.3,
             ha="left", va="bottom")

    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.18], wspace=0.06, left=0.045, right=0.995,
                          bottom=0.02, top=(bottom_h - 0.27) / H)
    pi_mark, pi_pair, hid_mark, hid_pair, B = T.allocate()
    a1, a2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    T.draw_roster(a1, pi_mark, hid_mark, C["mark"], "Mark-stratified review")
    T.draw_roster(a2, pi_pair, hid_pair, C["paired"], "Paired-tail review (ours)")
    a2.set_yticklabels([])
    for a in (a1, a2):
        a.annotate("", xy=(9.6, -0.68), xytext=(-0.3, -0.68),
                   arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.6, mutation_scale=6))
        a.text(4.5, -0.72, "image score, high to low", fontsize=6.6, color=MUTED, ha="center", va="top")
    top_b = (bottom_h - 0.04) / H
    fig.text(0.045, top_b, rf"$\bf{{(b)}}$ Audit probabilities on a toy roster (equal budget, {B:.1f} audits)",
             fontsize=8.3, ha="left", va="bottom")
    c = fig.add_subplot(gs[2])
    T.draw_cutoff(c)
    fig.text(c.get_position().x0, top_b, r"$\bf{(c)}$ Real thresholds of the selected detector",
             fontsize=8.3, ha="left", va="bottom")
    save(fig, "teaser")
    print("art source:", src.name, img.shape)


if __name__ == "__main__":
    main()
