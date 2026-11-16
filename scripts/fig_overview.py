"""Figure 1: the authors' overview slide (figures/fig1_slide_reference.png), redrawn with all
text in Times.

Layout, wording, colours and the illustrative scores (0.8 / 0.6 / 0.7) follow the slide.
Text, bars, boxes, arrows, bubbles and the candidate landscape are vector. The axial CT
slice is cut from the slide (figures/ct/slide_axial.png) and upscaled; its ring is redrawn
as a vector circle. Patch thumbnails in (B) are cut from the real LUNA16 crops
(figures/ct/crop-00*.png), which are sharper than the slide's thumbnails.

Slide glitches corrected: duplicated "Expert label"/"Corrected target" labels removed;
the overlapping "N_reduced" label set once; the purple (official-positive) bar left in the
reduced pool removed; the second CT in (D) shows the same nodule; the score dots and
threshold lines in (D) are drawn at their labelled values.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle, Ellipse
from PIL import Image

from style import TEXT_W, save, FIG

W, H = TEXT_W, 4.30
LAV, LAV_DARK = "#808ab4", "#3f4777"
PURP = "#9a74a8"
ORANGE, ORANGE_EDGE = "#d39a4c", "#b07a2e"
TEAL, TEAL_TEXT = "#4f8f8f", "#4b8e8a"
GREY_LINE = "#8c8fa6"
BOX_FACE, BOX_EDGE = "#e7edf4", "#9db0cc"
CARD = "#f9eddc"
INK = "#1d1d1f"

# slide bar heights (read from the slide pixels), 29 patients sorted by maximum score
BARS = np.array([1.00, 0.95, 0.91, 0.81, 0.78, 0.75, 0.72, 0.68, 0.68, 0.68, 0.66, 0.65, 0.63, 0.60, 0.57,
                 0.56, 0.56, 0.51, 0.50, 0.50, 0.47, 0.46, 0.38, 0.34, 0.28, 0.28, 0.21, 0.21, 0.09])
PURPLE_IDX = {8, 9, 17, 18}
T_ORIG, T_LOW, SCORE = 0.8, 0.6, 0.7

CT_RING = (40.8, 94.5, 7.4)        # ring centre (x, y) and radius in slide-CT pixels


def slide_ct(rows=None):
    a = np.asarray(Image.open(FIG / "ct" / "slide_axial.png").convert("RGB"))
    if rows:
        a = a[rows[0]:rows[1]]
    big = Image.fromarray(a).resize((a.shape[1] * 4, a.shape[0] * 4), Image.LANCZOS)
    return np.asarray(big), a.shape


def luna(i):
    return np.asarray(Image.open(FIG / "ct" / f"crop-00{i}.png").convert("L"))


# ------------------------------------------------------------ helpers
def txt(ax, x, y, s, size=6.5, color=INK, ha="center", va="center", **kw):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, linespacing=0.95, zorder=6, **kw)


def rbox(ax, x0, y0, x1, y1, fc, ec="none", lw=0.7, r=0.05, z=1):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, zorder=z))


def arrow(ax, x0, y0, x1, y1, color=INK, lw=0.9, rad=0.0, ms=7):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"))


def put_ct(ax, img, shape, x0, y0, w, ring_y_offset=0.0):
    h = w * shape[0] / shape[1]
    ax.imshow(img, extent=(x0, x0 + w, y0, y0 + h), interpolation="antialiased", zorder=2)
    cx, cy, r = CT_RING
    s = w / shape[1]
    ax.add_patch(Circle((x0 + cx * s, y0 + h - (cy - ring_y_offset) * s), r * s, fill=False,
                        ec=ORANGE, lw=1.4, zorder=4))
    return h


def crossed_box(ax, x, y, s=0.075):
    ax.add_patch(Rectangle((x - s / 2, y - s / 2), s, s, fc="#9aa3d6", ec=LAV_DARK, lw=0.6, zorder=5))
    for sg in (1, -1):
        ax.plot([x - s / 2, x + s / 2], [y - sg * s / 2, y + sg * s / 2], color=LAV_DARK, lw=0.6, zorder=6)


def circled_x(ax, x, y, r=0.022):
    ax.add_patch(Circle((x, y), r, fc="#5fa3a0", ec="white", lw=0.4, zorder=5))
    d = r * 0.55
    for sg in (1, -1):
        ax.plot([x - d, x + d], [y - sg * d, y + sg * d], color="white", lw=0.5, zorder=6)


def dot(ax, x, y, r=0.035, fc=ORANGE, ec=ORANGE_EDGE):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=0.5, zorder=5))


def person(ax, x, y, color="#6b6f7a", w=0.15):
    t = np.linspace(0, np.pi, 30)
    ax.add_patch(Polygon(np.c_[x + 0.5 * w * np.cos(t), y + 0.5 * w * np.sin(t)], closed=True,
                         fc=color, ec="none", zorder=4))
    ax.add_patch(Circle((x, y + 0.72 * w), 0.22 * w, fc=color, ec="white", lw=0.5, zorder=4))


def title(ax, x, y, s):
    ax.text(x, y, s, fontsize=8.0, ha="left", va="center", color=INK, zorder=6)


# ------------------------------------------------------------ (A)
def panel_a(ax):
    title(ax, 0.02, 4.21, r"$\mathbf{A}$  The problem: nodules hidden in negative labels")
    img, shape = slide_ct()
    put_ct(ax, img, shape, 0.03, 2.55, 1.62)

    rows = [("Reference target", "#f5ead9", "dot", "nodule present"),
            ("Weak annotation", "white", "faint", "nodule unmarked"),
            ("Training label", "#dfe2f2", "box", "treated as background")]
    for k, (lab, face, sym, desc) in enumerate(rows):
        y = 3.88 - 0.235 * k
        rbox(ax, 1.74, y - 0.095, 3.38, y + 0.095, face, r=0.05)
        txt(ax, 1.79, y, lab, size=6.4, ha="left")
        if sym == "dot":
            dot(ax, 2.47, y)
        elif sym == "faint":
            dot(ax, 2.47, y, fc="#f1f1f3", ec="#e2e2e6")
        else:
            crossed_box(ax, 2.47, y)
        txt(ax, 2.56, y, desc, size=6.4, ha="left")

    # candidate landscape: body outline, two lungs, candidate dots, the unmarked nodule
    cx, cy = 2.56, 2.90
    ax.add_patch(Ellipse((cx, cy), 1.20, 0.62, fc="#e9ebf6", ec="#b9bedf", lw=0.7, zorder=2))
    for side in (-1, 1):
        t = np.linspace(0, 2 * np.pi, 160)
        x = 0.21 * np.cos(t)
        y = 0.22 * np.sin(t)
        x = np.where(x * side < 0, x * 0.55, x)
        P = np.c_[cx + side * 0.24 + x, cy + 0.01 + y]
        ax.add_patch(Polygon(P, closed=True, fc="#f7f8fc", ec="#8f96c4", lw=0.7, zorder=3))
    rng = np.random.default_rng(11)
    pts = []
    while len(pts) < 48:
        p = rng.uniform([cx - 0.56, cy - 0.27], [cx + 0.56, cy + 0.27])
        if ((p[0] - cx) / 0.58) ** 2 + ((p[1] - cy) / 0.29) ** 2 < 1:
            pts.append(p)
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], "o", ms=2.1, color="#9aa3d6", mec="none", zorder=4)
    nx, ny = cx - 0.33, cy - 0.07
    ax.plot([nx], [ny], "o", ms=2.6, color="#9aa3d6", zorder=5)
    ax.add_patch(Circle((nx, ny), 0.045, fill=False, ec=ORANGE, lw=1.0, zorder=5))
    arrow(ax, 2.47, 3.355, nx + 0.04, ny + 0.05, color=INK, lw=0.9, rad=-0.25)
    txt(ax, cx, 2.47, "Candidate landscape", size=6.4)
    txt(ax, cx, 2.35, r"present but unmarked $\rightarrow$ treated as background", size=6.2)


# ------------------------------------------------------------ (C)
def panel_c(fig, ax):
    title(ax, 3.50, 4.21, r"$\mathbf{C}$  Our solution II: score-fixed calibration replay")
    L, R = 3.86, 5.98
    x = np.arange(len(BARS))
    rows = [(3.33, False), (2.43, True)]
    axes = []
    for y0, reduced in rows:
        b = fig.add_axes([L / W, y0 / H, (R - L) / W, 0.64 / H])
        for i, v in zip(x, BARS):
            purple = i in PURPLE_IDX
            if reduced and purple:
                continue
            b.bar(i, v, 0.72, color=PURP if purple else LAV, lw=0, zorder=2)
        if reduced:
            b.bar(0, BARS[0], 0.72, fc="none", ec=LAV_DARK, lw=1.0, zorder=3)
        b.axhline(T_ORIG if not reduced else T_LOW, color=GREY_LINE if not reduced else TEAL, lw=0.9,
                  ls=(0, (3, 2.2)), zorder=3)
        b.set_xlim(-0.7, len(BARS) - 0.3)
        b.set_ylim(0, 1.05)
        b.set_yticks(np.arange(0, 1.01, 0.2))
        b.set_yticklabels([f"{v:.1f}" for v in np.arange(0, 1.01, 0.2)])
        b.tick_params(axis="y", labelsize=6.0, pad=1, length=2)
        b.set_xticks([])
        for sp in ("top", "right"):
            b.spines[sp].set_visible(False)
        b.patch.set_alpha(0)
        axes.append(b)
    top, bot = axes
    bot.get_yticklabels()[4].set_color("#a3a6b5")          # 0.8: the former threshold
    top.text(15.0, 0.97, r"Original negative pool ($N_{\mathrm{neg}}$)", fontsize=6.4, ha="center",
             va="center", color=INK)
    top.annotate("", xy=(16.3, 0.90), xytext=(17.6, 0.58),
                 arrowprops=dict(arrowstyle="-|>", color="#444", lw=0.6, mutation_scale=6, shrinkA=0, shrinkB=0))
    bot.text(15.0, 0.83, r"Different negative pool ($N_{\mathrm{reduced}}$)", fontsize=6.4, ha="center",
             va="center", color=INK)
    txt(ax, 4.72, 3.215, "Same scores", size=6.5)
    ax.text(3.58, 3.18, "Patient Max Detector Score", rotation=90, fontsize=6.4, ha="center", va="center",
            color=INK, zorder=6)

    y_top = 3.33 + T_ORIG / 1.05 * 0.64
    y_low = 2.43 + T_LOW / 1.05 * 0.64
    xa = 6.09
    n = 40
    ys = np.linspace(y_top, y_low + 0.05, n + 1)
    c0, c1 = np.array([0.72, 0.62, 0.78]), np.array([0.31, 0.56, 0.56])
    for k in range(n):
        f = k / (n - 1)
        ax.plot([xa, xa], [ys[k], ys[k + 1]], color=c0 * (1 - f) + c1 * f, lw=1.1, solid_capstyle="butt", zorder=4)
    arrow(ax, xa, y_low + 0.06, xa, y_low - 0.005, color=TEAL, lw=1.1, ms=8)
    ax.plot([R, xa], [y_top, y_top], color=GREY_LINE, lw=0.9, ls=(0, (3, 2.2)), zorder=3)
    ax.plot([R, xa], [y_low, y_low], color=TEAL, lw=0.9, ls=(0, (3, 2.2)), zorder=3)
    txt(ax, 6.17, y_top + 0.02, "Original\nthreshold", size=6.4, ha="left")
    txt(ax, 6.17, (y_top + y_low) / 2 + 0.02, "Lower alert\nthreshold", size=6.4, ha="left")
    txt(ax, 6.17, y_low - 0.08, "Lower\nthreshold\n(0.6)", size=6.4, ha="left", color=TEAL_TEXT)


# ------------------------------------------------------------ (B)
def panel_b(ax):
    title(ax, 0.02, 2.06, r"$\mathbf{B}$  Our solution $\mathbf{I}$: $\mathbf{paired}$-tail $\mathbf{audit}$ allocation")
    rbox(ax, 0.05, 0.92, 0.60, 1.42, BOX_FACE, ec=BOX_EDGE, r=0.07)
    txt(ax, 0.325, 1.22, "Pilot\nDetector", size=7.0)
    txt(ax, 0.325, 1.02, "(frozen)", size=6.0)

    crops = [luna(i) for i in range(4)]

    def patch(i, dx, dy, z=0.5):
        im = crops[i]
        nn = im.shape[0]
        w = int(nn * z)
        cx, cy = nn // 2 + int(dx * nn), nn // 2 + int(dy * nn)
        return im[cy - w // 2:cy + w // 2, cx - w // 2:cx + w // 2]

    s, g = 0.20, 0.03
    gx0 = 0.80
    grids = {
        "top": (1.73, [(2, 0, 0), (1, 0.15, 0), (0, 0.05, 0.05), (3, 0, 0), (0, 0.2, -0.2), (1, -0.2, -0.2)],
                [None] * 6),
        "bot": (0.97, [(0, 0, 0), (2, 0.1, 0.1), (3, -0.1, 0.1), (1, 0.15, 0.05), (2, -0.15, -0.1), (3, 0.1, -0.1)],
                ["o", "o", "x", "o", "x", "x"]),
    }
    for key, (ytop, cells, marks) in grids.items():
        for k, ((i, dx, dy), m) in enumerate(zip(cells, marks)):
            c, rr = k % 3, k // 3
            x0 = gx0 + c * (s + g)
            y0 = ytop - (rr + 1) * s - rr * g
            ax.imshow(patch(i, dx, dy), cmap="gray", vmin=0, vmax=255, extent=(x0, x0 + s, y0, y0 + s),
                      interpolation="antialiased", zorder=2)
            if m == "o":
                dot(ax, x0 + s - 0.045, y0 + 0.045, r=0.028)
            elif m == "x":
                circled_x(ax, x0 + s - 0.045, y0 + 0.045)
    gw = 3 * s + 2 * g
    txt(ax, gx0 + gw / 2, 1.845, "Candidate patches\n(high score)", size=6.2)
    txt(ax, gx0 + gw / 2, 1.13, r"$\vdots$", size=7)
    txt(ax, gx0 + gw / 2, 0.42, "Candidate patches\n(uncertainty & disagreement)", size=6.2)
    arrow(ax, 0.62, 1.30, gx0 - 0.03, 1.62, rad=-0.3)
    arrow(ax, 0.62, 1.04, gx0 - 0.03, 0.62, rad=0.3)
    arrow(ax, gx0 + gw + 0.03, 1.62, 1.70, 1.22, rad=-0.3)
    arrow(ax, gx0 + gw + 0.03, 0.62, 1.70, 1.10, rad=0.3)

    # candidate prioritization bubbles
    rng = np.random.default_rng(5)
    radii = np.sort(rng.uniform(0.025, 0.11, 22))[::-1]
    placed = []
    bx, by = 2.13, 1.16
    for r in radii:
        for a in np.linspace(0, 45, 1200):
            p = np.array([bx + 0.0042 * a * np.cos(a), by + 0.0042 * a * np.sin(a)])
            if all(np.hypot(*(p - q)) >= r + rq + 0.008 for q, rq in placed):
                placed.append((p, r))
                break
    shades = ["#6f9fa2", "#8fb5b7", "#b3cdcf", "#d3e3e4"]
    for k, (p, r) in enumerate(placed):
        ax.add_patch(Circle(p, r, fc=shades[min(3, k // 5)], ec="none", zorder=3))
    txt(ax, bx, 0.64, "candidate-\nprioritization", size=6.2)

    # expert label
    arrow(ax, 2.55, 1.16, 2.66, 1.16)
    txt(ax, 2.88, 1.60, "Expert\nlabel", size=6.4)
    person(ax, 2.77, 1.03)
    rbox(ax, 2.84, 1.02, 3.06, 1.38, "white", ec="#7d8190", lw=0.6, r=0.02, z=3)
    txt(ax, 2.885, 1.29, "+", size=6.5, color=ORANGE_EDGE)
    dot(ax, 2.99, 1.29, r=0.034)
    txt(ax, 2.885, 1.10, r"$-$", size=6.5, color=LAV_DARK)
    crossed_box(ax, 2.99, 1.10, s=0.065)
    arrow(ax, 3.09, 1.16, 3.19, 1.16)
    # corrected target
    txt(ax, 3.33, 1.60, "Corrected\ntarget", size=6.4)
    rbox(ax, 3.21, 0.96, 3.45, 1.42, CARD, ec="none", r=0.04, z=3)
    dot(ax, 3.33, 1.29, r=0.042)
    crossed_box(ax, 3.33, 1.08, s=0.075)
    arrow(ax, 3.48, 1.16, 3.57, 1.16)
    # frozen encoder
    enc = np.array([[3.59, 0.90], [3.59, 1.44], [4.00, 1.36], [4.00, 0.98]])
    ax.add_patch(Polygon(enc, closed=True, fc=BOX_FACE, ec=BOX_EDGE, lw=0.7, zorder=2))
    txt(ax, 3.795, 1.21, "Frozen\nencoder", size=6.6)
    txt(ax, 3.795, 1.03, "(3D features)", size=5.0)
    arrow(ax, 4.02, 1.16, 4.08, 1.16)
    rbox(ax, 4.09, 0.97, 4.38, 1.37, BOX_FACE, ec=BOX_EDGE, r=0.05)
    txt(ax, 4.235, 1.21, "Linear\nhead", size=6.5)
    txt(ax, 4.235, 1.04, "(trained)", size=5.4)
    txt(ax, 3.99, 0.78, "compact pipeline", size=6.2)
    txt(ax, 2.20, 0.12, r"candidate score + uncertainty $\rightarrow$ audit priority $\rightarrow$ expert label"
        r" $\rightarrow$ corrected target $\rightarrow$ linear head", size=6.4)


# ------------------------------------------------------------ (D)
def panel_d(fig, ax):
    title(ax, 4.19, 2.06, r"$\mathbf{D}$  Consequence: an unchanged $\mathbf{nodule}$ becomes detectable")
    img, shape = slide_ct(rows=(10, 145))
    w = 1.12
    for k, (x0, lab) in enumerate([(4.52, "No alert"), (5.72, "Alert")]):
        put_ct(ax, img, shape, x0, 0.98, w, ring_y_offset=10)
        b = fig.add_axes([(x0 + 0.08) / W, 0.40 / H, (w - 0.08) / W, 0.44 / H])
        b.axhline(T_ORIG, color=GREY_LINE, lw=0.9, ls=(0, (3, 2.2)))
        if k == 0:
            b.text(0.5, T_ORIG + 0.04, "Original threshold (0.8)", fontsize=6.0, ha="center", va="bottom", color=INK)
            b.text(0.5, SCORE - 0.12, "0.7", fontsize=6.4, ha="center", va="top", color=TEAL_TEXT)
        else:
            b.axhline(T_LOW, color=TEAL, lw=0.9, ls=(0, (3, 2.2)))
            b.text(0.5, T_LOW - 0.06, "Lower threshold (0.6)", fontsize=6.0, ha="center", va="top", color=TEAL_TEXT)
        b.plot([0.5], [SCORE], "o", ms=4.6, color=LAV, mec="none", zorder=4)
        b.set_xlim(0, 1)
        b.set_ylim(0, 1.05)
        b.set_xticks([])
        b.set_yticks([0.0, 0.5, 1.0])
        b.tick_params(axis="y", labelsize=6.0, pad=1, length=2)
        b.set_ylabel("Score", fontsize=6.4, labelpad=1)
        for sp in ("top", "right"):
            b.spines[sp].set_visible(False)
        b.patch.set_alpha(0)
        txt(ax, x0 + w / 2 + 0.04, 0.29, lab, size=6.8)
    txt(ax, 5.62, 0.12, "Threshold changes; predictions stay fixed.", size=6.4)


def main():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    panel_a(ax)
    panel_c(fig, ax)
    panel_b(ax)
    panel_d(fig, ax)
    save(fig, "teaser")


if __name__ == "__main__":
    main()
