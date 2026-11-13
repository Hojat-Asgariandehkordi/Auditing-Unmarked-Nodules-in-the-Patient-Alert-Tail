"""Every number plotted in the paper, with its source.

Two kinds of source:
  * TABLE: copied from a .tex table or macro in tables/ (printed in the paper).
  * RECOVERED: read back from the vector geometry of the v-received figures by
    scripts/recover_vector.py (stored in scripts/recovered.json). These were not
    printed anywhere and must be confirmed against the analysis ledger.
"""
import json
from pathlib import Path

_REC = json.loads((Path(__file__).resolve().parent / "recovered.json").read_text())

# ---------------------------------------------------------------- acquisition
# TABLE tables/costs.tex, column "Exp. omit." (expected distinct omissions of 92)
# and "Exp. dbl. unmarked" (of 35 double-unmarked omissions).
BUDGET_AUDITS = {  # mean realized candidate audits (thousands), tables/costs.tex "Candidates"
    "paired": (3.940, 7.898), "image": (3.939, 7.892), "mark": (3.942, 7.933), "uniform": (3.938, 7.938)}
REACH = {"paired": (79.4, 84.6), "image": (64.2, 79.7), "mark": (13.0, 23.8), "uniform": (1.4, 2.7)}
REACH_DBL = {"paired": (27.4, 30.2), "image": (22.6, 29.1), "mark": (0.4, 0.9), "uniform": (0.5, 0.9)}
N_OMIT_TRAIN, N_DBL = 92, 35
# RECOVERED: per-draw distinct omissions reached (Fig. 1A points of the original)
DRAWS = _REC["acquisition_draws"]["values"]

# --------------------------------------------------------- cutoff mechanics
# TABLE tables/values.tex: n=67 C/D negatives, k=62, cutoff logit 1.524; n=53, k=49,
# cutoff logit 0.630 (rank 55 in the original pool).
N_P, K_P, T_P = 67, 62, 1.524
N_U, K_U, T_U = 53, 49, 0.630
RANK_U_IN_P = 55
# RECOVERED: the 15 largest C/D-negative calibration maxima of the selected anchor
POOL = _REC["cutoff_pool"]["values"]
# RECOVERED: subset-matched random deletion, central 95% range of the rank drop
DELETION = {d["head"]: d for d in _REC["deletion_control"]["values"]}

# TABLE tables/reference_anchor.tex (omission calls /42, all targets /276,
# alerts /90 common negatives) under C/D -> C/D + official cutoffs, rank drop.
REF_ANCHOR = {
    "Descriptors / first":     dict(omit=(2, 2), all=(39, 55), alert=(7, 12), drop=2),
    "Descriptors / full ref.": dict(omit=(2, 2), all=(47, 57), alert=(7, 10), drop=2),
    "Multi-view / first":      dict(omit=(4, 11), all=(66, 125), alert=(1, 7), drop=6),
    "Multi-view / full ref.":  dict(omit=(3, 11), all=(69, 142), alert=(1, 9), drop=7),
    "3D / first":              dict(omit=(4, 11), all=(81, 133), alert=(0, 5), drop=6),
    "3D / full ref.":          dict(omit=(1, 10), all=(74, 140), alert=(0, 8), drop=7),
    "3D / mark IPW":           dict(omit=(3, 6), all=(70, 91), alert=(2, 6), drop=6),
    "3D / paired tail":        dict(omit=(1, 11), all=(69, 138), alert=(0, 8), drop=7),
}
# RECOVERED (cell labels; three rows also in tables/roles.tex)
READER_PAIRS = _REC["reader_pairs"]["values"]
PAIRS = ["AB", "AC", "AD", "BC", "BD", "CD"]

# ------------------------------------------------------- paired effects
# TABLE tables/reference_effects.tex: selected (half-budget paired-tail disc.)
# minus baseline, pp, six-fit mean, patient bootstrap 95% CI.
#                 baseline: {ref: (est, lo, hi)} for omission / all / alert
REF_EFFECTS = {
    "Mark IPW": {
        "C/D":        dict(omit=(-4.0, -7.0, -1.4), all=(3.0, 1.3, 4.9), alert=(-1.5, -3.1, 0.0)),
        "+ official": dict(omit=(3.6, -1.4, 9.5), all=(6.0, 3.8, 8.4), alert=(1.1, -0.8, 3.4))},
    "Mark, same head": {
        "C/D":        dict(omit=(-4.4, -8.3, -0.8), all=(-1.3, -3.0, 0.4), alert=(-2.0, -4.2, -0.4)),
        "+ official": dict(omit=(4.4, -0.9, 10.0), all=(4.8, 3.0, 6.7), alert=(0.9, -0.7, 2.7))},
    "First read": {
        "C/D":        dict(omit=(-6.3, -15.1, 0.0), all=(-6.2, -9.3, -3.4), alert=(0.7, 0.2, 1.5)),
        "+ official": dict(omit=(-6.0, -12.2, -1.6), all=(-3.8, -6.2, -1.4), alert=(1.7, -0.6, 4.3))},
}
NONINF_MARGIN = -5.0  # prespecified margin on the omission endpoint (methods.tex)

# TABLE tables/contrasts.tex: omission difference, nominal vs calibration-matched
CONTRAST_OMIT = {
    "First read":      dict(nominal=(-6.3, -15.1, 0.0), matched=(-7.1, -17.1, 0.0)),
    "Mark IPW":        dict(nominal=(-4.0, -7.0, -1.4), matched=(-3.6, -7.0, -0.9)),
    "Mark, same head": dict(nominal=(-4.4, -8.3, -0.8), matched=(-2.4, -5.7, 0.8)),
}

# RECOVERED: alert curves (mean alerts %, mean omission recall %)
CURVES = _REC["alert_curves"]["values"]
# TABLE tables/allocations.tex: nominal alpha=0.10 points (alert %, omission %)
NOMINAL = {"paired": (2.5, 3.2), "mark_ipw": (4.3, 7.1), "first": (1.9, 9.5), "mark_same_head": (4.4, 7.5)}

# RECOVERED: variability decomposition (paired tail minus mark IPW, pp)
VARIABILITY = _REC["variability"]["values"]

# ------------------------------------------------------------ CT examples
# Crops are the 521 px rasters embedded in figures/orig/ct_evidence.pdf
# (28.0 mm field of view: 5 mm scale bar = 18.6 pt of 104.2 pt). Text values are
# the original panel labels.
CT = [
    dict(tag="Calibration", title="Sets the C/D threshold", note="rank 62 of 67", kind="neg", circle_mm=6.0),
    dict(tag="Calibration", title="Consensus-positive scan", note="rank 61 of 67", kind="official", circle_mm=6.0),
    dict(tag="Test", title="Found at lower threshold", note="margin $-0.81$ / $+0.09$", kind="gain", circle_mm=5.7),
    dict(tag="Test", title="Persistent miss", note="margin $-6.68$ / $-5.79$", kind="miss", circle_mm=7.7),
]
CT_FOV_MM = 28.0
