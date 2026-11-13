# Build

This project follows the official **CVPR 2027 author kit** (`author-kit-CVPR2027-v1-latex`):
`cvpr.sty` and `ieeenat_fullname.bst` are the unmodified kit files, `main.tex` is the kit's
skeleton, and `preamble.tex` is the kit's preamble with this paper's extra packages appended.

| File | Role |
|---|---|
| `main.tex` | Main paper (review mode). Overleaf "Main document". |
| `preamble.tex` | Kit preamble + `algorithm`, `algpseudocode`, `placeins`, `tables/values.tex` macros |
| `sec/teaser.tex` | Title + full-width Fig. 1 (calls `\maketitle`) |
| `sec/0_abstract.tex` … `sec/8_llm_statement.tex` | Paper sections |
| `sec/X_suppl.tex` | Supplementary material (uses the kit's `\maketitlesupplementary`) |
| `supplement.tex` | Standalone build of `sec/X_suppl.tex` |
| `main.bib` | Bibliography |

Build: `latexmk -pdf main.tex supplement.tex`, or `./scripts/make_all.sh` to also regenerate figures.
To produce one PDF with the supplement appended (kit style), uncomment `\input{sec/X_suppl}` at the end of `main.tex`.

Camera-ready: switch to `\usepackage{cvpr}` in `main.tex`, fill in `\author{...}`, and add acknowledgements.
The old extended working draft is kept, uncompiled, in `archive/extended-draft/`.
