# Build

This project follows the official **CVPR 2027 author kit** (`author-kit-CVPR2027-v1-latex`):
`cvpr.sty` and `ieeenat_fullname.bst` are the unmodified kit files, `main.tex` is the kit's
skeleton, and `preamble.tex` is the kit's preamble with this paper's extra packages appended.

| File | Role |
|---|---|
| `main.tex` | Main paper (review mode). With `\input{sec/X_suppl}` uncommented, main paper and supplement in one PDF. Overleaf "Main document". |
| `supplement.tex` | Supplement alone, as the separate supplementary PDF (pages start at 1). |
| `numbers.tex` | Every number stated in the paper, defined once |
| `preamble.tex` | Kit preamble + `algorithm`, `algpseudocode`, `placeins`, and `\storedref` with `\mainref`/`\maineqref` (supplement → paper) and `\suppsec` (paper → supplement) |
| `sec/teaser.tex` | Title + full-width Fig. 1 (calls `\maketitle`) |
| `sec/0_abstract.tex` … `sec/8_llm_statement.tex` | Paper sections |
| `sec/X_suppl.tex` | Supplementary material, appended after the references as in the kit (`\maketitlesupplementary`, pages restart at 1, sections A–F) |
| `main.bib` | Bibliography |

Build: `latexmk -pdf main.tex`, or `./scripts/make_all.sh` to also regenerate figures.
With `\input{sec/X_suppl}` active: pages 1–8 content, 9–10 LLM statement and references, 11–18 supplement. It is currently commented out (Overleaf edit, 2026-11-16), so `main.tex` builds the 10-page paper alone.
**Submission (two PDFs):**
- paper: `main.tex` with `%\input{sec/X_suppl}` commented out (10 pages);
- supplementary material: `supplement.tex` (8 pages). In Overleaf, set Menu → Main document to `supplement.tex`, recompile and download, then set it back to `main.tex`.

Cross-references between the two parts store their value, so neither PDF shows "??":
- the supplement refers to the main paper (Eqs. 1–4, Sec. 4.2) with `\mainref{label}{number}` / `\maineqref{label}{number}`;
- the main paper points to supplement sections with `\suppsec{label}{letter}`, printed as "Supp. Sec. D" (ten places in Secs. 4–5 and the Tab. 1 caption).

In the combined build these are live links; in a separate build the stored value is printed. If numbering or section order changes, the combined build warns: `Package storedref Warning: Stored value … is out of date`. Then update the stored value where it is used.

Camera-ready: switch to `\usepackage{cvpr}` in `main.tex`, fill in `\author{...}`, and add acknowledgements.
The old extended working draft is kept, uncompiled, in `archive/extended-draft/`.
