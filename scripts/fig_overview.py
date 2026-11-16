"""Figure 1: overview in four panels, following the authors' slide layout.

(a) The problem: a visible nodule left unmarked becomes a background label.
(b) Paired-tail audit allocation: pilot scores and reader disagreement set audit
    priorities; audited labels are corrected and train a linear head on a frozen encoder.
(c) Score-fixed calibration replay: the 15 largest of the 67 C/D-negative calibration
    maxima of the selected detector (recovered values, scripts/data.py) before and after
    excluding patients with an official consensus nodule; thresholds 1.524 -> 0.630.
(d) Consequence: the test omission of Fig. 6(c) (margins -0.81 / +0.09) is missed under
    the original threshold and found under the lower one, with its score unchanged.

Every element is drawn in vector form in one inch-based coordinate system; the only
rasters are the real LUNA16 crops (figures/ct, 28 mm field of view). All text is Times.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle
from matplotlib.path import Path
from PIL import Image

from style import C, TEXT_W, save, FIG
import data as D

W, H = TEXT_W, 4.30
NAVY, MUTED, PURPLE, BLUE = C["neg"], C["muted"], C["official"], C["paired"]
AMBER = "#e0912f"
TEAL = "#2a8c8c"
BOX_EDGE = "#8d9aa5"
HEAD_FACE, HEAD_EDGE = "#fbd6b6", "#d9893f"
T_SCORE = D.T_P - 0.81            # test omission of Fig. 6(c): margin -0.81 / +0.09


def ct(i):
    return np.asarray(Image.open(FIG / "ct" / f"crop-00{i}.png").convert("L"))


# ------------------------------------------------------------ drawing helpers
def txt(ax, x, y, s, size=6.5, color="black", ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, linespacing=0.95, zorder=6, **kw)


def rbox(ax, x0, y0, x1, y1, fc, ec="none", lw=0.7, ls="-", r=0.04, z=1):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def arrow(ax, x0, y0, x1, y1, color=NAVY, lw=0.8):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=7, shrinkA=0, shrinkB=0))


def image(ax, im, x0, y0, size, frame=None, lw=0.6):
    ax.imshow(im, cmap="gray", vmin=0, vmax=255, extent=(x0, x0 + size, y0, y0 + size),
              interpolation="lanczos", zorder=2)
    if frame:
        ax.add_patch(Rectangle((x0, y0), size, size, fill=False, ec=frame, lw=lw, zorder=3))


def ring(ax, x, y, r, color, lw=1.2, ls="-"):
    ax.add_patch(Circle((x, y), r, fill=False, ec=color, lw=lw, ls=ls, zorder=4))


def crossed_box(ax, x, y, s=0.075, color="#3d6fa8", face="#dce7f3"):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc=face, ec=color, lw=0.8, zorder=5))
    ax.plot([x - s / 2, x + s / 2], [y - s / 2, y + s / 2], color=color, lw=0.7, zorder=6)
    ax.plot([x - s / 2, x + s / 2], [y + s / 2, y - s / 2], color=color, lw=0.7, zorder=6)


def person(ax, x, y, color=NAVY, w=0.16):
    t = np.linspace(0, np.pi, 30)
    ax.add_patch(Polygon(np.c_[x + 0.5 * w * np.cos(t), y + 0.52 * w * np.sin(t)], closed=True,
                         fc=color, ec="none", zorder=4))
    ax.add_patch(Circle((x, y + 0.74 * w), 0.24 * w, fc=color, ec="white", lw=0.5, zorder=4))


def check(ax, x, y, s=0.045, color=BLUE, lw=1.4):
    ax.plot([x - s, x - 0.35 * s, x + s], [y, y - 0.6 * s, y + 0.75 * s], color=color, lw=lw,
            solid_capstyle="round", solid_joinstyle="round", zorder=6)


def snowflake(ax, x, y, r=0.045, color="#7f8e9a"):
    for k in range(3):
        t = np.pi / 2 + k * np.pi / 3
        ax.plot([x - r * np.cos(t), x + r * np.cos(t)], [y - r * np.sin(t), y + r * np.sin(t)],
                color=color, lw=0.8, solid_capstyle="round", zorder=6)
        for sgn in (-1, 1):
            bx, by = x + sgn * 0.58 * r * np.cos(t), y + sgn * 0.58 * r * np.sin(t)
            for dt in (-0.8, 0.8):
                u = t + (0 if sgn > 0 else np.pi) + dt
                ax.plot([bx, bx + 0.42 * r * np.cos(u)], [by, by + 0.42 * r * np.sin(u)],
                        color=color, lw=0.7, solid_capstyle="round", zorder=6)


def title(ax, x, y, letter, s):
    ax.text(x, y, rf"$\bf{{({letter})}}$ {s}", fontsize=8.2, ha="left", va="center", zorder=6)


def lung(cx, cy, rx, ry, side):
    """Closed lung-like outline; side=-1 for the lung on the left of the image, +1 for the right."""
    t = np.linspace(0, 2 * np.pi, 120)
    x, y = np.cos(t), np.sin(t)
    medial = (x * side) < 0
    x = np.where(medial, x * 0.55, x)
    y = y * (1 - 0.18 * (y < 0) * np.clip(x * side, 0, None))
    return np.c_[cx + rx * x, cy + ry * y]


# ------------------------------------------------------------ panels
def panel_a(ax):
    title(ax, 0.02, 4.22, "a", "The problem: nodules hidden in negative labels")
    x0, y0, s = 0.05, 2.42, 1.48
    image(ax, ct(3), x0, y0, s, frame=NAVY)
    r = D.CT[3]["circle_mm"] / 2 / D.CT_FOV_MM * s
    ring(ax, x0 + s / 2, y0 + s / 2, r, AMBER, lw=1.4)

    rows = [("reference target", "#f8ead7", "dot", "nodule present"),
            ("weak annotation", "#efefef", "empty", "nodule unmarked"),
            ("training label", "#dfe9f5", "box", "background")]
    for k, (lab, face, sym, desc) in enumerate(rows):
        y = 3.86 - 0.235 * k
        rbox(ax, 1.62, y - 0.095, 3.10, y + 0.095, face, r=0.05)
        txt(ax, 1.67, y, lab, size=6.2, color=MUTED, ha="left")
        if sym == "dot":
            ax.add_patch(Circle((2.42, y), 0.038, fc=AMBER, ec="#b06a1c", lw=0.6, zorder=5))
        elif sym == "empty":
            ax.add_patch(Circle((2.42, y), 0.038, fc="white", ec="#9aa4ab", lw=0.7, zorder=5))
        else:
            crossed_box(ax, 2.42, y)
        txt(ax, 2.50, y, desc, size=6.4, ha="left")

    # candidate landscape: present but unmarked -> treated as background
    rng = np.random.default_rng(7)
    shapes = [lung(2.08, 2.80, 0.27, 0.33, -1), lung(2.66, 2.80, 0.27, 0.33, +1)]
    for P in shapes:
        ax.add_patch(Polygon(P, closed=True, fc="#f4f7fa", ec="#9aa4ab", lw=0.7, zorder=2))
    pts = []
    while len(pts) < 46:
        p = rng.uniform([1.80, 2.48], [2.95, 3.12])
        if any(Path(P).contains_point(p) for P in shapes):
            pts.append(p)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], "o", ms=1.9, color="#9aa4ab", zorder=3)
    hx, hy = 2.00, 2.90
    ax.add_patch(Circle((hx, hy), 0.024, fc=AMBER, ec="none", zorder=4))
    ring(ax, hx, hy, 0.06, AMBER, lw=1.0)
    arrow(ax, 2.42, 3.29, 2.08, 2.97, color=MUTED)
    txt(ax, 2.74, 3.205, "candidate landscape", size=6.1, color=MUTED)
    txt(ax, 2.37, 2.36, r"present but unmarked $\rightarrow$ background", size=6.1, color=MUTED)


def panel_b(ax):
    title(ax, 0.02, 2.04, "b", "Our solution I: paired-tail audit allocation")
    rbox(ax, 0.05, 0.92, 0.66, 1.40, "#eef2f5", ec=BOX_EDGE, ls=(0, (3, 2)))
    snowflake(ax, 0.355, 1.30)
    txt(ax, 0.355, 1.10, "pilot detector\n(frozen)", size=6.2)

    # candidate patches from real crops: centre crops show the candidate, offset crops do not
    crops = [ct(i) for i in range(4)]

    def patch(i, dx, dy, z=0.46):
        im = crops[i]
        n = im.shape[0]
        w = int(n * z)
        cx, cy = n // 2 + int(dx * n), n // 2 + int(dy * n)
        return im[cy - w // 2:cy + w // 2, cx - w // 2:cx + w // 2]

    top = [(2, 0, 0, AMBER), (0, 0.22, -0.2, None), (1, 0.2, 0.0, AMBER),
           (3, -0.22, 0.2, None), (1, -0.25, -0.25, None), (0, 0.0, 0.0, None)]
    bot = [(3, 0, 0, TEAL), (2, -0.25, 0.22, None), (0, -0.05, 0.05, TEAL),
           (1, 0.25, 0.25, None), (2, 0.22, -0.25, None), (3, 0.2, -0.22, None)]
    s, g = 0.215, 0.035
    for grid, ytop, lab, ylab in ((top, 1.80, "high score", 1.885), (bot, 0.96, "uncertainty & disagreement", 0.40)):
        for k, (i, dx, dy, mark) in enumerate(grid):
            c, rr = k % 3, k // 3
            x0 = 0.84 + c * (s + g)
            y0 = ytop - (rr + 1) * s - rr * g
            image(ax, patch(i, dx, dy), x0, y0, s, frame="#c3ccd3", lw=0.4)
            if mark:
                ring(ax, x0 + s / 2, y0 + s / 2, 0.055, mark, lw=1.0)
        txt(ax, 0.84 + 1.5 * s + g, ylab, lab, size=6.2, color=MUTED)
    arrow(ax, 0.67, 1.24, 0.82, 1.54)
    arrow(ax, 0.67, 1.08, 0.82, 0.72)

    # priority bubbles
    rng = np.random.default_rng(3)
    radii = np.sort(rng.uniform(0.022, 0.095, 24))[::-1]
    placed = []
    cx, cy = 2.10, 1.17
    for r in radii:
        for a in np.linspace(0, 40, 900):
            p = np.array([cx + 0.0045 * a * np.cos(a), cy + 0.0045 * a * np.sin(a)])
            if all(np.hypot(*(p - q)) >= r + rq + 0.006 for q, rq in placed):
                placed.append((p, r))
                break
    for k, (p, r) in enumerate(placed):
        col = TEAL if k < 6 else ("#9fc4c4" if k < 14 else "#d3dde2")
        ax.add_patch(Circle(p, r, fc=col, ec="white", lw=0.4, zorder=3))
    arrow(ax, 1.60, 1.52, 1.74, 1.36)
    arrow(ax, 1.60, 0.74, 1.74, 0.96)
    txt(ax, 2.10, 0.66, r"audit priority $\pi_i$", size=6.3)

    # expert label -> corrected target -> frozen encoder -> linear head
    arrow(ax, 2.50, 1.17, 2.62, 1.17)
    person(ax, 2.77, 1.06)
    check(ax, 2.88, 1.33)
    txt(ax, 2.77, 0.86, "expert\nlabel", size=6.3)
    arrow(ax, 2.93, 1.17, 3.04, 1.17)
    rbox(ax, 3.06, 0.98, 3.36, 1.38, "#fdf6ec", ec="#e3c79d")
    ax.add_patch(Circle((3.21, 1.28), 0.04, fc=AMBER, ec="#b06a1c", lw=0.6, zorder=5))
    crossed_box(ax, 3.21, 1.085)
    arrow(ax, 3.21, 1.13, 3.21, 1.235, color=AMBER, lw=0.7)
    txt(ax, 3.21, 0.84, "corrected\ntarget $z_i$", size=6.3)
    arrow(ax, 3.37, 1.17, 3.44, 1.17)
    enc = np.array([[3.45, 0.90], [3.45, 1.44], [3.80, 1.33], [3.80, 1.01]])
    ax.add_patch(Polygon(enc, closed=True, fc="#eceff1", ec=BOX_EDGE, lw=0.7, ls=(0, (3, 2)), zorder=2))
    snowflake(ax, 3.535, 1.30, r=0.035)
    txt(ax, 3.615, 1.10, "frozen\nencoder", size=5.9)
    arrow(ax, 3.81, 1.17, 3.87, 1.17)
    rbox(ax, 3.88, 1.00, 4.16, 1.34, HEAD_FACE, ec=HEAD_EDGE)
    txt(ax, 4.02, 1.17, "linear\nhead", size=6.0)
    txt(ax, 2.10, 0.13, r"pilot score + uncertainty $\rightarrow$ audit priority $\rightarrow$ expert label"
        r" $\rightarrow$ corrected target $\rightarrow$ linear head", size=6.2, color=MUTED)


def panel_c(fig, ax):
    title(ax, 3.22, 4.22, "c", "Our solution II: score-fixed calibration replay")
    vals = np.array([p["logit"] for p in D.POOL])[::-1]           # rank 67 .. 53
    off = np.array([p["official"] for p in D.POOL])[::-1]
    x = np.arange(len(vals))
    L, R = 3.60, 5.74
    rows = [(3.30, D.T_P, False, MUTED), (2.47, D.T_U, True, BLUE)]
    axes = []
    for y0, cut, drop, col in rows:
        b = fig.add_axes([L / W, y0 / H, (R - L) / W, 0.62 / H])
        for xi, v, o in zip(x, vals, off):
            if drop and o:
                b.bar(xi, v, 0.72, fc="none", ec=PURPLE, lw=0.5, ls=(0, (2, 1.5)), alpha=0.45)
            else:
                b.bar(xi, v, 0.72, color=PURPLE if o else NAVY, lw=0)
        b.axhline(cut, color=col, lw=1.0, ls=(0, (4, 2.4)), zorder=3)
        b.set_xlim(-0.6, len(vals) - 0.4)
        b.set_ylim(0, 3.0)
        b.set_yticks([0, 1, 2, 3])
        b.tick_params(axis="y", labelsize=6.0, pad=1, length=2)
        b.set_xticks([])
        for sp in ("top", "right"):
            b.spines[sp].set_visible(False)
        b.patch.set_alpha(0)
        axes.append(b)
        yl = y0 + cut / 3.0 * 0.62
        txt(ax, 5.80, yl + 0.055, ("original threshold" if not drop else "lower threshold"), size=6.3,
            color=col, ha="left")
        txt(ax, 5.80, yl - 0.065, f"{cut:.2f}", size=6.3, color=col, ha="left")
    top, bot = axes
    top.text(0.99, 0.93, "official consensus nodule", transform=top.transAxes, ha="right", va="top",
             fontsize=6.0, color=PURPLE)
    top.add_patch(Rectangle((0.555, 0.86), 0.022, 0.08, transform=top.transAxes, fc=PURPLE, clip_on=False))
    txt(ax, L, 3.99, "67 negative calibration patients (15 largest maxima)", size=6.3, ha="left")
    bot.text(0.17, 0.97, "53 after excluding official positives", transform=bot.transAxes, ha="left",
             va="top", fontsize=6.3)
    txt(ax, (L + R) / 2, 3.185, "same scores, different negative pool", size=6.2, color=MUTED)
    ax.text(3.33, 3.19, "patient maximum (logit)", rotation=90, fontsize=6.3, ha="center", va="center", zorder=6)
    arrow(ax, 6.60, 3.50, 6.60, 2.72, color=BLUE, lw=1.0)


def panel_d(fig, ax):
    title(ax, 4.30, 2.04, "d", "Consequence: an unchanged nodule is found")
    im = ct(2)
    s = 0.98
    r = D.CT[2]["circle_mm"] / 2 / D.CT_FOV_MM * s
    for k, (x0, cut, col, lab, margin) in enumerate([(4.55, D.T_P, MUTED, "no alert", "$-0.81$"),
                                                     (5.82, D.T_U, BLUE, "alert", "$+0.09$")]):
        image(ax, im, x0, 0.90, s, frame=col if k else NAVY, lw=1.6 if k else 0.6)
        ring(ax, x0 + s / 2, 0.90 + s / 2, r, AMBER, lw=1.3)
        b = fig.add_axes([x0 / W, 0.40 / H, s / W, 0.42 / H])
        b.axhline(cut, color=col, lw=1.0, ls=(0, (4, 2.4)))
        b.plot([0.75], [T_SCORE], "o", ms=3.8, color=BLUE if k else NAVY, mec="white", mew=0.4, zorder=4)
        b.text(0.82, T_SCORE + (0.0 if k == 0 else 0.13), margin, fontsize=6.0, va="center", ha="left",
               color=BLUE if k else NAVY)
        b.text(0.03, cut + (0.08 if k == 0 else -0.08), f"threshold {cut:.2f}", fontsize=5.9, color=col,
               ha="left", va="bottom" if k == 0 else "top")
        b.set_xlim(0, 1)
        b.set_ylim(0.2, 1.8)
        b.set_xticks([])
        b.set_yticks([0.5, 1.0, 1.5])
        b.tick_params(axis="y", labelsize=5.8, pad=1, length=2)
        if k:
            b.set_yticklabels([])
        for sp in ("top", "right"):
            b.spines[sp].set_visible(False)
        b.patch.set_alpha(0)
        txt(ax, x0 + s / 2, 0.29, lab, size=6.6, color=col if k else NAVY)
    ax.text(4.315, 0.61, "score (logit)", rotation=90, fontsize=5.9, ha="center", va="center", zorder=6)
    txt(ax, 5.68, 0.12, "threshold changes; the score stays fixed", size=6.2, color=MUTED)


def main():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_a(ax)
    panel_b(ax)
    panel_c(fig, ax)
    panel_d(fig, ax)
    ax.plot([0.02, W - 0.02], [2.17, 2.17], color="#d5dce1", lw=0.5, zorder=1)
    ax.plot([3.17, 3.17], [2.24, 4.28], color="#d5dce1", lw=0.5, zorder=1)
    ax.plot([4.25, 4.25], [0.02, 2.10], color="#d5dce1", lw=0.5, zorder=1)
    save(fig, "teaser")


if __name__ == "__main__":
    main()
