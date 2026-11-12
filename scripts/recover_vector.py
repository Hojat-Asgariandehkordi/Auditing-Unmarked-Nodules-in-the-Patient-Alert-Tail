"""Recover plotted values from the vector geometry of the v-received figures.

The source package had no plotting scripts or analysis ledger, so numbers that are
plotted but not printed in any table are read back from the original PDFs in
figures/orig/. Axes are calibrated from the tick labels; every value is rounded to
the resolution implied by its definition (counts to integers, recall on 42
omissions to multiples of 1/42, etc.) and cross-checked against numbers printed in
the text where possible. Output: scripts/recovered.json.

**These values must be confirmed against the analysis output by the authors.**
Run:  python -I scripts/recover_vector.py figures/orig
"""
import json
import sys
from pathlib import Path

import pymupdf

ORIG = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures" / "orig")
OUT = Path(__file__).resolve().parent / "recovered.json"


def page(name):
    return pymupdf.open(ORIG / f"{name}.pdf")[0]


def spans(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                x0, y0, x1, y1 = s["bbox"]
                out.append((s["text"].strip(), (x0 + x1) / 2, (y0 + y1) / 2))
    return out


def num(t):
    try:
        return float(t.replace("−", "-"))
    except ValueError:
        return None


def ticks(pg):
    """Short grey tick segments drawn by matplotlib: (orientation, x, y)."""
    out = []
    for d in pg.get_drawings():
        r = d["rect"]
        if d.get("fill") and len(d["items"]) == 1 and d["items"][0][0] == "l":
            if r.width < 0.1 and 2 < r.height < 4:
                out.append(("x", (r.x0 + r.x1) / 2, r.y1))
            elif r.height < 0.1 and 2 < r.width < 4:
                out.append(("y", r.x1, (r.y0 + r.y1) / 2))
    return out


def axis(pg, kind, xlim=None, ylim=None):
    """Linear map from page coordinate to data value, from labels next to ticks."""
    pts = []
    tk = ticks(pg)
    for t, x, y in spans(pg):
        v = num(t)
        if v is None:
            continue
        if kind == "x":
            if xlim and not (xlim[0] <= x <= xlim[1]):
                continue
            cand = [tx for o, tx, ty in tk if o == "x" and abs(tx - x) < 1.5 and 0 < y - ty < 12]
            if cand:
                pts.append((cand[0], v))
        else:
            if ylim and not (ylim[0] <= x <= ylim[1]):
                continue
            cand = [ty for o, tx, ty in tk if o == "y" and abs(ty - y) < 1.5 and 0 < tx - x < 16]
            if cand:
                pts.append((cand[0], v))
    pts = sorted(set(pts))
    assert len(pts) >= 2, (kind, pts)
    (p0, v0), (p1, v1) = pts[0], pts[-1]
    a = (v1 - v0) / (p1 - p0)
    return lambda p: v0 + a * (p - p0)


def markers(pg, fill=None, size=None, kinds=None, xlim=(0, 1e9)):
    out = []
    for d in pg.get_drawings():
        k = "".join(i[0] for i in d["items"])
        r = d["rect"]
        cx, cy = (r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2
        if not (xlim[0] <= cx <= xlim[1]):
            continue
        if kinds and k != kinds:
            continue
        if size and abs(r.width - size) > 0.3:
            continue
        f = tuple(round(c, 2) for c in d["fill"]) if d.get("fill") else None
        if fill is not None and f != fill:
            continue
        out.append(dict(cx=cx, cy=cy, x0=r.x0, x1=r.x1, color=tuple(round(c, 2) for c in d["color"]) if d.get("color") else None, fill=f, w=r.width, kinds=k))
    return out


def hlines(pg, color, width, xlim=(0, 1e9)):
    out = []
    for d in pg.get_drawings():
        r = d["rect"]
        c = tuple(round(v, 2) for v in d["color"]) if d.get("color") else None
        if c == color and d.get("width") and abs(d["width"] - width) < 0.05 and r.height < 0.1 \
                and xlim[0] <= (r.x0 + r.x1) / 2 <= xlim[1]:
            out.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    return out


R = {"_note": "Recovered from vector geometry of figures/orig/*.pdf by scripts/recover_vector.py. "
              "Confirm against the analysis ledger before submission."}

# ---------------------------------------------------------------- acquisition
pg = page("acquisition")
fx = axis(pg, "x", xlim=(0, 300))
fy = axis(pg, "y", ylim=(0, 60))
cols = {"paired": (0.09, 0.4, 0.64), "image": (0.0, 0.5, 0.45),
        "mark": (0.64, 0.36, 0.07), "uniform": (0.41, 0.47, 0.52)}
draws = {}
for k, col in cols.items():
    pts = [m for m in markers(pg, fill=col, size=3.7, xlim=(40, 300))]
    half = sorted(round(fy(m["cy"])) for m in pts if fx(m["cx"]) < 6)
    base = sorted(round(fy(m["cy"])) for m in pts if fx(m["cx"]) > 6)
    draws[k] = {"half": half, "base": base}
R["acquisition_draws"] = {"what": "distinct training omissions (of 92) reached in each of six matched audit draws",
                          "source": "Fig. 1A small points (orig acquisition.pdf)", "values": draws}

# ------------------------------------------------------------- reference_tail
pg = page("reference_tail")
fx = axis(pg, "x", xlim=(40, 200))
fy = axis(pg, "y", ylim=(0, 46))
pool = []
for m in markers(pg, xlim=(47, 180)):
    if m["fill"] == (0.09, 0.17, 0.22) and abs(m["w"] - 5.0) < 0.2 and 65 < m["cy"] < 160 and m["cx"] > 50:
        pool.append({"rank": round(fx(m["cx"])), "logit": round(fy(m["cy"]), 2), "official": False})
    if m["fill"] == (0.64, 0.36, 0.07) and m["kinds"] == "llll" and m["cx"] > 70:
        pool.append({"rank": round(fx(m["cx"])), "logit": round(fy(m["cy"]), 2), "official": True})
pool = sorted(pool, key=lambda d: d["rank"])
R["cutoff_pool"] = {"what": "selected-anchor maxima of C/D-negative calibration patients near the cutoff "
                            "(rank in the original pool of 67; official = has an official LUNA16 consensus nodule)",
                    "source": "Fig. 2A (orig reference_tail.pdf); ranks 62 and 55 match \\PRank and \\PairRank, "
                              "logits at those ranks match \\PairCutoffP=1.524 and \\PairCutoffU=0.630 to 0.01",
                    "values": pool}

# ----------------------------------------------------------------- robustness
pg = page("robustness")
fx = axis(pg, "x", xlim=(100, 260))
rows = ["Descriptors / first", "Descriptors / full ref.", "Multi-view / first", "Multi-view / full ref.",
        "3D / first", "3D / full ref.", "3D / mark IPW", "3D / paired tail"]
bands = sorted(hlines(pg, (0.67, 0.74, 0.77), 2.2), key=lambda b: b[2])
meds = sorted([(m["cx"], m["cy"]) for m in markers(pg, fill=(0.31, 0.39, 0.44), xlim=(100, 260))], key=lambda t: t[1])
dots = sorted([m for m in markers(pg, size=6.0, kinds="cccccccc", xlim=(100, 260))], key=lambda m: m["cy"])
rob = []
for name, b, md, dt in zip(rows, bands, meds, dots):
    rob.append({"head": name, "drop": round(fx(dt["cx"])), "band_lo": round(fx(b[0])),
                "band_hi": round(fx(b[1])), "band_median": round(fx(md[0]))})
R["deletion_control"] = {"what": "observed cutoff rank drop and central 95% range / median of the drop under "
                                 "8,192 subset-matched random deletions",
                         "source": "Fig. 3A (orig robustness.pdf); drops match Tab. 2, paired-tail band "
                                   "matches \\PairRobustMedian=0 and \\PairControlHi=4",
                         "values": rob}
grid_rows = ["Descriptors / first", "Multi-view / first", "3D / first", "3D / full ref.", "3D / mark IPW", "3D / paired tail"]
pairs = ["AB", "AC", "AD", "BC", "BD", "CD"]
cells = [(t, x, y) for t, x, y in spans(pg) if x > 350 and y < 175 and num(t) is not None]
ys = sorted({round(y, 1) for _, _, y in cells})
xs = sorted({round(x, 0) for _, x, _ in cells})
grid = {r: {} for r in grid_rows}
for t, x, y in cells:
    grid[grid_rows[ys.index(round(y, 1))]][pairs[xs.index(round(x, 0))]] = int(num(t))
R["reader_pairs"] = {"what": "omission calls (of 42) after calibrating on the negatives of each reader pair",
                     "source": "Fig. 3B cell labels (orig robustness.pdf); first-read / mark IPW / paired-tail "
                               "rows match supplement Tab. roles", "values": grid}

# ------------------------------------------------------- locked_performance
pg = page("locked_performance")
fx = axis(pg, "x", xlim=(40, 240))
fy = axis(pg, "y", ylim=(0, 50))
curves = {}
names = {((0.09, 0.4, 0.64), False): "paired", ((0.64, 0.36, 0.07), False): "mark_ipw",
         ((0.09, 0.17, 0.22), False): "first", ((0.64, 0.36, 0.07), True): "mark_same_head"}
for d in pg.get_drawings():
    it = d["items"]
    if d.get("color") and len(it) > 3 and all(i[0] == "l" for i in it):
        col = tuple(round(c, 2) for c in d["color"])
        dashed = bool(d.get("dashes") and d["dashes"].strip("[] 0"))
        key = names.get((col, dashed))
        if key:
            pts = [it[0][1]] + [i[2] for i in it]
            seen, xy = set(), []
            for p in pts:
                k = (round(p.x, 2), round(p.y, 2))
                if k not in seen:
                    seen.add(k)
                    xy.append([round(fx(p.x), 2), round(fy(p.y), 2)])
            curves[key] = xy
nominal = {}
for m in markers(pg, fill=(1.0, 1.0, 1.0), size=5.7, xlim=(40, 240)):
    key = {(0.09, 0.4, 0.64): "paired", (0.09, 0.17, 0.22): "first"}.get(m["color"])
    if key is None:
        key = "mark_ipw" if m["cx"] < 92 else "mark_same_head"
    nominal[key] = [round(fx(m["cx"]), 2), round(fy(m["cy"]), 2)]
R["alert_curves"] = {"what": "mean realized negative-patient alerts (%) vs mean observed-omission recall (%) "
                             "over calibration-derived cutoffs, six matched fits",
                     "source": "supplement Fig. locked_performance A (orig); nominal points match Tab. 1 "
                               "(paired 2.5/3.2, mark IPW 4.3/7.1, first read 1.9/9.5) to 0.1",
                     "values": curves, "nominal": nominal}

# ---------------------------------------------------------------- variability
pg = page("variability")
out = {}
for panel, xl in (("omission", (130, 300)), ("alerts", (330, 500))):
    fx = axis(pg, "x", xlim=xl)
    lines = sorted(hlines(pg, (0.09, 0.17, 0.22), 1.65, xlim=xl) + hlines(pg, (0.0, 0.5, 0.45), 1.65, xlim=xl),
                   key=lambda b: b[2])
    pts = markers(pg, xlim=xl)
    rowsv = {}
    labels = {43.4: "anchor_patient_ci", 62.5: "six_fit_patient_ci", 100.9: "anchor_calibration", 120.0: "both_resampled"}
    for x0, x1, y in lines:
        name = labels[min(labels, key=lambda k: abs(k - y))]
        est = [m for m in pts if abs(m["cy"] - y) < 0.5 and 4.5 < m["w"] < 6][0]
        rowsv[name] = {"est": round(fx(est["cx"]), 2), "lo": round(fx(x0), 2), "hi": round(fx(x1), 2)}
    rowsv["audit_draws"] = sorted(round(fx(m["cx"]), 2) for m in pts if 78 < m["cy"] < 85 and abs(m["w"] - 4.8) < 0.2)
    out[panel] = rowsv
R["variability"] = {"what": "paired tail minus mark IPW (pp) under different sources of variation",
                    "source": "supplement Fig. variability (orig); six-fit CI matches [-7.0,-1.4]; "
                              "both-resampled matches the text's -14.3 to +7.1",
                    "values": out}

OUT.write_text(json.dumps(R, indent=1))
print("wrote", OUT)
print(json.dumps({k: v.get("values") for k, v in R.items() if isinstance(v, dict)}, indent=None)[:3000])
