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
                ax.text(x + 0.2, y + 0.17, r["marks"][j], fontsize=5.8, color=C["first"], ha="left", va="bottom")
            k += 1
        ax.text(8.0, y, f"+{N_HIDDEN} more:\n{hidden[row]:.1f} audits", fontsize=6.1, color=color,
                ha="left", va="center", linespacing=0.95)
    ax.set_xlim(-0.6, 9.9)
    ax.set_ylim(-0.75, 2.55)
    ax.set_xticks([])
    ax.set_yticks(range(3))
    ax.set_yticklabels(["scan 3", "scan 2", "scan 1"], fontsize=6.6)
    ax.tick_params(axis="y", length=0, pad=1)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title, fontsize=7.6, color=color, pad=2)


def main():
    pi_mark, pi_pair, hid_mark, hid_pair, B = allocate()
    fig = plt.figure(figsize=(TEXT_W, 2.3))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.18], wspace=0.06, left=0.045, right=0.995, bottom=0.2, top=0.81)
    a1, a2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    draw_roster(a1, pi_mark, hid_mark, C["mark"], "Mark-stratified review")
    draw_roster(a2, pi_pair, hid_pair, C["paired"], "Paired-tail review (ours)")
    a2.set_yticklabels([])
    for ax in (a1, a2):
        ax.annotate("", xy=(9.6, -0.68), xytext=(-0.3, -0.68),
                    arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.6, mutation_scale=6))
        ax.text(4.5, -0.72, "image score, high to low", fontsize=6.2, color=C["muted"], ha="center", va="top")
    fig.text(0.045, 0.93, rf"$\bf{{(a)}}$ Which candidates get a second look? (same budget, {B:.1f} expected audits)",
             fontsize=8.3, ha="left", va="bottom")
    fig.text(0.045, 0.005, "Disc area = audit probability. A, B = weak reader marks. Ring = reference nodule "
             "(thick: missed by reader A; number = its audit probability). Toy roster, real allocation rules.",
             fontsize=6.3, color=C["muted"], ha="left", va="bottom")

    # ---------------------------------------------------- (b) the cutoff
    b = fig.add_subplot(gs[2])
    vals_all = [p["logit"] for p in D.POOL]
    off = [p["official"] for p in D.POOL]
    test_score = D.T_P - 0.81          # Fig. 6(c): margin -0.81 to the C/D cutoff, +0.09 to the new one
    rows = [(1.0, "67 C/D-negative patients", D.T_P, False),
            (0.0, "53 left after excluding official positives", D.T_U, True)]
    for y, lab, cut, drop in rows:
        b.plot([0.4, 3.0], [y, y], color=C["band"], lw=0.8, zorder=0)
        for v, o in zip(vals_all, off):
            if drop and o:
                b.plot([v], [y], "D", ms=4.0, mfc="none", mec=C["official"], mew=0.6, alpha=0.45, zorder=2)
                continue
            b.plot([v], [y], "D" if o else "o", ms=4.4 if o else 4.0, color=C["official"] if o else C["neg"],
                   mec="white", mew=0.3, zorder=2)
        col = C["paired"] if drop else C["muted"]
        b.plot([cut, cut], [y - 0.2, y + 0.2], color=col, lw=1.8, zorder=3)
        b.text(cut + 0.04, y + 0.12, f"cutoff {cut:.2f}", ha="left", va="bottom", fontsize=6.5, color=col)
        b.text(0.4, y + 0.36, lab, ha="left", va="bottom", fontsize=6.9, color=C["first"])
        found = test_score > cut
        b.plot([test_score], [y - 0.3], "*", ms=8.5, color=C["paired"] if found else "white",
               mec=C["paired"], mew=0.9, zorder=4)
        b.text(test_score + 0.08, y - 0.3, "test omission: found" if found else "test omission: missed",
               fontsize=6.6, va="center", ha="left", color=C["paired"] if found else C["muted"])
    b.set_xlim(0.38, 3.75)
    b.set_ylim(-0.55, 1.62)
    b.set_yticks([])
    b.spines["left"].set_visible(False)
    b.spines["bottom"].set_bounds(0.4, 3.0)
    b.set_xticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
    b.set_xlabel("Patient maximum (logit), selected detector", labelpad=1, fontsize=7, x=0.38)
    x0 = b.get_position().x0
    fig.text(x0, 0.93, r"$\bf{(b)}$ Which negatives set the alert cutoff?", fontsize=8.3, ha="left", va="bottom")
    for idx, xy, box, col in ((1, (1.42, 1.0), (3.42, 1.12), C["official"]),
                              (2, (test_score, -0.3), (3.42, -0.12), C["paired"])):
        im = np.asarray(Image.open(FIG / "ct" / f"crop-00{idx}.png").convert("L"))[110:410, 110:410]
        ab = AnnotationBbox(OffsetImage(im, cmap="gray", zoom=0.1), xy, xybox=box, xycoords="data",
                            boxcoords="data", pad=0.1, bboxprops=dict(ec=col, lw=1.1),
                            arrowprops=dict(arrowstyle="-", color=col, lw=0.5, shrinkA=0, shrinkB=4,
                                            connectionstyle="arc3,rad=0.0"))
        b.add_artist(ab)
    b.text(3.42, 1.47, "official positive", fontsize=6.1, color=C["official"], ha="center", va="bottom")
    b.text(3.42, 0.23, "test omission", fontsize=6.1, color=C["paired"], ha="center", va="bottom")
    save(fig, "teaser")
    return pi_mark, pi_pair, hid_mark, hid_pair


if __name__ == "__main__":
    pm, pp, hm, hp = main()
    print("hidden audits mark", np.round(hm, 2), "paired", np.round(hp, 2))
    print("omission pi mark", pm[[8, 17]].round(3), "paired", pp[[8, 17]].round(3))
