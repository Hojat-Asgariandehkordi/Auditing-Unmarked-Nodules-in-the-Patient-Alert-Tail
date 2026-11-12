"""Shared figure style: Times text (TeX Gyre Termes), STIX math, Type-42 fonts.

TeX Gyre Termes ships as CFF-based OpenType. Matplotlib embeds CFF fonts poorly in
PDF, so on first use we convert the four Termes faces to TrueType (quadratic
outlines) into scripts/fonts/ (git-ignored) and register them.
"""
from pathlib import Path
import glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
FIG = HERE.parent / "figures"
FONT_DIR = HERE / "fonts"


def _otf_to_ttf(src, dst):
    from fontTools.ttLib import TTFont, newTable
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    f = TTFont(src)
    order = f.getGlyphOrder()
    gs = f.getGlyphSet()
    glyphs = {}
    for name in order:
        pen = TTGlyphPen(gs)
        gs[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyphs[name] = pen.glyph()
    f["loca"] = newTable("loca")
    f["glyf"] = glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = glyphs
    del f["CFF "]
    if "VORG" in f:
        del f["VORG"]
    glyf.compile(f)
    for n, g in glyf.glyphs.items():
        if hasattr(g, "xMin"):
            f["hmtx"][n] = (f["hmtx"][n][0], g.xMin)
    maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    for k in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs",
              "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions",
              "maxComponentElements"):
        setattr(maxp, k, 1 if k == "maxZones" else 0)
    f["maxp"] = maxp
    post = f["post"]
    post.formatType = 2.0
    post.extraNames, post.mapping, post.glyphOrder = [], {}, order
    f.sfntVersion = "\000\001\000\000"
    f.save(dst)


def _register_termes():
    FONT_DIR.mkdir(exist_ok=True)
    srcs = sorted(glob.glob("/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-*.otf")
                  + glob.glob("/usr/share/texlive/texmf-dist/fonts/opentype/public/tex-gyre/texgyretermes-*.otf"))
    for s in srcs:
        dst = FONT_DIR / (Path(s).stem + ".ttf")
        if not dst.exists():
            _otf_to_ttf(s, dst)
    fm = font_manager.fontManager
    # drop the CFF-based system copies so only the TrueType conversions match
    fm.ttflist = [f for f in fm.ttflist if not ("termes" in f.fname.lower() and f.fname.endswith(".otf"))]
    for t in FONT_DIR.glob("*.ttf"):
        fm.addfont(str(t))


_register_termes()

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["TeX Gyre Termes", "Times New Roman", "Times", "Nimbus Roman", "STIXGeneral"],
    "mathtext.fontset": "stix",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.2,
    "axes.linewidth": 0.6,
    "axes.edgecolor": "#5b6770",
    "axes.labelcolor": "#1b262c",
    "xtick.color": "#3d4a52",
    "ytick.color": "#3d4a52",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "legend.frameon": False,
    "savefig.dpi": 300,
    "figure.dpi": 150,
})

# ---- One colour per method / role, used in every figure --------------------
C = {
    "paired": "#17669f",     # paired-tail audit (the proposed policy)
    "image": "#00806f",      # image-tail audit (same ranking, no marks)
    "mark": "#a65c12",       # mark-stratified audit / mark IPW
    "uniform": "#6b7780",    # uniform audit
    "first": "#17293a",      # first-read training
    "official": "#7b3294",   # patients/targets in the official LUNA16 consensus
    "neg": "#17293a",        # patients that stay negative
    "band": "#b9c4ca",       # random-deletion control
    "grid": "#e3e8ea",
    "muted": "#5b6770",
    "shade": "#eef3f6",
}

TEXT_W = 6.875   # CVPR \textwidth in inches (495 pt)
COL_W = 3.25     # CVPR \columnwidth in inches (237 pt)


def panel_title(ax, letter, text, x=0.0, y=1.04, **kw):
    ax.text(x, y, rf"$\bf{{({letter})}}$ {text}", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=8.5, **kw)


def ci_h(ax, y, lo, hi, x, color, open_=False, ms=4.6, lw=1.4, cap=2.6, marker="o", z=3):
    """Horizontal 95% interval with end caps and a point estimate."""
    ax.errorbar([x], [y], xerr=[[x - lo], [hi - x]], fmt="none", ecolor=color,
                elinewidth=lw, capsize=cap, capthick=lw, zorder=z)
    ax.plot([x], [y], marker=marker, ms=ms, mfc="white" if open_ else color,
            mec=color, mew=1.2, zorder=z + 1, ls="none")


def save(fig, name):
    out = FIG / f"{name}.pdf"
    fig.savefig(out, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", out.relative_to(HERE.parent))
