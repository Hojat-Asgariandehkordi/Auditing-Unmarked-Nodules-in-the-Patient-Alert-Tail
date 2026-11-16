"""Figure 1: method overview (a) above the toy-roster (b) and real-threshold (c) panels.

Panel (a) is drawn in vector form: panels, boxes, bars, thresholds, arrows and every label
are placed in one coordinate system (inches), so each label sits inside its own shape and
the layout uses the full width. Only four pictorial icons come from the BioRender art
(figure 5186a2a8dbee86b88aec68cb, "H1"): the scanner with the training CT slice, the two
readers, the magnifier and the test CT slice. They are cut out with their pastel
background keyed to transparent. The extra (7th) candidate circle that BioRender drew on
the training slice is inpainted, so the slice shows the six candidates listed in the bars.

Icon coordinates are pixels of the 1024-px BioRender preview and are scaled to the
full-resolution export automatically when figures/biorender/overview_H1.png exists.
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle
from PIL import Image

from style import C, TEXT_W, save, FIG
import fig_teaser as T

PREVIEW_W = 1024.0
SRC = [FIG / "biorender" / "overview_H1.png", FIG / "biorender" / "overview_H1_preview.jpg"]

# icon boxes in preview pixels (x0, y0, x1, y1) and the panel colour they sit on
BG_BLUE, BG_GREEN = (216, 232, 247), (224, 237, 217)
ICONS = {
    "ct_train": ((22, 210, 192, 360), BG_BLUE),
    "readers": ((200, 226, 307, 298), BG_BLUE),
    "magnifier": ((352, 168, 384, 200), BG_BLUE),
    "ct_test": ((803, 246, 908, 338), BG_GREEN),
}
EXTRA_CIRCLE = (139, 266, 7)

NAVY = C["neg"]
MUTED = C["muted"]
PURPLE = C["official"]
BLUE = C["paired"]
PANEL = {"train": "#d8e8f7", "cal": "#ece3f3", "test": "#e0edd9"}
BOX_FACE, BOX_EDGE = "#f3f5f7", "#8d9aa5"
A_W, A_H = TEXT_W, 2.40          # panel (a) in inches


# ---------------------------------------------------------------- icons
def load_art():
    for p in SRC:
        if p.exists():
            return np.asarray(Image.open(p).convert("RGB")).copy(), p
    raise FileNotFoundError(SRC)


def icons():
    img, src = load_art()
    s = img.shape[1] / PREVIEW_W
    S = lambda v: int(round(v * s))
    mask = np.zeros(img.shape[:2], np.uint8)
    cx, cy, r = EXTRA_CIRCLE
    cv2.circle(mask, (S(cx), S(cy)), S(r), 255, -1)
    img = cv2.inpaint(img, mask, max(3, S(4)), cv2.INPAINT_TELEA)
    out = {}
    for name, ((x0, y0, x1, y1), bg) in ICONS.items():
        a = img[S(y0):S(y1), S(x0):S(x1)].astype(float)
        if name == "readers":       # drop the leader line from reader B towards the candidate list
            yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
            tinted = a[..., 0] > a[..., 1] + 4          # purple line and its anti-aliased fringe
            a[tinted & (xx > S(294 - x0))] = bg
        if name == "ct_test":       # the reader icon overlapped the left frame of the slice
            frame = np.median(a[S(320 - y0):S(330 - y0), S(805 - x0):S(809 - x0)].reshape(-1, 3), axis=0)
            a[S(268 - y0):S(318 - y0), 0:S(812 - x0)] = frame
            a[:, 0:S(804 - x0)] = bg
        d = np.sqrt(((a - np.array(bg, float)) ** 2).sum(-1))
        alpha = np.clip((d - 7.0) / 16.0, 0, 1)
        out[name] = np.dstack([a / 255.0, alpha])
    return out, src


def put(ax, icon, x0, y0, w):
    h = w * icon.shape[0] / icon.shape[1]
    ax.imshow(icon, extent=(x0, x0 + w, y0, y0 + h), interpolation="lanczos", zorder=3)
    return h


# ---------------------------------------------------------------- vector glyphs
def panel(ax, x0, y0, x1, y1, color):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=0.09",
                                fc=color, ec="none", zorder=0))


def box(ax, x0, y0, x1, y1, text, fc=BOX_FACE, ec=BOX_EDGE, ls="-", size=6.5, tx=None):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=fc, ec=ec, lw=0.7, ls=ls, zorder=2))
    ax.text((x0 + x1) / 2 if tx is None else tx, (y0 + y1) / 2, text, ha="center", va="center",
            fontsize=size, linespacing=0.95, zorder=4)


def arrow(ax, x0, y0, x1, y1, color=NAVY):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.8, mutation_scale=7,
                                shrinkA=0, shrinkB=0))


def snowflake(ax, x, y, r=0.05, color="#7f8e9a"):
    for k in range(3):
        t = np.pi / 2 + k * np.pi / 3
        ax.plot([x - r * np.cos(t), x + r * np.cos(t)], [y - r * np.sin(t), y + r * np.sin(t)],
                color=color, lw=0.8, solid_capstyle="round", zorder=4)
        for sgn in (-1, 1):
            bx, by = x + sgn * 0.58 * r * np.cos(t), y + sgn * 0.58 * r * np.sin(t)
            for dt in (-0.8, 0.8):
                u = t + (0 if sgn > 0 else np.pi) + dt
                ax.plot([bx, bx + 0.42 * r * np.cos(u)], [by, by + 0.42 * r * np.sin(u)],
                        color=color, lw=0.7, solid_capstyle="round", zorder=4)


def person(ax, x, y, color, alpha=1.0, w=0.085):
    """Simple patient glyph: head and shoulders, base at y."""
    t = np.linspace(0, np.pi, 30)
    ax.add_patch(Polygon(np.c_[x + 0.5 * w * np.cos(t), y + 0.52 * w * np.sin(t)], closed=True,
                         fc=color, ec="none", alpha=alpha, zorder=3))
    ax.add_patch(Circle((x, y + 0.74 * w), 0.25 * w, fc=color, ec="white", lw=0.4, alpha=alpha, zorder=3))


def check(ax, x, y, s=0.07, color=BLUE):
    ax.plot([x - s, x - 0.35 * s, x + s], [y, y - 0.6 * s, y + 0.75 * s], color=color, lw=1.6,
            solid_capstyle="round", solid_joinstyle="round", zorder=4)


def cross(ax, x, y, s=0.05, color="#b8312f"):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=1.5, solid_capstyle="round", zorder=4)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=1.5, solid_capstyle="round", zorder=4)


def dashed(ax, x0, x1, y, color):
    ax.plot([x0, x1], [y, y], color=color, lw=1.0, ls=(0, (4, 2.4)), zorder=4)


def titles(ax, x, title, sub):
    ax.text(x, 2.215, title, ha="center", va="center", fontsize=7.9, zorder=4)
    ax.text(x, 2.075, sub, ha="center", va="center", fontsize=6.6, color=MUTED, zorder=4)


# ---------------------------------------------------------------- panel (a)
CAL_H = np.array([1.0, 0.83, 0.72, 0.66, 0.50, 0.43, 0.36, 0.30, 0.25])
CAL_OFFICIAL = {0, 2, 3}
BAR_SCALE = 0.50
ROW_BASE = (1.38, 0.30)                       # baselines of the two threshold rows
T_TOP = ROW_BASE[0] + CAL_H[1] * BAR_SCALE   # 2nd largest maximum of all negatives
T_LOW = ROW_BASE[1] + CAL_H[4] * BAR_SCALE   # 2nd largest after excluding official positives
TEST_H = 0.70                                 # test omission: between the two thresholds


def draw_overview(ax, ic):
    ax.set_xlim(0, A_W)
    ax.set_ylim(0, A_H)
    ax.set_aspect("equal")
    ax.axis("off")
    tr, ca, te = (0.03, 3.28), (3.43, 5.30), (5.45, 6.845)
    panel(ax, tr[0], 0.03, tr[1], 2.34, PANEL["train"])
    panel(ax, ca[0], 0.03, ca[1], 2.34, PANEL["cal"])
    panel(ax, te[0], 0.03, te[1], 2.34, PANEL["test"])
    arrow(ax, tr[1] + 0.015, 1.20, ca[0] - 0.012, 1.20)
    arrow(ax, ca[1] + 0.015, 1.20, te[0] - 0.012, 1.20)
    titles(ax, sum(tr) / 2, "Training (445 patients)", "which candidates to audit")
    titles(ax, sum(ca) / 2, "Calibration (175 patients)", "who sets the alert threshold")
    titles(ax, sum(te) / 2, "Test (265 patients)", "is an omission found?")

    # --- training, top row: CT -> weak reads + frozen detector -> audit probabilities
    put(ax, ic["ct_train"], 0.08, 1.06, 0.975)
    arrow(ax, 1.065, 1.45, 1.17, 1.45)
    put(ax, ic["readers"], 1.20, 1.38, 0.66)
    ax.text(1.20 + 0.66 * 21 / 107, 1.905, "reader A", ha="center", va="center", fontsize=6.5, zorder=4)
    ax.text(1.20 + 0.66 * 85 / 107, 1.905, "reader B", ha="center", va="center", fontsize=6.5, zorder=4)
    box(ax, 1.20, 1.06, 1.86, 1.31, "frozen\ndetector", ls=(0, (3, 2)), size=6.3, tx=1.565)
    snowflake(ax, 1.29, 1.185)
    arrow(ax, 1.885, 1.45, 2.00, 1.45)

    ax.text(2.62, 1.905, r"audit probability $\pi_i$", ha="center", va="center", fontsize=6.5, zorder=4)
    pis = [1.0, 0.87, 0.07, 0.58, 0.05, 0.03]
    for k, p in enumerate(pis):
        y = 1.775 - 0.118 * k
        ax.text(2.085, y, str(k + 1), ha="center", va="center", fontsize=6.2, zorder=4)
        omit = k == 3
        ax.add_patch(Circle((2.185, y), 0.03, fc="white", ec=PURPLE if omit else "#7d8a94",
                            lw=1.5 if omit else 0.7, zorder=4))
        ax.add_patch(Rectangle((2.26, y - 0.037), 0.90 * p, 0.074, fc=BLUE, ec="none", zorder=3))
    ax.text(2.185, 1.06, r"$\cdots$", ha="center", va="center", fontsize=6.5, zorder=4)

    # --- training, bottom row: audit -> corrected labels -> head g <- frozen encoder <- CT
    enc = np.array([[0.12, 0.20], [0.12, 0.88], [0.82, 0.74], [0.82, 0.34]])
    ax.add_patch(Polygon(enc, closed=True, fc="#eceff1", ec=BOX_EDGE, lw=0.7, ls=(0, (3, 2)), zorder=2))
    snowflake(ax, 0.215, 0.54)
    ax.text(0.50, 0.54, "frozen 3D\nencoder", ha="center", va="center", fontsize=6.3,
            linespacing=0.95, zorder=4)
    arrow(ax, 0.70, 1.045, 0.70, 0.765)
    box(ax, 0.98, 0.40, 1.52, 0.69, "trained\nhead $g$", fc="#fbd6b6", ec="#d9893f", size=6.5)
    arrow(ax, 0.825, 0.545, 0.975, 0.545)
    box(ax, 1.70, 0.40, 2.36, 0.69, "corrected\nlabels $z_i$", fc="white", ec=BLUE, size=6.5)
    arrow(ax, 1.695, 0.545, 1.525, 0.545)
    box(ax, 2.55, 0.37, 3.20, 0.72, "", fc="white", ec=BOX_EDGE)
    put(ax, ic["magnifier"], 2.60, 0.455, 0.175)
    ax.text(2.99, 0.545, "expert\naudit", ha="center", va="center", fontsize=6.5, linespacing=0.95, zorder=4)
    arrow(ax, 2.545, 0.545, 2.365, 0.545)
    arrow(ax, 2.875, 1.03, 2.875, 0.725)
    ax.text(2.835, 0.875, r"sampled with prob. $\pi_i$", ha="right", va="center", fontsize=6.0,
            color=MUTED, zorder=4)

    # --- calibration: two rows of negative-patient maxima, before / after exclusion
    pitch, bw = 0.175, 0.115
    x0 = ca[0] + (ca[1] - ca[0] - (8 * pitch + bw)) / 2 + bw / 2
    for row, base in enumerate(ROW_BASE):
        for j, h in enumerate(CAL_H):
            xc = x0 + j * pitch
            official = j in CAL_OFFICIAL
            col = PURPLE if official else NAVY
            alpha = 0.22 if (official and row == 1) else 1.0
            ax.add_patch(Rectangle((xc - bw / 2, base), bw, h * BAR_SCALE, fc=col, ec="none",
                                   alpha=alpha, zorder=3))
            person(ax, xc, base - 0.105, col, alpha)
    dashed(ax, ca[0] + 0.08, ca[1] - 0.06, T_TOP, MUTED)
    ax.text(ca[1] - 0.06, T_TOP + 0.045, r"threshold $T$", ha="right", va="bottom", fontsize=6.5,
            color=MUTED, zorder=4)
    ax.text(sum(ca) / 2, 1.115, "excluding official positives", ha="center", va="center", fontsize=6.6,
            color=PURPLE, zorder=4)
    dashed(ax, ca[0] + 0.08, ca[1] - 0.06, T_LOW, BLUE)
    ax.text(ca[1] - 0.06, T_LOW + 0.045, "lower threshold", ha="right", va="bottom", fontsize=6.5,
            color=BLUE, zorder=4)

    # --- test: the same omission score against both thresholds
    w_ct = 0.76
    h_ct = w_ct * ic["ct_test"].shape[0] / ic["ct_test"].shape[1]
    put(ax, ic["ct_test"], 5.50, 1.14 - h_ct / 2, w_ct)
    ax.text(5.50 + w_ct / 2, 1.14 - h_ct / 2 - 0.075, "test omission", ha="center", va="center",
            fontsize=6.4, color=BLUE, zorder=4)
    xb, xm = 6.40, 6.665
    for row, base in enumerate(ROW_BASE):
        ax.add_patch(Rectangle((xb - bw / 2, base), bw, TEST_H * BAR_SCALE, fc=BLUE, ec="none", zorder=3))
        person(ax, xb, base - 0.105, BLUE)
    dashed(ax, 6.30, 6.80, T_TOP, MUTED)
    dashed(ax, 6.30, 6.80, T_LOW, BLUE)
    ax.text(6.255, T_TOP, r"threshold $T$", ha="right", va="center", fontsize=6.5, color=MUTED, zorder=4)
    ax.text(6.255, T_LOW, "lower threshold", ha="right", va="center", fontsize=6.5, color=BLUE, zorder=4)
    cross(ax, xm, 1.62, color=MUTED)
    ax.text(xm, 1.49, "missed", ha="center", va="center", fontsize=6.5, color=MUTED, zorder=4)
    check(ax, xm, 0.43)
    ax.text(xm, 0.30, "found", ha="center", va="center", fontsize=6.5, color=BLUE, zorder=4)


def main():
    ic, src = icons()
    bottom_h = 1.68
    H = A_H + bottom_h + 0.30
    fig = plt.figure(figsize=(TEXT_W, H))
    ax = fig.add_axes([0, (bottom_h + 0.15) / H, 1, A_H / H])
    draw_overview(ax, ic)
    fig.text(0.004, (bottom_h + 0.15 + A_H) / H + 0.002, r"$\bf{(a)}$ Method overview", fontsize=8.3,
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
    print("icon source:", src.name)


if __name__ == "__main__":
    main()
