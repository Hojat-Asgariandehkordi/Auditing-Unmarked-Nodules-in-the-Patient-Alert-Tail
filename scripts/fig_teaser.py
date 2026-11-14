"""Figure 1: the two questions of the paper.

(a) runs the paper's allocation rules (Eqs. 1-2 and the mark-stratified rule) on a
    small synthetic roster, so the disc sizes are the real rule, not a sketch.
(b) uses the selected detector's real calibration maxima (scripts/data.py) and two
    of the CT crops; only the layout is schematic.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

from style import C, TEXT_W, save, FIG
import data as D

# ----------------------------------------------------------- synthetic roster
T0 = 2.0   # frozen pilot cutoff (logit)
# per scan: scores (descending), marks per candidate ("", "A", "B", "AB"),
# nodule flags, and the out-of-fold image probability of a weak mark p_i
ROSTER = [
    dict(s=[2.6, 1.2, 0.4, -0.3, -0.9, -1.5, -2.0, -2.6], marks=["AB", "", "", "", "A", "", "", ""],
         nod=[1, 0, 0, 0, 0, 0, 0, 0], p=[.9, .3, .1, .08, .2, .05, .04, .03]),
    dict(s=[1.8, 1.0, 0.2, -0.4, -1.1, -1.6, -2.2, -2.9], marks=["B", "", "", "", "", "", "", ""],
         nod=[1, 0, 0, 0, 0, 0, 0, 0], p=[.6, .2, .1, .1, .05, .05, .03, .02]),
    dict(s=[0.9, 0.6, -0.1, -0.7, -1.2, -1.8, -2.3, -3.0], marks=["", "", "", "", "", "B", "", ""],
         nod=[0, 1, 0, 0, 0, 0, 0, 0], p=[.25, .3, .1, .1, .05, .25, .03, .02]),
]
B_FACTOR = 1.0
N_HIDDEN = 250   # unremarkable low-ranked candidates per scan (not drawn; real scans have ~250)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def allocate():
    """Returns per-candidate pi for the drawn candidates plus the expected number of
    audits each policy spends on the hidden tail of each scan."""
    s, rank, m, p, shown = [], [], [], [], []
    for r in ROSTER:
        n = len(r["s"])
        s += list(r["s"]) + list(np.linspace(-3.2, -8, N_HIDDEN))
        rank += list(range(1, n + N_HIDDEN + 1))
        m += [len(x) for x in r["marks"]] + [0] * N_HIDDEN
        p += list(r["p"]) + [0.02] * N_HIDDEN
        shown += [True] * n + [False] * N_HIDDEN
    s, rank, m, p, shown = map(np.array, (s, rank, m, p, shown))
    # mark-stratified rule; its expected count sets the common budget B
    pi_mark = np.array([0.02, 0.35, 0.20])[m] * B_FACTOR
    B = pi_mark.sum()
    # paired tail: Eq. (1) leverage and the working probability of Sec. 3.2
    h = np.maximum(np.exp(-(rank - 1) / 6), sigmoid((s - T0 + 1) / 0.7))
    hb = np.maximum(h, 0.002)
    u = np.where(m == 0, 0.35 * p, np.where(m == 1, 0.55 + 0.35 * p, 0.92 + 0.06 * p))
    v = np.maximum(u * (1 - u), 0.006)
    lo, hi = 0.005 * B_FACTOR, 0.95
    a, b = 1e-6, 1e3
    for _ in range(200):   # bisection on c so that sum(pi) = B
        c = (a + b) / 2
        if np.clip(c * hb * np.sqrt(v), lo, hi).sum() > B:
            b = c
        else:
            a = c
    pi_pair = np.clip(c * hb * np.sqrt(v), lo, hi)
    hid = lambda pi: [pi[~shown][i * N_HIDDEN:(i + 1) * N_HIDDEN].sum() for i in range(len(ROSTER))]
    return pi_mark[shown], pi_pair[shown], hid(pi_mark), hid(pi_pair), B


def draw_roster(ax, pi, hidden, color, title):
    k = 0
    for row, r in enumerate(ROSTER):
        y = len(ROSTER) - 1 - row
        for j in range(len(r["s"])):
            x = j
            ax.scatter([x], [y], s=165 * pi[k], color=color, alpha=0.30, lw=0, zorder=1)
            ax.scatter([x], [y], s=165 * pi[k], facecolor="none", edgecolor=color, lw=0.6, zorder=1)
            ax.plot([x], [y], "o", ms=2.6, color=C["muted"], zorder=3)
            if r["nod"][j]:
                omitted = "A" not in r["marks"][j]
                ax.plot([x], [y], "o", ms=8.5, mfc="none", mec=C["official"], mew=1.3 if omitted else 0.8,
                        ls="none", zorder=4)
                if omitted:
                    ax.text(x, y - 0.36, f"{pi[k]:.2f}", ha="center", va="top", fontsize=6.6,
                            color=color, weight="bold")
            if r["marks"][j]:
                ax.text(x + 0.2, y + 0.17, r["marks"][j], fontsize=6.5, color=C["first"], ha="left", va="bottom")
            k += 1
        ax.text(8.0, y, f"+{N_HIDDEN} more:\n{hidden[row]:.1f} audits", fontsize=6.6, color=color,
                ha="left", va="center", linespacing=0.95)
    ax.set_xlim(-0.6, 9.9)
    ax.set_ylim(-0.75, 2.55)
    ax.set_xticks([])
    ax.set_yticks(range(3))
    ax.set_yticklabels(["scan 3", "scan 2", "scan 1"], fontsize=7)
    ax.tick_params(axis="y", length=0, pad=1)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title, fontsize=7.6, color=color, pad=2)


def pipeline(ax):
    """(c) What is frozen, trained, calibrated and tested."""
    from matplotlib.patches import FancyBboxPatch
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 10)
    ax.axis("off")
    stages = [(0, 60.8, "training: 445 patients", "#eef3f6"), (61.8, 86.2, "calibration: 175 patients", "#f3eef6"),
              (87.2, 100, "test: 265 patients", "#eef6f1")]
    for x0, x1, lab, col in stages:
        ax.add_patch(FancyBboxPatch((x0, 0.2), x1 - x0, 9.4, boxstyle="round,pad=0,rounding_size=0.8",
                                    fc=col, ec="none", zorder=0))
        ax.text((x0 + x1) / 2, 0.9, lab, ha="center", va="bottom", fontsize=6.6, color=C["muted"], style="italic")
    boxes = [
        (6.0, "pilot detector\n(frozen): $s_i$, $r_i$", True),
        (18.0, "leverage $h_i$ and\ndisagreement $v_i$", False),
        (30.0, "audit $R_i$ with\nprob. $\\pi_i$ (Eq. 3)", False),
        (42.0, "3D encoder\n(frozen): $X_i$", True),
        (54.4, "linear head $g$\ntrained on $z_i$ (Eq. 5)", False),
        (68.0, "patient score $S_j$:\nmax of $g$ in scan $j$", False),
        (80.0, "threshold $T$ from\nnegatives $P$ or $U$", False),
        (93.6, "omissions found,\nnegatives alerted", False),
    ]
    w, h, y = 11.0, 5.0, 3.0
    for i, (x, txt, frozen) in enumerate(boxes):
        ax.add_patch(FancyBboxPatch((x - w / 2, y), w, h, boxstyle="round,pad=0,rounding_size=0.6",
                                    fc="white", ec=C["muted"], lw=0.9 if frozen else 0.6,
                                    ls=(0, (2, 1.2)) if frozen else "-", zorder=2))
        ax.text(x, y + h / 2, txt, ha="center", va="center", fontsize=6.6, color=C["first"], zorder=3,
                linespacing=1.05)
        if i < len(boxes) - 1:
            x2 = boxes[i + 1][0]
            ax.annotate("", xy=(x2 - w / 2 - 0.2, y + h / 2), xytext=(x + w / 2 + 0.2, y + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.7, mutation_scale=6), zorder=1)


def main():
    pi_mark, pi_pair, hid_mark, hid_pair, B = allocate()
    fig = plt.figure(figsize=(TEXT_W, 2.85))
    gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1.18], height_ratios=[1, 0.34], wspace=0.06, hspace=0.62,
                          left=0.045, right=0.995, bottom=0.005, top=0.87)
    a1, a2 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
    draw_roster(a1, pi_mark, hid_mark, C["mark"], "Mark-stratified review")
    draw_roster(a2, pi_pair, hid_pair, C["paired"], "Paired-tail review (ours)")
    a2.set_yticklabels([])
    for ax in (a1, a2):
        ax.annotate("", xy=(9.6, -0.68), xytext=(-0.3, -0.68),
                    arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.6, mutation_scale=6))
        ax.text(4.5, -0.72, "image score, high to low", fontsize=6.6, color=C["muted"], ha="center", va="top")
    fig.text(0.045, 0.935, rf"$\bf{{(a)}}$ Which candidates get a second look? (equal budget, {B:.1f} expected audits)",
             fontsize=8.3, ha="left", va="bottom")

    # ---------------------------------------------------- (b) the cutoff
    b = fig.add_subplot(gs[0, 2])
    vals_all = [p["logit"] for p in D.POOL]
    off = [p["official"] for p in D.POOL]
    test_score = D.T_P - 0.81          # Fig. 6(c): margin -0.81 to the C/D cutoff, +0.09 to the new one
    rows = [(1.0, "67 C/D-negative patients", D.T_P, False),
            (0.0, "53 after excluding official positives", D.T_U, True)]
    for y, lab, cut, drop in rows:
        b.plot([0.4, 3.0], [y, y], color=C["band"], lw=0.8, zorder=0)
        for v, o in zip(vals_all, off):
            if drop and o:
                b.plot([v], [y], "D", ms=4.0, mfc="none", mec=C["official"], mew=0.6, alpha=0.4, zorder=2)
                continue
            b.plot([v], [y], "D" if o else "o", ms=4.6 if o else 4.2, color=C["official"] if o else C["neg"],
                   mec="white", mew=0.3, zorder=2)
        col = C["paired"] if drop else C["muted"]
        b.plot([cut, cut], [y - 0.2, y + 0.2], color=col, lw=1.8, zorder=3)
        b.text(cut, y + 0.24, f"threshold {cut:.2f}", ha="center", va="bottom", fontsize=6.7, color=col)
        b.text(3.0, y + 0.24, lab, ha="right", va="bottom", fontsize=6.9, color=C["first"])
        found = test_score > cut
        b.plot([test_score], [y - 0.32], "*", ms=9, color=C["paired"] if found else "white",
               mec=C["paired"], mew=0.9, zorder=4)
        b.text(test_score + 0.09, y - 0.32, "test omission found" if found else "test omission missed",
               fontsize=6.9, va="center", ha="left", color=C["paired"] if found else C["muted"])
    b.set_xlim(0.38, 3.05)
    b.set_ylim(-0.62, 1.95)
    b.set_yticks([])
    b.spines["left"].set_visible(False)
    b.spines["bottom"].set_bounds(0.4, 3.0)
    b.set_xticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    b.tick_params(axis="x", labelsize=6.8, pad=1)
    b.set_xlabel("patient maximum (logit), selected detector", labelpad=1, fontsize=6.9)
    x0 = b.get_position().x0
    fig.text(x0, 0.935, r"$\bf{(b)}$ Which negatives set the alert threshold?", fontsize=8.3, ha="left", va="bottom")
    # CT crops: the official-positive maximum (rank 61, directly above its point) and the recovered omission
    for idx, xy, box, col in ((1, (1.42, 1.0), (0.86, 1.62), C["official"]),
                              (2, (test_score, -0.32), (2.62, -0.32), C["paired"])):
        im = np.asarray(Image.open(FIG / "ct" / f"crop-00{idx}.png").convert("L"))[110:410, 110:410]
        arrow = dict(arrowstyle="-", color=col, lw=0.6, shrinkA=0, shrinkB=3) if idx == 1 else None
        ab = AnnotationBbox(OffsetImage(im, cmap="gray", zoom=0.085), xy, xybox=box, xycoords="data",
                            boxcoords="data", pad=0.08, bboxprops=dict(ec=col, lw=1.1), arrowprops=arrow)
        b.add_artist(ab)
    # leader from the recovered-omission star down and across to its crop (the crop is not on the score axis)
    b.plot([test_score, test_score, 2.36], [-0.42, -0.56, -0.56], color=C["paired"], lw=0.6, zorder=1)

    c = fig.add_subplot(gs[1, :])
    pipeline(c)
    fig.text(0.045, c.get_position().y1 + 0.012, r"$\bf{(c)}$ Pipeline: dashed boxes are frozen before auditing; the replay in (b) changes only the negatives that set $T$",
             fontsize=8.3, ha="left", va="bottom")
    save(fig, "teaser")
    return pi_mark, pi_pair, hid_mark, hid_pair


if __name__ == "__main__":
    pm, pp, hm, hp = main()
