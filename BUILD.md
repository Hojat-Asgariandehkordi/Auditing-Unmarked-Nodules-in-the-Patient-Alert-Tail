# CVPR 2027 review package

Build both PDFs with

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex supplement.tex
```

The archive includes the official review template, figure assets, and generated tables. Submit `main.pdf` as the manuscript and `supplement.pdf` as supplementary material. The main manuscript fits within the eight-page content limit.

The longer working draft uses the same title, abstract, and figures. To build it, run `latexmk -pdf -interaction=nonstopmode -halt-on-error extended.tex`.
