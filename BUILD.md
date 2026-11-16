# Build

This project follows the official **CVPR 2027 author kit** (`author-kit-CVPR2027-v1-latex`):
`cvpr.sty` and `ieeenat_fullname.bst` are the unmodified kit files, `main.tex` is the kit's
skeleton, and `preamble.tex` is the kit's preamble with this paper's extra packages appended.

| File | Role |
|---|---|
| `main.tex` | Main paper and supplement in one PDF (review mode). Overleaf "Main document". |
| `preamble.tex` | Kit preamble + `algorithm`, `algpseudocode`, `placeins`, `tables/values.tex` macros |
| `sec/teaser.tex` | Title + full-width Fig. 1 (calls `\maketitle`) |
| `sec/0_abstract.tex` … `sec/8_llm_statement.tex` | Paper sections |
| `sec/X_suppl.tex` | Supplementary material, appended after the references as in the kit (`\maketitlesupplementary`, pages restart at 1, sections A–F) |
| `main.bib` | Bibliography |

Build: `latexmk -pdf main.tex`, or `./scripts/make_all.sh` to also regenerate figures.
One PDF: pages 1–8 content, 9–10 LLM statement and references, 11–18 supplement.
**Submission:** as the kit warns, split the PDF before uploading: the paper is pages 1–10 and the supplementary file is pages 11–18. Alternatively, comment out `\input{sec/X_suppl}` for the paper-only build.

Camera-ready: switch to `\usepackage{cvpr}` in `main.tex`, fill in `\author{...}`, and add acknowledgements.
The old extended working draft is kept, uncompiled, in `archive/extended-draft/`.
