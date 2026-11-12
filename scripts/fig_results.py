"""Main-paper result figures: acquisition, cutoff, robustness, effects, CT examples."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from PIL import Image
import matplotlib.patheffects as pe

from style import C, TEXT_W, COL_W, panel_title, ci_h, save, FIG
import data as D

LABEL = {"paired": "Paired tail", "image": "Image tail", "mark": "Mark stratified", "uniform": "Uniform"}
MARK = {"paired": "o", "image": "D", "mark": "s", "uniform": "^"}


# ------------------------------------------------------------------ Fig. 2
def fig_acquisition():
    fig, (a, b) = plt.subplots(1, 2, figsize=(COL_W, 1.62), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.62))
    rng = np.random.default_rng(3)
    a.axhline(D.N_OMIT_TRAIN, color=C["muted"], lw=0.6, ls=":")
    a.text(3.3, D.N_OMIT_TRAIN + 1.5, "all 92", fontsize=6.3, color=C["muted"], ha="left", va="bottom")
    for k in ("paired", "image", "mark", "uniform"):
        x = D.BUDGET_AUDITS[k]
        for j, half in enumerate(("half", "base")):
            ys = D.DRAWS[k][half]
            a.scatter(x[j] + rng.uniform(-0.17, 0.17, len(ys)), ys, s=5, color=C[k], alpha=0.35, lw=0, zorder=2)
        a.plot(x, D.REACH[k], color=C[k], lw=1.3, marker=MARK[k], ms=4, mec="white", mew=0.5, zorder=3, label=LABEL[k])
    a.set_xlim(3.2, 8.7)
    a.set_xticks([4, 8])
    a.set_xticklabels(["4\n(half)", "8\n(base)"])
    a.set_ylim(-3, 101)
    a.set_yticks([0, 20, 40, 60, 80])
    a.set_xlabel("Candidate audits (thousands)", labelpad=1)
    a.set_ylabel("Omissions reached (of 92)")
    a.legend(loc="center", bbox_to_anchor=(0.56, 0.43), ncol=2, handlelength=1.2, borderpad=0.1, labelspacing=0.25,
             columnspacing=0.6, handletextpad=0.3, fontsize=6.1)
    panel_title(a, "a", "Expected reach", x=-0.28)

    ks = ["paired", "image", "mark", "uniform"]
    vals = [D.REACH_DBL[k][0] for k in ks]
    yy = np.arange(len(ks))[::-1]
    b.barh(yy, vals, color=[C[k] for k in ks], height=0.62)
    for y, v in zip(yy, vals):
        b.text(v + 0.8, y, f"{v:.1f}", va="center", fontsize=7)
    b.set_yticks(yy)
    b.set_yticklabels([LABEL[k] for k in ks], fontsize=7)
    b.set_xlim(0, D.N_DBL)
    b.set_xticks([0, 10, 20, 30])
    b.set_xlabel("Reached (of 35)", labelpad=1)
    b.tick_params(axis="y", length=0)
    panel_title(b, "b", "Neither reader marked", x=-0.72)
    save(fig, "acquisition")


# ------------------------------------------------------------------ Fig. 4
def fig_cutoff():
    fig = plt.figure(figsize=(TEXT_W, 1.95))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.55, 1, 0.82], wspace=0.42, left=0.06, right=0.99, bottom=0.2, top=0.86)
    a = fig.add_subplot(gs[0])
    pool = D.POOL
    r = [p["rank"] for p in pool]
    v = [p["logit"] for p in pool]
    lo, hi = 62 - D.DELETION["3D / paired tail"]["band_hi"], 62 - D.DELETION["3D / paired tail"]["band_lo"]
    a.axvspan(lo - 0.45, hi + 0.45, color=C["shade"], zorder=0, lw=0)
    a.text((lo + hi) / 2, 2.98, "random removal\nof 14 patients (95%)", ha="center", va="top", fontsize=6.3, color=C["muted"])
    a.plot(r, v, color=C["band"], lw=0.8, zorder=1)
    for p in pool:
        if p["official"]:
            a.plot(p["rank"], p["logit"], "D", ms=4.6, color=C["official"], mec="white", mew=0.4, zorder=3)
        else:
            a.plot(p["rank"], p["logit"], "o", ms=4.4, color=C["neg"], mec="white", mew=0.4, zorder=3)
    a.axhline(D.T_P, color=C["muted"], lw=0.9, ls=(0, (1.5, 1.5)), zorder=1)
    a.axhline(D.T_U, color=C["paired"], lw=0.9, ls=(0, (4, 2)), zorder=1)
    a.text(52.5, D.T_P + 0.05, f"C/D cutoff {D.T_P:.2f} (rank 62 of 67)", fontsize=6.4, color=C["muted"], va="bottom", ha="left")
    a.text(67.6, D.T_U - 0.05, f"+ official cutoff {D.T_U:.2f} (rank 49 of 53)", fontsize=6.4, color=C["paired"], va="top", ha="right")
    for rk, col in ((62, C["muted"]), (D.RANK_U_IN_P, C["paired"])):
        val = [p["logit"] for p in pool if p["rank"] == rk][0]
        a.plot([rk], [val], "o", ms=9, mfc="none", mec=col, mew=1.1, zorder=4)
    a.annotate("", xy=(55.3, 1.3), xytext=(61.7, 1.3),
               arrowprops=dict(arrowstyle="-|>", color=C["paired"], lw=0.9, mutation_scale=7))
    a.text(58.5, 1.33, "7 ranks", fontsize=6.5, color=C["paired"], ha="center", va="bottom")
    a.set_xlim(52.3, 67.7)
    a.set_ylim(0.3, 3.05)
    a.set_xticks([54, 56, 58, 60, 62, 64, 66])
    a.set_xlabel("Rank among the 67 C/D-negative patients", labelpad=1)
    a.set_ylabel("Patient maximum (logit)")
    a.plot([], [], "o", color=C["neg"], ms=4, label="stays negative")
    a.plot([], [], "D", color=C["official"], ms=4, label="official consensus nodule")
    a.legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), fontsize=6.4, handletextpad=0.2, labelspacing=0.2)
    panel_title(a, "a", "Who sets the cutoff? (selected detector, top 15 shown)", x=-0.1)

    heads = [("3D / first", "First read", C["first"]), ("3D / mark IPW", "Mark IPW", C["mark"]),
             ("3D / paired tail", "Paired tail", C["paired"])]
    for ax, key, n, title, letter in ((fig.add_subplot(gs[1]), "omit", 42, "Omissions found (of 42)", "b"),
                                      (fig.add_subplot(gs[2]), "alert", 90, "Negatives alerted (of 90)", "c")):
        for i, (h, lab, col) in enumerate(heads):
            y = len(heads) - 1 - i
            x0, x1 = D.REF_ANCHOR[h][key]
            if lab == "Paired tail":
                ax.axhspan(y - 0.42, y + 0.42, color=C["shade"], lw=0, zorder=0)
            ax.plot([x0, x1], [y, y], color=col, lw=1.4, zorder=2)
            ax.plot([x0], [y], "o", ms=5, mfc="white", mec=col, mew=1.2, zorder=3)
            ax.plot([x1], [y], "o", ms=5, color=col, zorder=3)
            ax.text(x0, y + 0.2, f"{x0}", ha="center", va="bottom", fontsize=6.8, color=col)
            ax.text(x1, y + 0.2, f"{x1}", ha="center", va="bottom", fontsize=6.8, color=col, weight="bold")
        ax.set_yticks(range(len(heads)))
        ax.set_yticklabels([h[1] for h in heads][::-1] if key == "omit" else [])
        ax.tick_params(axis="y", length=0)
        ax.set_ylim(-0.55, 2.7)
        ax.set_xlim(-0.8, 13 if key == "omit" else 10)
        ax.set_xticks([0, 4, 8, 12] if key == "omit" else [0, 3, 6, 9])
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("open: C/D cutoff;  filled: + official", fontsize=6.6, labelpad=1, color=C["muted"])
        panel_title(ax, letter, title, x=-0.02 if key == "alert" else -0.02)
    save(fig, "reference_tail")


# ------------------------------------------------------------------ Fig. 5
def fig_robustness():
    fig = plt.figure(figsize=(TEXT_W, 1.9))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.02], wspace=0.5, left=0.13, right=0.99, bottom=0.17, top=0.88)
    a = fig.add_subplot(gs[0])
    rows = list(D.REF_ANCHOR)
    for i, h in enumerate(rows):
        y = len(rows) - 1 - i
        d = D.DELETION[h]
        a.errorbar([d["band_median"]], [y], xerr=[[d["band_median"] - d["band_lo"]], [d["band_hi"] - d["band_median"]]],
                   fmt="none", ecolor=C["band"], elinewidth=3.2, capsize=0, zorder=1)
        a.plot([d["band_lo"]] * 2, [y - 0.22, y + 0.22], color=C["muted"], lw=0.8)
        a.plot([d["band_hi"]] * 2, [y - 0.22, y + 0.22], color=C["muted"], lw=0.8)
        a.plot([d["band_median"]], [y], "|", ms=7, color=C["muted"], mew=1.0, zorder=2)
        col = C["paired"] if "paired" in h else C["mark"] if "mark" in h else C["first"]
        a.plot([d["drop"]], [y], "o", ms=5, color=col, zorder=3)
    a.axvline(0, color=C["muted"], lw=0.6)
    a.set_yticks(range(len(rows)))
    a.set_yticklabels([h.replace(" / ", " · ") for h in rows][::-1])
    a.tick_params(axis="y", length=0)
    a.set_xlim(-2, 10)
    a.set_xticks([0, 2, 4, 6, 8])
    a.set_xlabel("Cutoff drop (ranks in the original pool)", labelpad=1)
    a.plot([], [], "o", color=C["first"], ms=4, label="official membership")
    a.plot([], [], color=C["band"], lw=3.2, label="random removal, 95% range")
    a.legend(loc="upper right", fontsize=6.4, handlelength=1.4, borderaxespad=0.1)
    panel_title(a, "a", "Removing the 14 patients vs. removing 14 at random", x=-0.42)

    b = fig.add_subplot(gs[1])
    gr = list(D.READER_PAIRS)
    M = np.array([[D.READER_PAIRS[h][p] for p in D.PAIRS] for h in gr])
    b.imshow(M, cmap="Blues", vmin=-2, vmax=16, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            b.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=7.2,
                   color="white" if M[i, j] >= 9 else C["first"])
    b.add_patch(Rectangle((4.5, -0.5), 1, len(gr), fill=False, ec=C["first"], lw=1.1))
    b.set_xticks(range(6))
    b.set_xticklabels(D.PAIRS)
    b.set_yticks(range(len(gr)))
    b.set_yticklabels([h.replace(" / ", " · ") for h in gr])
    b.tick_params(length=0)
    for s in b.spines.values():
        s.set_visible(False)
    b.set_xlabel("Reader pair defining the calibration negatives (CD = original)", labelpad=1)
    panel_title(b, "b", "Omissions found (of 42) for each reader pair", x=-0.38)
    save(fig, "robustness")


# ------------------------------------------------------------------ Fig. 3
def fig_effects():
    fig = plt.figure(figsize=(TEXT_W, 1.85))
    gs = fig.add_gridspec(1, 5, width_ratios=[1.15, 0.36, 1, 1, 1], wspace=0.1, left=0.055, right=0.99, bottom=0.21,
                          top=0.86)
    a = fig.add_subplot(gs[0])
    style = {"paired": (C["paired"], "-", "Paired tail (half)"), "mark_ipw": (C["mark"], "-", "Mark IPW (base)"),
             "mark_same_head": (C["mark"], (0, (3, 1.5)), "Mark, same head (half)"), "first": (C["first"], "-", "First read")}
    for k, (col, ls, lab) in style.items():
        xy = np.array(D.CURVES[k])
        a.plot(xy[:, 0], xy[:, 1], color=col, ls=ls, lw=1.1, marker="o", ms=1.8, label=lab, drawstyle="default")
        nx, ny = D.NOMINAL[k]
        a.plot([nx], [ny], "o", ms=4.8, mfc="white", mec=col, mew=1.1, zorder=4)
    a.set_xlim(0, 20)
    a.set_ylim(0, 33)
    a.set_xticks([0, 5, 10, 15, 20])
    a.set_xlabel("Negative patients alerted (%)", labelpad=1)
    a.set_ylabel("Omission recall (%)")
    a.legend(loc="upper left", fontsize=6.2, handlelength=1.6, labelspacing=0.2, borderaxespad=0.1)
    a.text(19.5, 1.2, "open: nominal $\\alpha=0.10$", fontsize=6.3, ha="right", color=C["muted"])
    panel_title(a, "a", "Recall along the alert curve", x=-0.2)

    base = list(D.REF_EFFECTS)
    refs = [("C/D", C["first"], True), ("+ official", C["official"], False)]
    spec = [("omit", "Omission recall diff. (pp)", (-17, 12), "b"), ("all", "All-target recall diff. (pp)", (-11, 10), "c"),
            ("alert", "Alert-rate diff. (pp)", (-5, 5), "d")]
    for j, (key, lab, xl, letter) in enumerate(spec):
        ax = fig.add_subplot(gs[j + 2])
        if j == 0:
            ax.axvspan(xl[0], D.NONINF_MARGIN, color="#f6ecec", lw=0, zorder=0)
            ax.axvline(D.NONINF_MARGIN, color="#b2182b", lw=0.7, ls=(0, (3, 2)))
            ax.text(D.NONINF_MARGIN - 0.4, 2.62, "margin", fontsize=6.2, color="#b2182b", ha="right", va="center")
        ax.axvline(0, color=C["muted"], lw=0.6)
        for i, bname in enumerate(base):
            y0 = len(base) - 1 - i
            for dy, (ref, col, open_) in zip((0.17, -0.17), refs):
                est, lo, hi = D.REF_EFFECTS[bname][ref][key]
                ci_h(ax, y0 + dy, lo, hi, est, col, open_=open_, marker="o" if open_ else "D", ms=4.2, lw=1.2)
        ax.set_ylim(-0.6, 2.8)
        ax.set_yticks(range(len(base)))
        ax.set_yticklabels(base[::-1] if j == 0 else [])
        if j == 0:
            ax.tick_params(axis="y", length=0, pad=1)
            for t in ax.get_yticklabels():
                t.set_fontsize(7)
        else:
            ax.tick_params(axis="y", length=0)
        ax.set_xlim(*xl)
        ax.set_xticks({"omit": [-15, -10, -5, 0, 5, 10], "all": [-10, -5, 0, 5], "alert": [-4, -2, 0, 2, 4]}[key])
        ax.set_xlabel(lab, labelpad=1)
        panel_title(ax, letter, "Paired tail minus" if j == 0 else "", x=-0.02)
    h1, = fig.axes[1].plot([], [], "o", mfc="white", mec=C["first"], ms=4)
    h2, = fig.axes[1].plot([], [], "D", color=C["official"], ms=4)
    fig.legend([h1, h2], ["cutoff from C/D negatives", "cutoff after excluding official-positive patients"],
               loc="upper right", bbox_to_anchor=(0.995, 1.01), ncol=2, fontsize=6.6, handletextpad=0.25,
               columnspacing=1.0, borderaxespad=0.1)
    save(fig, "effects")


# ------------------------------------------------------------------ Fig. 6
def fig_ct():
    fig, axes = plt.subplots(2, 2, figsize=(COL_W, 3.2), gridspec_kw=dict(wspace=0.06, hspace=0.42))
    axes = axes.ravel()
    frame = {"neg": C["neg"], "official": C["official"], "gain": C["paired"], "miss": C["muted"]}
    for i, (ax, d) in enumerate(zip(axes, D.CT)):
        im = np.asarray(Image.open(FIG / "ct" / f"crop-00{i}.png").convert("L"))
        n = im.shape[0]
        ax.imshow(im, cmap="gray", vmin=0, vmax=255, extent=(0, D.CT_FOV_MM, D.CT_FOV_MM, 0))
        c = D.CT_FOV_MM / 2
        ax.add_patch(Circle((c, c), d["circle_mm"] / 2, fill=False, ec="#f6d860", lw=1.0))
        stroke = [pe.withStroke(linewidth=2.2, foreground="#1b262c")]
        ax.plot([1.6, 6.6], [D.CT_FOV_MM - 2.2] * 2, color="white", lw=2.0, solid_capstyle="butt",
                path_effects=[pe.Stroke(linewidth=3.4, foreground="#1b262c"), pe.Normal()])
        ax.text(4.1, D.CT_FOV_MM - 3.0, "5 mm", color="white", ha="center", va="bottom", fontsize=6.6,
                path_effects=stroke)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(True)
            s.set_color(frame[d["kind"]])
            s.set_linewidth(1.6 if d["kind"] in ("official", "gain") else 0.6)
        ax.set_title(rf"$\bf{{({'abcd'[i]})}}$ {d['tag']}" + "\n" + d["title"], fontsize=7.2, pad=3, loc="left",
                     linespacing=1.0)
        ax.text(0.5, -0.07, d["note"], transform=ax.transAxes, ha="center", va="top", fontsize=7)
    save(fig, "ct_evidence")


if __name__ == "__main__":
    fig_acquisition()
    fig_cutoff()
    fig_robustness()
    fig_effects()
    fig_ct()
