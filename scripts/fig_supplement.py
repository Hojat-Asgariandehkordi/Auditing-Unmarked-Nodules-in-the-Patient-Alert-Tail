"""Supplement figures redrawn in the main-paper style (data: scripts/data.py)."""
import numpy as np
import matplotlib.pyplot as plt

from style import C, TEXT_W, panel_title, ci_h, save
import data as D


def fig_locked():
    fig, (a, b) = plt.subplots(1, 2, figsize=(TEXT_W, 2.0), gridspec_kw=dict(width_ratios=[1, 1.05], wspace=0.55))
    style = {"paired": (C["paired"], "-", "Paired tail (half)"), "mark_ipw": (C["mark"], "-", "Mark IPW (base)"),
             "mark_same_head": (C["mark"], (0, (3, 1.5)), "Mark, same head (half)"), "first": (C["first"], "-", "First read")}
    for k, (col, ls, lab) in style.items():
        xy = np.array(D.CURVES[k])
        a.plot(xy[:, 0], xy[:, 1], color=col, ls=ls, lw=1.2, marker="o", ms=2.2, label=lab)
        a.plot(*D.NOMINAL[k], "o", ms=5, mfc="white", mec=col, mew=1.1, zorder=4)
    a.set_xlim(0, 20)
    a.set_ylim(0, 33)
    a.set_xlabel("Negative patients alerted (%)")
    a.set_ylabel("Omission recall (%)")
    a.legend(loc="upper left", fontsize=6.6)
    a.text(19.6, 1.2, r"open: nominal $\alpha=0.10$", ha="right", fontsize=6.6, color=C["muted"])
    panel_title(a, "a", "Recall along the alert curve", x=-0.15)

    names = list(D.CONTRAST_OMIT)
    b.axvspan(-18.5, D.NONINF_MARGIN, color="#f6ecec", lw=0)
    b.axvline(D.NONINF_MARGIN, color="#b2182b", lw=0.7, ls=(0, (3, 2)))
    b.axvline(0, color=C["muted"], lw=0.6)
    for i, n in enumerate(names):
        y = len(names) - 1 - i
        col = C["first"] if n == "First read" else C["mark"]
        e, lo, hi = D.CONTRAST_OMIT[n]["nominal"]
        ci_h(b, y + 0.15, lo, hi, e, col)
        e, lo, hi = D.CONTRAST_OMIT[n]["matched"]
        ci_h(b, y - 0.15, lo, hi, e, col, open_=True)
    b.set_yticks(range(len(names)))
    b.set_yticklabels(names[::-1])
    b.tick_params(axis="y", length=0)
    b.set_xlim(-18.5, 3)
    b.set_ylim(-0.6, 2.6)
    b.set_xlabel("Paired tail minus baseline, omission recall (pp)")
    b.plot([], [], "o", color=C["first"], ms=4, label="nominal cutoff")
    b.plot([], [], "o", mfc="white", mec=C["first"], ms=4, label="calibration-matched")
    b.legend(loc="lower right", fontsize=6.6)
    panel_title(b, "b", "Paired effects with 95% patient intervals", x=-0.3)
    save(fig, "locked_performance")


def fig_variability():
    fig, axes = plt.subplots(1, 2, figsize=(TEXT_W, 1.75), gridspec_kw=dict(wspace=0.08))
    rows = [("anchor_patient_ci", "Test patients, one fit", C["first"], "o"),
            ("six_fit_patient_ci", "Test patients, six fits", C["first"], "o"),
            ("audit_draws", "Audit draws", C["paired"], "o"),
            ("anchor_calibration", "Calibration patients", C["image"], "s"),
            ("both_resampled", "Audit + calibration", C["image"], "s")]
    for ax, key, title, letter, xl in ((axes[0], "omission", "Omission recall", "a", (-15.5, 8.5)),
                                       (axes[1], "alerts", "Negative-patient alerts", "b", (-9.5, 4.8))):
        V = D.VARIABILITY[key]
        ax.axvline(0, color=C["muted"], lw=0.6)
        for i, (k, lab, col, mk) in enumerate(rows):
            y = len(rows) - 1 - i
            if k == "audit_draws":
                xs = V[k]
                ax.scatter(xs, y + np.linspace(-0.18, 0.18, len(xs)), s=12, color=col, zorder=3)
            else:
                r = V[k]
                ci_h(ax, y, r["lo"], r["hi"], r["est"], col, marker=mk, ms=4.3)
        ax.set_yticks(range(len(rows)))
        ax.set_yticklabels([r[1] for r in rows][::-1] if letter == "a" else [])
        ax.tick_params(axis="y", length=0)
        ax.set_xlim(*xl)
        ax.set_ylim(-0.6, 4.6)
        ax.set_xlabel("Paired tail minus mark IPW (pp)")
        panel_title(ax, letter, title, x=0.0)
    save(fig, "variability")


if __name__ == "__main__":
    fig_locked()
    fig_variability()
