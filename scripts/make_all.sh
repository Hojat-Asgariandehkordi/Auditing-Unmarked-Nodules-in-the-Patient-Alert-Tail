#!/usr/bin/env bash
# Rebuild every figure and both PDFs.  Requires: python3 with matplotlib, numpy,
# pillow, fonttools, pymupdf; TeX Live with latexmk.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -I scripts/recover_vector.py figures/orig   # values not printed in any table
(cd scripts && python3 fig_teaser.py && python3 fig_results.py && python3 fig_supplement.py)
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex supplement.tex
