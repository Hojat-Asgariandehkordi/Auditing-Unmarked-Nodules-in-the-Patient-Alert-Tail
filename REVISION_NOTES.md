# Revision notes: paper 3, "Auditing Unmarked Nodules in the Patient Alert Tail"

Baseline: the source as received (first commit). No supervisor comments were provided, so the group's standing checklist was applied.

## Build
- `main.tex` builds one PDF in the kit's layout: 8 pages of content, LLM statement and references on pages 9–10, then the supplement (`sec/X_suppl.tex`, 8 pages, page numbers restart at 1): `latexmk -pdf main.tex`.
- To rebuild everything (figures + PDFs), run `./scripts/make_all.sh`.
- `extended.tex` (the longer working draft) still compiles but was **not** updated. Its cross-references to the new sections are undefined.

## Checklist → what changed
| Item | Change |
|---|---|
| Abstract with no undefined terms | Rewritten in plain language. It poses two questions and gives about 6 numbers. It now **states that the primary endpoint failed** (3.2% vs 7.1% omission recall, margin missed); before, this appeared only in Sec. 4.3. |
| Schematic Fig. 1 | New full-width teaser on page 1 (`teaser.pdf`). (a) applies the paper's actual allocation rules (Eqs. 1–3 and the mark-stratified rule) to a toy roster: at the same budget, the chance an omission is audited is 0.35/0.02 under mark stratification vs 0.95/0.95 under paired tail, and mark stratification spends 5.0 of its audits per scan on the unremarkable tail. (b) shows the real calibration maxima of the selected detector, both cutoffs, and two real CT crops. |
| Step-by-step math + algorithm box | Method rewritten as Sec. 3.1–3.5: setting and notation → where to audit (Steps 1–3, reach) → training → cutoff → replay → protocol. Every symbol is defined at first use, and every constant in Eqs. 1–3 is explained (e.g. the rank term halves every ~4 ranks). Worked examples: h_i = 0.61 for rank 4 at one logit below t₀; k = ⌈61.2⌉ = 62 → 6th-largest maximum, 6/68 = 8.8%; k = ⌈48.6⌉ = 49. New **Algorithm 1** covers the audit and the score-fixed replay. |
| Small tables → text; wide → one column | Both main tables were already one column and are kept. The 18-row contrast table stays in the supplement; its key rows are now a forest plot (Fig. 3b–d). |
| Clear error bars, consistent colours | Every figure was redrawn in Times with capped 95% intervals. Colours are fixed: paired tail blue, image tail teal, mark-based orange, uniform grey, first read navy, **official-consensus patients purple** (before, this used the same orange as mark IPW). |
| Related work + conclusion | New first paragraph, "Reference standards in lung nodule detection" (Armato 2007, 2009; Jacobs 2016). Label-noise survey, Horvitz–Thompson and test-label-error references were added. Discussion now has "Reach is not detection", "Reference membership is part of the operating point" and **Limitations**, followed by a separate **Conclusion**. |
| Fill the 8 pages | Content now ends on page 8 (it ended on page 7 before). |
| More results from the supplement in the main paper | New **Fig. 3**: alert curve plus paired effects under both references (previously supplement Tab. S-reference_effects and Fig. S-locked). The CT examples became a one-column 2×2 figure. |
| Review-history wording | Removed "revision scoring", "earlier work inspected", "initial anchor check", "sibling ... review" and "historical". The text now states plainly that the reference replay was specified after the locked comparison. |

## Style pass (2026-11-12, second round)
Goal: every section should read as a CVPR paper, not as a generated report or an implementation log.
- **Main paper.** Abstract, introduction, related work, discussion and conclusion rewritten as connected prose, with no verdict-style bold sentences. Method headings are now *Alert leverage / Reader disagreement / Allocation / Budget-matched controls / Reach* (no "Step 1/2/3"). Data, baselines, protocol and the "anchor draw" definition moved into a new **Sec. 4.1 Experimental setup**. Sections were renamed to standard CVPR headings: 4 Experiments (setup, audit reach, effect of the representation, main results, analysis of missed omissions) and 5 Effect of the Calibration Reference (threshold displacement, robustness, effect on the method comparison, qualitative examples).
- **Figure placement.** Full-width figures are now defined earlier, so Figs. 3–5 appear before the Discussion. Content still ends on page 8.
- **Supplement.** Rewritten with lettered sections (A Dataset and Reference Construction, B Representations and Optimization, C Audit Design and Estimation, D Evaluation Protocol and Additional Results, E Calibration Reference Analysis, F Simulation Study). Imperative step sequences ("Use…", "Repeat…", "Reparse…", "Sum over…") became descriptive prose. Internal pipeline terms were replaced: *ledger, arm, route, gate, bounded repair, historical, sibling*. All table captions now define their columns.
- **Removed from the paper:** the "Figure data provenance" section and the "values recovered from the original figure" caption notes. This is workflow information, so it stays here in the notes (see *Recovered values* above).
- The Figure 1 footnote now reads "Synthetic roster; probabilities from Eqs. (1)–(3)".

## CVPR 2027 author kit (2026-11-12, third round)
- Checked against the official kit `author-kit-CVPR2027-v1-latex`. `cvpr.sty` and `ieeenat_fullname.bst` are byte-identical to the kit's.
- The project now follows the kit's layout:
  - `main.tex` is the kit's skeleton (`\input{preamble}` before hyperref, review mode, `\confName`/`\confYear`, no Paper ID, as the 2027 kit specifies).
  - `preamble.tex` is the kit's preamble plus `algorithm`/`algpseudocode`/`placeins`.
  - Sections live in `sec/`, and the bibliography is now `main.bib`.
- The supplement lives in `sec/X_suppl.tex` and uses the kit's `\maketitlesupplementary`. It builds standalone through `supplement.tex`, or appended to `main.tex` as in the kit (verified: 17 pages, no undefined references).
- Text uses the kit macros `\vs`, `\eg`, `\etal`.
- Page limit (kit: 8 pages excluding references) is still met: the Conclusion ends on page 8.
- The extended working draft moved to `archive/extended-draft/` (not compiled); `extended.pdf` was removed.
- **Overleaf:** after pulling these GitHub changes, check that Menu → Main document is still `main.tex`.

## Overview figure moved to page 2 (2026-11-14)
- Fig. 1 is now a normal full-width float (`figure*`), defined right after `\maketitle` in `sec/teaser.tex`, so LaTeX places it at the top of page 2. Page 1 holds the title, abstract and the start of the introduction.
- This also removed the two `\vspace` adjustments the old title-block placement needed. The figure, caption, numbering and text are unchanged.
- The page limit still holds: the conclusion and LLM statement end on page 8.

## Abstract numbers, bold and white space (2026-11-14)
- **Abstract:** reduced to headline numbers (79 of 92 omissions; more than 3× the mark-based yield; 14 patients; 280 of 283 detectors). The detailed values (3.2% vs 7.1%, +3 points, 202, 11 of 42, −4.0 → +3.6) remain in the Introduction, Secs. 4.4 and 5 and the Conclusion; a script confirmed that no number was lost.
- **Bold removed:**
  - the contribution labels became "First, … Second, … Third, …";
  - no figure or table caption, in the main paper or the supplement, opens in bold any more;
  - the one-paragraph "Qualitative examples" run-in heading was folded into Sec. 5.3.
  - Still bold: section and paragraph headings, algorithm keywords, and the selected method's row in Tab. 1, which its caption explains.
- **White space:**
  - the CT figure (Fig. 6) is now one row at column width instead of a tall 2×2 block;
  - Figs. 3 and 4 are slightly shorter, so Section 5 starts on page 6 and the stretched gaps on pages 6–8 are gone.
  - References now begin on page 8.

## Fig. 1 rebuilt with BioRender (2026-11-14)
- **Layout:**
  - (a) is a BioRender method overview: Training → Calibration → Test, with frozen and trained parts marked;
  - (b) is the toy-roster audit probabilities;
  - (c) is the real thresholds of the selected detector.
- **Interactive rounds (previews are in `figures/biorender/`):**
  - round 1: strip vs. pictorial cards;
  - round 2: two hybrids, with H1 chosen (BioRender figure `5186a2a8dbee86b88aec68cb`);
  - round 3: BioRender refinements were too imprecise, so the corrections are made in code.
- **`scripts/fig_overview_br.py`** cleans and corrects the art from one LAYOUT table:
  - every BioRender label is erased and retypeset in Times;
  - the 7th candidate circle is removed (the CT slice shows 6);
  - the pale score segment above the grey test threshold is removed;
  - the third excluded patient icon is faded;
  - the threshold lines are redrawn exactly at the 2nd-tallest bar (top row, y=175) and the 2nd-tallest remaining navy bar (bottom row, y=360), confirmed by measuring the bar tops;
  - the corrected-label arrow is added.
- The caption says "Schematic created in BioRender, labels added", and the LLM/tool statement now mentions BioRender. Add BioRender's named citation at camera-ready (TODO in `sec/teaser.tex`).
- **Still to do:** the art currently uses the 1024-px BioRender preview (`overview_H1_preview.jpg`). Import the full-resolution export as `figures/biorender/overview_H1.png` (via Overleaf "From external URL"); the script picks it up automatically.

## Figures (`figures/`, regenerated by `scripts/`)
| File | Figure | Script |
|---|---|---|
| `teaser.pdf` | Fig. 1 | `fig_overview.py` |
| `acquisition.pdf` | Fig. 2 (now one column) | `fig_results.py` |
| `effects.pdf` | Fig. 3 (new) | `fig_results.py` |
| `reference_tail.pdf` | Fig. 4 (adds the random-removal band) | `fig_results.py` |
| `robustness.pdf` | Fig. 5 | `fig_results.py` |
| `ct_evidence.pdf` | Fig. 6 (2×2) | `fig_results.py` |
| `locked_performance.pdf`, `variability.pdf` | supplement | `fig_supplement.py` |

- **Fonts:** TeX Gyre Termes is converted to TrueType at runtime (`scripts/fonts/`, git-ignored). Math uses STIX. `pdffonts` shows only Times/STIX in every figure. `study_map.pdf` (DejaVu) is used only by the extended draft.
- **Data:** every plotted number is in `scripts/data.py`, which names its source.
- **Recovered values (please confirm):** the package had no analysis ledger. Values plotted but never printed were read back from the vector geometry of the original figures (kept in `figures/orig/`) by `scripts/recover_vector.py` → `scripts/recovered.json`. These are the per-draw reach, the 15 calibration maxima, the random-removal ranges, the reader-pair cells, the alert curves and the variability decomposition. Every recovered set reproduces the numbers in the text: draw means 79.2/65.5/24.2, deletion upper end 4, cutoff logits 1.52/0.63, and nominal points equal to Tab. 1 to 0.1. Replace them with the ledger output when available.
- **CT crops** in `figures/ct/` are the four 521-px rasters from the original figure (public, de-identified LUNA16). No volumes or `.npz` files are in the repo.

## Open items for the group
1. **Primary endpoint framing.** The abstract and intro now lead with the failed non-inferiority result and the reference effect that explains its fragility. Agree as a group that this is the framing you want.
2. **Confirm the recovered values** listed above against the analysis output.
3. **Verify the 6 new references** at the end of `references.bib`.
4. **LLM statement.** Replaced on 2026-11-15/16 with the authors' wording, naming Codex (ChatGPT) (copy-editing, readability, visualization boilerplate code, preliminary literature discovery). Earlier versions also credited Codex with experimental design, analysis code and drafting, and Claude with figure redrawing. Confirm the new wording covers all actual use under the CVPR 2027 policy.
5. **Anonymity.** This GitHub repo is public under a named account and has the paper's exact title. Consider making it private during review.
6. **Extended draft:** moved to `archive/extended-draft/`. Delete it if no longer needed.
7. **Optional experiments:**
   - an end-to-end or non-linear head trained on the paired-tail labels, to test whether more reach turns into more detection;
   - independent adjudication of the 14 excluded calibration patients' maxima;
   - the same replay on a second dataset.

## Changes ported from the Blue review version (2026-11-15)
Source: `BLUE_REVIEW_33410___marked_revisions___2026_11_15.pdf`. The current text, abstract style and figures were kept; only Blue's corrections and its acquisition ablation were brought in. Full comparison: project doc `paper3-unmarked-nodules-alert-tail/blue-review-comparison.md`.

- **Claims corrected:**
  - Sec. 4.2 no longer credits the 15.2-omission contrast or the gain on unmarked omissions to the reader marks. A new paragraph, "Sources of the acquisition gain", reports Blue's ablation:
    - image uncertainty without marks reaches 76.1, marks alone 69.7, the complete policy 79.4;
    - the complete policy is +3.3 omissions or 3.6 points [1.3, 5.9];
    - on the 35 unmarked omissions, image uncertainty without marks reaches 27.8 against 27.4 for the complete policy.
  - The abstract, intro and Discussion now attribute the gain to image ranking and image-based uncertainty.
  - Sec. 4.5: "the failure occurs at the threshold rather than in the ranking" became "winning within a scan does not establish their ranking against negatives in other scans".
  - The leverage example in Eq. 1 is made precise; the alert-rate guarantee is stated as a marginal upper bound; the loss statement now applies to "any fixed head".
- **Honesty additions (numbers already in our supplement):**
  - CIs condition on the fitted models and calibration patients;
  - joint calibration resampling spans −14.3 to +7.1;
  - first-read gap after exclusion: −6.0 [−12.2, −1.6];
  - 202 detectors break down as 196/257 3D, 2/2 multi-view and 4/24 descriptor score vectors;
  - multi-view is described as a frozen 2.5D checkpoint;
  - an explicit sentence that the mark, uniform and image-tail allocations beat paired tail on test omissions;
  - "without establishing superiority"; "simulated" re-reading; "a linear head on frozen 3D features".
- **Supplement:**
  - New paragraphs "Sources of the acquisition gain" (with the full ablation table, `tables/ablation.tex`) and "Leverage terms" (factorial: 6.27 / 65.22 / 79.33 / 79.38).
  - Both are placed at the end of Sec. D so that the Sec. D floats do not cascade. The supplement is now 8 pages.
- **Other:**
  - The table caption defines "weighted".
  - Captions and some sentences were tightened with Blue's wording.
  - Fixed the hyphen-minus in the CI macros (`[-1.4, 9.5]` → `[−1.4, 9.5]`).
  - Added the ChatGPT disclosure to both LLM statements.
- **Layout:** content ends on page 8; the LLM statement starts page 9 (`\clearpage`) and references follow. This stops the stretched white gaps on page 8.
- **Not taken from Blue:**
  - its number-heavy abstract;
  - the Fig. 1b toy-roster numbers repeated in the intro;
  - the two-decimal leverage paragraph in the main text (now in the supplement);
  - the long next-steps paragraph (now one sentence).
- **Needs author confirmation:** the ablation and factorial values come from the Blue PDF only (no source table in this repo).

## Blue supplement and references (2026-11-15, evening)
Source: `BLUE_REVIEW_33410___marked_revisions___2026_11_15_1.pdf` (Blue's supplement, built on our pushed version).
- **Taken from Blue's supplement:**
  - **Acquisition controls:** full protocol. p_i is recovered by inverting Eq. 2. The policies share leverage, floor 0.0025, cap 0.95 and an expected budget of 3,950.15. The marks-only control uses u = 0.175 / 0.725 / 0.95. Reach is exact, the bootstrap details are given, and the caveats are stated.
  - **Ablation table** (`tables/ablation.tex`): now has two-decimal values plus a bottom panel of complete-minus-control differences:
    - vs image tail: 15.18 omissions, 16.50 pp [12.16, 20.65];
    - vs marks only: 9.70, 10.54 [6.91, 13.94];
    - vs image uncertainty: 3.27, 3.55 [1.32, 5.95].
  - **Leverage factorial:** fully specified (Eq. 1 terms, floors, clipping, the 378,371-candidate roster, a constant arm that is not uniform sampling). There is a new table (`tables/leverage.tex`) that includes the expected patients opened. Its contrasts are 79.5 [74.0, 84.1] vs constant, 15.4 [9.6, 21.3] vs threshold alone, and +0.047 [−0.261, 0.593] vs rank alone.
  - **Power tuning:** "power tuning leaves the omission endpoint unchanged in this setting".
  - **Supplement LLM statement:** Codex wording now matches the main paper, and the BioRender sentence was added.
- **Not taken:** the run seed, the 14-digit t0 (rounded to 1.566), three-decimal table values (shown to two decimals), and the "not prospectively preregistered" wording (it reads as review history). The text keeps "post hoc" and "specified before the contrasts were computed".
- **References:** 30 → 47, every one checked online (venue, volume, pages):
  - active learning: Settles 2009; Sener & Savarese ICLR 2018; Yoo & Kweon CVPR 2019; Yuan et al. CVPR 2021; Budd et al. MedIA 2021;
  - sparse annotation: Niitani et al. CVPR 2019;
  - multiple annotators: Dawid & Skene 1979; Raykar et al. JMLR 2010;
  - nodule detectors: Dou et al. TBME 2017; Ardila et al. Nat Med 2019; Baumgartner et al. MICCAI 2021;
  - allocation: Neyman 1934;
  - conformal: Vovk et al. 2005; Bates et al. AoS 2023;
  - evaluation fragility: Recht et al. ICML 2019; Beyer et al. 2020; Maier-Hein et al. Nat Commun 2018.
- **Related Work:** each new reference is cited inside the existing sentences. One new sentence positions active learning: it adapts the model between queries without known inclusion probabilities. "Reader sensitivity varies with the panel" was removed there because the Introduction already says it.
- Content still ends on page 8; the supplement is 8 pages.

## Main paper and supplement in one PDF (2026-11-15, night)
- Re-checked against the uploaded `author-kit-CVPR2027-v1-latex.zip`: `cvpr.sty` and `ieeenat_fullname.bst` are byte-identical to the project's copies.
- **One document, kit pattern:** `main.tex` now `\input{sec/X_suppl}` after the bibliography (the kit's own commented line, uncommented). The supplement opens with the kit's `\clearpage`, `\setcounter{page}{1}`, `\maketitlesupplementary`.
- **Removed:** `supplement.tex` and `supplement.pdf`. The supplement's LLM statement was identical to the main one, so a single statement remains, on page 9. `scripts/make_all.sh` and `BUILD.md` are updated.
- **Supplement back-references are now live:** "Eq. (1)/(2)/(4) of the main paper" and "Sec. 4.2 of the main paper" became `\eqref{eq:leverage}`, `\eqref{eq:working}`, `\eqref{eq:reach}`, `\eqref{eq:allocation}` and `\ref{sec:reach}`.
- **Hyperlinks:** supplement sections got unique link anchors (`\theHsection`), so "Sec. A" no longer jumps to main Section 1. The 8 duplicate page anchors that remain come from the kit's page reset and are harmless.
- **Result:** 18 pages (1–8 content, 9–10 LLM statement and references, 11–18 supplement). No undefined references, no "??", fonts unchanged, empty PDF metadata.
- **Before submitting:** split pages 11–18 off as the supplementary file, as the kit warns.

## LLM statement (2026-11-15, late)
- `sec/8_llm_statement.tex` now holds the authors' statement verbatim (2026-11-16 wording, naming Codex (ChatGPT)). It starts page 9 as before; layout is unchanged.
- The BioRender credit is no longer in the statement (BioRender is not an LLM). It remains in the Fig. 1 caption ("Schematic created in BioRender, labels added").
- 2026-11-16: an Overleaf edit commented out `\input{sec/X_suppl}` in `main.tex`, so the default build is now the paper alone (10 pages). Uncomment that line to append the supplement again (18 pages).

## Fig. 1 (a) redrawn as a vector layout (2026-11-16)
- **Problem (author feedback):** in the BioRender-based panel, labels did not match their shapes and space was wasted. The Calibration title was wider than its panel; "frozen 3D encoder" was squeezed into the trapezoid; "corrected labels z_i" floated beside an arrow; a faint dashed line was left under "lower threshold"; the Test panel's lower half and the Training panel's corners were empty. These came from typesetting labels over a fixed raster whose boxes could not be moved.
- **New generator `scripts/fig_overview.py`** (replaces `fig_overview_br.py`; `make_all.sh` updated):
  - Draws in vector form every panel, box, bar, threshold line, arrow, patient glyph, snowflake, tick and cross. Every label is placed inside its own shape in one inch-based coordinate system.
  - Takes only four icons from BioRender figure `5186a2a8dbee86b88aec68cb`: the scanner with the training slice (7th circle inpainted, six candidates match the six bars), the two readers (leader-line remnant removed), the magnifier, and the test slice (overlapping reader icon removed). Their pastel backgrounds are keyed to transparent.
- **Layout:**
  - **Titles:** each panel has a one-line title with its patient count and a short subtitle.
  - **Training:** the top row runs CT → readers A/B (disagree) and frozen detector → audit probabilities π_i for candidates 1–6, with the omission (purple) in row 4. The bottom row has the expert audit (sampled with prob. π_i) → corrected labels z_i → trained head g ← frozen 3D encoder ← CT.
  - **Calibration:** two rows of negative maxima. T sits at the 2nd-largest maximum. After excluding official positives (faded purple), the lower threshold sits at the 2nd-largest remaining maximum.
  - **Test:** mirrors the two rows. The same test-omission score is *missed* under T and *found* under the lower threshold; the threshold names sit at the left end of the lines.
- **Unchanged:** panels (b) and (c). Panel (a) is 2.40 in tall (was 2.56).
- **Caption:** "Schematic created in BioRender, labels added" → "Icons created in BioRender".
- The LLM statement no longer forces a page break (`\par` instead of `\clearpage`): page 8 is full, and the statement opens page 9.
- Fonts in `teaser.pdf`: TeX Gyre Termes and STIX only.

## Fig. 1 rebuilt from the authors' slide (2026-11-16)
- **Source:** the authors' four-panel slide (`figures/fig1_slide_reference.png`). It is rebuilt in matplotlib, with all text in Times (TeX Gyre Termes; STIX for math) and every element drawn in vector form.
- **Panels:**
  - **(a) The problem:** a real unmarked nodule (LUNA16 crop, Fig. 6d); a legend (reference target / weak annotation / training label); a candidate-landscape sketch.
  - **(b) Paired-tail audit allocation:** pilot detector (frozen) → patch grids (high score; uncertainty & disagreement) → audit-priority bubbles π_i → expert label → corrected target z_i (background → nodule) → frozen encoder → linear head. The patches are cut from the four real crops and are illustrative (the caption says so).
  - **(c) Score-fixed calibration replay:** the real 15 largest of the 67 C/D-negative maxima (recovered values in `scripts/data.py`), official consensus patients in purple. Before and after their exclusion, the thresholds are 1.52 → 0.63.
  - **(d) Consequence:** the real Fig. 6(c) test omission (margins −0.81 / +0.09), with no alert at 1.52 and an alert at 0.63; its score is unchanged.
- **Changed from the slide:**
  - the slide's illustrative 0.8 / 0.6 / 0.7 values were replaced by the paper's real values, so the paper never shows two different threshold sets;
  - panel letters are (a)–(d), as in the other figures;
  - colours follow the paper's palette (purple = official consensus, navy = negatives, blue = lower threshold / found).
- **Removed:** BioRender is no longer used in Fig. 1, so its caption credit was removed. The old toy roster and real-threshold dot plot were replaced by (b)–(d).
- **Caption:** rewritten for (a)–(d).
- **LLM statement:** made breakable. Page 8 is full with no stretched gaps; the statement starts at the bottom of page 8 and ends on page 9.

## Fig. 1 = the authors' slide, set in Times (2026-11-16, final)
- **Request:** "just change the font to times in this slide and use it for figure 1". `scripts/fig_overview.py` now reproduces the slide (`figures/fig1_slide_reference.png`) as given: layout, wording (including its bold words), colours, panel letters A–D, the 29 bar heights read from the slide pixels, and the illustrative scores 0.8 / 0.6 / 0.7. All text is Times (TeX Gyre Termes; STIX for math and bold).
- **Vector:** text, bars, thresholds, arrows, boxes, bubbles and the candidate landscape.
- **Raster:**
  - the axial CT slice, cut from the slide (`figures/ct/slide_axial.png`) and upscaled 4×, with its ring redrawn as a vector circle;
  - the patch thumbnails in B, cut from the real LUNA16 crops because the slide's thumbnails are about 19 px.
- **Slide glitches corrected:**
  - duplicate "Expert label"/"Corrected target" labels removed;
  - overlapping "N_reduced" label set once;
  - the purple (official-positive) bar left in the reduced pool removed;
  - the second CT in D now shows the same nodule (it had an empty ring);
  - D's dots and threshold lines are drawn at their labelled values (0.7, 0.8, 0.6).
- **Caption** describes A–D and states that the scores in C and D are illustrative, citing the measured 1.524 → 0.630 (Sec. 5).
- **Open (content, not changed):**
  - In C, the purple bars sit at 0.68 and 0.50, below the 0.8 threshold. Removing patients below an upper-tail threshold cannot lower it; in the real data the official positives are among the largest maxima (Fig. 4a).
  - Recolouring a few of the tallest bars purple would make the schematic consistent with the mechanism.
- **Sharper CT:** the CT images come from a 720-px screenshot. The slide's original images (or the .pptx) would give a sharper print.

## Page 8 filled; LLM statement on page 9 (2026-11-16)
- **Request:** "make it a bit longer to fill 8 pages and push the llm usage to the 9th page".
- **Added** (Sec. 6, end of the first paragraph, about five lines):
  > The audit remains useful in its own right: because every candidate is audited with a known probability, the same sample gives an unbiased estimate of the proportion of positives among the candidates that the first reader left unmarked, whatever detector is trained afterwards, so the completeness of the weak labels can be reported before detectors are compared.
  - Basis: the Horvitz–Thompson property stated in Sec. 3 and the estimand of the supplement's controlled simulation (Sec. F). No new numbers.
- **LLM statement:** `sec/8_llm_statement.tex` now starts with `\clearpage`, so it always begins at the top of page 9, followed by the references.
- **Layout:** page 8 ends flush in both columns with no gap; nothing else moved (Fig. 1 still on page 2; 10 pages). Nothing was removed.
- **Note:** page 8 is now exactly full. An edit that adds a line anywhere in Secs. 5–6 will push the last line of Sec. 6 onto page 9; shorten by the same amount.

## Numbers as variables (2026-11-16)
- **Request:** "replace the hard coded numbers with variables and then have one paragraph stating those numbers".
- **One block:** `numbers.tex` (repo root) defines every number stated in the main paper with `\newcommand`, each with a short comment on its meaning and units. The groups follow the paper: data and cohort; representations and protocol; audit-design constants (Eqs. 1–3); alert threshold; reach; representation; main results; missed omissions; calibration reference. `main.tex` loads it right after the preamble (`\input{numbers}`).
- **Replaced:** 94 hard-coded numbers in the abstract, introduction, method (including the constants inside Eqs. 1–3 and Algorithm 1), experiments, Sec. 5, the discussion, all figure and table captions, and the Tab. 1 cells that the text quotes (first read, mark IPW, mark/uniform/image-tail disc. omission recall, and the selected method's row). A value now changes everywhere from one line.
- **Replaced file:** `tables/values.tex`, the earlier partial list (44 macros, loaded from `preamble.tex`), was merged into `numbers.tex` and deleted. Its six unused macros were dropped: `\MoreHeads` 251, `\TopRemoved` 4, `\IwahitsP` 3, `\IwahitsU` 6, `\FirstHitsP` 4, `\FirstHitsU` 11 (recoverable from git).
- **Left as literals:**
  - mathematical structure ($Y_i=0/1$, $m_i\in\{0,1,2\}$, $r_i=1$, $n+1$, $1-\alpha$, $b=1$);
  - table spacing lengths;
  - table cells that the text does not quote (rest of Tab. 1, all of Tab. 2);
  - spelled-out counts ("six matched draws", "four readers");
  - the supplement (`sec/X_suppl.tex`), which is not in the current build.
- **Check:** the PDF text (`pdftotext`) and every page image are identical to the build before the change. With the supplement enabled, the document still builds (18 pages) without errors.

## Equations with named constants (2026-11-16)
- **Request (clarified):** the numbers inside the equations should become symbols, so the equations are easier to read, with one paragraph giving their values.
- **Eq. 1:** $h_i=\max\{e^{-(r_i-1)/\tau},\ \sigma((s_i-t_0+\delta)/\omega)\}$. The text now explains the symbols: the rank term halves every $\tau\ln 2$ ranks; the score term equals one half at $\delta$ logits below $t_0$, with width $\omega$. The worked example ($h_i=\max\{0.61,0.50\}$) keeps its numbers.
- **Eq. 2:** the three-case display became one line, $u_i=\beta_{m_i}+\gamma_{m_i}p_i$, $v_i=\max\{u_i(1-u_i),\varepsilon_v\}$, with an intercept and slope per mark count. Algorithm 1 now reads "$u_i,v_i\gets$ Eq. (2)" (one line shorter).
- **Eq. 3:** $\pi_i=\mathrm{clip}(c\bar h_i\sqrt{v_i},\ \pi_{\min}b,\ \pi_{\max})$ with $\bar h_i=\max(h_i,\varepsilon_h)$.
- **Mark stratification:** $\pi_i=\rho_{m_i}b$.
- **New paragraph "Design constants"** (end of Sec. 3.2):
  > We set τ = 6, δ = 1 and ω = 0.7 in Eq. (1); (β0, β1, β2) = (0, 0.55, 0.92), (γ0, γ1, γ2) = (0.35, 0.35, 0.06) and εv = 0.006 in Eq. (2); εh = 0.002, πmin = 0.005 and πmax = 0.95 in Eq. (3); and (ρ0, ρ1, ρ2) = (0.02, 0.35, 0.20). All are heuristic and were fixed before any reference label was revealed.
  - The values come from `numbers.tex` (new `\WpZeroBase` = 0; the comments there now name each symbol). They are identical to the previous equations.
- **Moved:** "a fixed design heuristic chosen before any reference label was revealed" moved from the Reader disagreement paragraph into the new paragraph.
- **Trimmed to keep 8 pages** (no content removed):
  - "and its floored Bernoulli variance" → "and its Bernoulli variance" (the floor is in Eq. 2);
  - "for each mark count m" → "for m marks";
  - "the floor of 0.006 keeps clear negatives from being excluded entirely" → "ε_v keeps clear negatives from being excluded";
  - Sec. 3.4: "Below, α = 0.10 throughout, and … or simply T" → "Below, α = 0.10, and … or T"; "if any candidate" → "if a candidate".
- **Supplement:** the leverage-factorial paragraph and the image-uncertainty control use the same symbols (τ, δ, ω, ε_h, ε_v).
- **Symbols checked for clashes:** τ, δ, ω, β, γ, ρ and ε were unused in the paper; a_j (reach), b (budget), c (bisection), α (alert rate), σ (logistic) and π (inclusion probability) were avoided.
- **Layout:** 10 pages. Page 8 ends flush and the LLM statement opens page 9. Pages 5–8 have the same layout as before. With the supplement enabled, the document builds (18 pages) without errors.

## "??" in the supplement when it is built separately (2026-11-16)
- **Report:** with the supplement disabled in `main.tex` to submit the paper alone, "??" appeared for references in the supplement.
- **Cause:** the main paper itself has no references into the supplement; its paper-only build (10 pages) had no undefined references. The supplement, however, refers to the main paper eight times (Eqs. 1–4 and Sec. 4.2). These were live `\eqref`/`\ref` links, and they only resolve when both parts are compiled together. Compiled on its own, the supplement printed "??".
- **Fix:**
  - `preamble.tex` defines `\mainref{label}{number}` and `\maineqref{label}{number}` (robust, with `refcount`):
    - in the combined build they are live links;
    - when the label does not exist (supplement compiled alone) they print the stored number;
    - if a stored number differs from the paper's actual number, the combined build warns ("Stored number … is out of date").
  - The eight references in `sec/X_suppl.tex` use them: Eq. (1) ×2, (2) ×2, (3), (4) ×2, Sec. 4.2.
- **New `supplement.tex`:** builds the supplementary material alone as the separate PDF for submission (8 pages, page 1 = "Supplementary Material", tables numbered from 1). `scripts/make_all.sh` builds it too; `BUILD.md` explains the two-PDF submission.
- **Checked from a clean copy:**
  - paper alone: 10 pages, 0 undefined, no "??", text identical to before;
  - paper + supplement: 18 pages, 0 undefined;
  - supplement alone: 8 pages, 0 undefined, no "??", correct numbers.
  - Updating an existing build in place (as Overleaf does) gives no errors, and the stale-number warning fires when a number is wrong.

## Main-paper pointers name the supplement section (2026-11-16)
- **Request:** the main paper's pointers to the supplement did not say which part of the supplement.
- **Change:** all ten "(supplement)" / "in the supplement" pointers now name the section, as "Supp. Sec. X":

| Main paper | Content | Supplement |
|---|---|---|
| Sec. 4.1, data | matching rules and cohort details | A (Dataset and Reference Construction) |
| Sec. 4.1, baselines | architectures and optimization | B (Representations and Optimization) |
| Tab. 1 caption | tail-weighted objective | C (Audit Design and Estimation) |
| Sec. 4.2 | acquisition-gain replay; leverage factorial | D (Evaluation Protocol and Additional Results) |
| Sec. 4.4 | joint calibration resampling; bookmark-cap setting ("Supp. Sec. D reports …") | D |
| Sec. 5.2 | frozen 2.5D multi-view checkpoint; per-family breakdown (196/257, 2/2, 4/24) | E (Calibration Reference Analysis) |
| Sec. 5.3 | first-read gap after exclusion (−6.0 [−12.2, −1.6]) | E |

- **Mechanism:** `\suppsec{label}{letter}` uses the same stored-value reference as `\mainref`. The generic command is now `\storedref`, and `\mainref`/`\maineqref`/`\suppsec` call it.
  - In the combined build the letter is a live link.
  - In the paper-only build the stored letter is printed (no "??").
  - A wrong stored letter triggers a warning in the combined build (tested).
- **Format:** section letters were used rather than supplement table numbers, because the tables are numbered 1, 2, … in the standalone supplement but continue the paper's numbering (3, 4, …) in the combined build.
- **Checks:**
  - paper alone: 10 pages, 0 undefined, no "??", every column ends at the same place as before (no line moved), and the LLM statement opens page 9;
  - combined: 18 pages, 0 undefined, no stale warnings;
  - supplement alone: 8 pages, 0 undefined.

## Supplementary material for submission (2026-11-19)
- **Context:** the main paper was submitted on 2026-11-16 (assumed to be the GitHub version `afb8898`). The supplementary deadline is Nov 23, 2026 AoE. CVPR 2027 sets no format for the supplement, but it must be anonymous and self-contained, with no external links.
- **Frozen interface with the submitted paper:**
  - section letters A–F are unchanged, because the paper cites "Supp. Sec. A–E";
  - every pointer still finds its content (A: matching and cohort; B: architectures; C: tail-weighted objective; D: acquisition replay, factorial, joint resampling, bookmark cap; E: 2.5D checkpoint, per-family breakdown, first-read gap);
  - the paper's own files are untouched, and its PDF text is identical.
- **Layout and typography:**
  - every float stays inside its own section (`\FloatBarrier` before each section and before the references); before, Tables 9–11 of Sec. E were printed after the references;
  - the supervision table is now one column, placed at the start of Sec. D;
  - true minus signs replace hyphens in `tables/contrasts.tex` and `tables/reference_effects.tex`, which are supplement-only tables;
  - numbers shared with the paper now come from `numbers.tex` (cohort counts, bootstrap and random-removal counts, constants), so the two parts cannot disagree.
- **Added:**
  - **Tab. 1, Notation:** every symbol of Sec. 3 with the design constants (from `numbers.tex`).
  - **A, Data use:** a public, de-identified secondary analysis with no participant interaction and no new ethics review (from the authors' extended draft and the paper's last sentence).
  - **C, Allocation rule:** a short proof that Eq. (3) solves the box-constrained convex problem (Lagrangian per term, clip, monotone bisection). It replaces the one-sentence version in "Weak evidence".
  - **C, Unbiasedness:** adds E[z_i] = Y_i, Var(z_i), and the affine logistic loss. It defines the **tail-weighted objective** as loss weight **η_i = 1 + 9h_i**, from the authors' extended draft (`archive/extended-draft/design.tex`); please confirm. The loss weights were renamed from a_i to η_i, because a_j is the reach in the paper.
  - **D, Supervision and representation:** a short paragraph that introduces Tab. 4 and links Tab. 5 and Fig. 1.
  - **D, Confidence intervals:** "jointly resampling calibration patients and audit draws gives −14.3 to +7.1 points" (`\JointLo`/`\JointHi`; the same values are in `scripts/recovered.json`, variability, both_resampled). Correction: Sec. D already stated this range, in "Per-target changes" (the earlier search missed it because it is typeset as math). The polish pass below merges the two sentences.
  - **D, Audit workload:** 3,940 (652 positive) vs 7,933 (169 positive) audited candidates; both designs open almost all 445 patients, so the 50.3% saving is in candidate decisions, not reading time; the cost of the second read, pilot and review was not measured (Tab. costs; extended draft).
  - **E, Alert-rate bound:** an exchangeability rank proof of (n+1−k)/(n+1) ≤ α and why the bound refers to the calibration population, which links it to the replay.
  - **E, Masking disputed candidates:** at the original threshold, masking removes both negative alerts and keeps the one recovered omission; after recalibration, 12 of 42 omissions are recovered with 5 alerts among 105. From the authors' extended draft (`archive/extended-draft/experiments.tex`); please confirm.
- **Moved within sections:** "Uncertainty" in Sec. E now follows "Size-matched random removal". Nothing was removed.
- **Result:** `supplement.pdf`, 9 pages (Sec. F and the references on page 9). No undefined references, no external links, empty PDF metadata. Fonts: Times (Nimbus/TeX Gyre Termes), STIX and CM math, and the kit's Helvetica ruler.
  - Clean builds: paper alone 10 pages (text identical), combined 19 pages with no stale stored numbers, supplement alone 9 pages.
- **Open:**
  - confirm η_i = 1 + 9h_i and the masking numbers;
  - ~~confirm that the submitted paper equals GitHub `afb8898`~~ — confirmed by the authors (2026-11-19): the paper's referencing is unchanged and the paper may not be changed at all;
  - check on OpenReview whether CVPR 2027 again requires a compute reporting form with the supplement (CVPR 2026 did);
  - code upload is optional, and only experiment code would help, not the figure scripts.

## Supplement polish (2026-11-19, later)
- **Request:** "Just polish it… We are not allowed to change the main at all." No main-paper file was touched: the paper's PDF text is identical, and section letters A–F and every stored cross-reference are unchanged (no stale-number warnings in the combined build).
- **Edited files:** `sec/X_suppl.tex`, `tables/supplement_results.tex`, `tables/costs.tex` and `tables/aux.tex`, all used only by the supplement.
- **Language and terms:**
  - the joint-resampling sentence appeared twice; it is now kept once in "Confidence intervals", with the detail "six draws by 300 resamples" and "test patients held fixed" moved from "Per-target changes";
  - "arm(s)" → "variant(s)" in "Leverage terms", matching the earlier style pass;
  - "difference to" → "difference from"; "every supervision" → "every training method";
  - "in the case of LargeCAD" → "for one of the original systems (LargeCAD)"; a comma added after "For each released contour";
  - the power-tuned multipliers are now labelled "for the three folds";
  - Sec. E names the pools: "C/D pool $P$", "augmented pool $U$".
- **Removed:** "The figures show crops of the released images only." (Data use). The supplement's figures are plots, not CT crops.
- **Math:** the allocation problem and the power-tuning criterion are now displayed equations (the inline sums broke the lines). "Reach and gradient variance" refers to Eq. (4) instead of restating the product.
- **Tables:**
  - the notation table has one line per row, and the β and γ rows are split;
  - workload table headers: "Lesions" → "Targets" and "Exp. dbl. unmarked" → "Exp. unmarked", both defined in the caption;
  - the auxiliary-error caption defines the mark codes (00/01/10/11), N and Ref.; 224631 → 224,631;
  - the reference-effects caption defines "C/D" (pool P) and "+ official" (pool U).
- **Layout:** the wide figure and table of Sec. D (variability, workload) are now defined early, so they share page 6. This removed a one-third-page empty band at the bottom of page 6. All pages are full except the last; 9 pages.
- **Checks:** clean builds of the paper alone (10 pages, text identical), combined (19 pages) and supplement alone (9 pages): 0 errors, 0 undefined, 0 overfull, no "??", no external links, empty metadata.

## Supplement: strict polish of the submitted-day version (2026-11-20)
- **Rule:** the main paper stays exactly as submitted, so everything it cites in the supplement keeps its number. It cites only section letters: Supp. Sec. A, B, C, D (×4) and E (×3). The polish changes wording and presentation only. Nothing is reordered, removed or renumbered, and the two-column CVPR style is kept.
- **Restored:** `sec/X_suppl.tex`, `supplement.tex` and the supplement-only tables were restored to the submitted-day version (`afb8898`). This drops the additions of 2026-11-19: the notation table, "Data use", "Allocation rule", the extended unbiasedness paragraph with η_i, "Supervision and representation", "Audit workload", "Alert-rate bound" and "Masking disputed candidates". They remain in git history (commits `5668602`, `37f98ea`) if wanted later.
- **Wording (all edits):**
  - "in the case of LargeCAD" → "for one of the original systems (LargeCAD)";
  - a comma after "For each released contour";
  - "difference to the complete policy" → "difference from";
  - "arm"/"arms" → "variant"/"variants" (three times);
  - the power-tuning criterion is a displayed equation instead of an inline sum that broke across lines;
  - the square root in "Leverage terms" no longer widens the line spacing (`\smash[t]`).
- **Captions:**
  - Table 2 defines Marks, N and Ref.;
  - Table 6 headers: "Lesions" → "Targets" and "Exp. dbl. unmarked" → "Exp. unmarked", both defined;
  - Table 10 defines "Cal. pool" (C/D or + official).
- **Tables:** true minus signs in Tables 5 and 10 (`contrasts`, `reference_effects`); 224631 → 224,631 in Table 2.
- **Placement (numbers unchanged, verified: Tables 1–11, Figures 1–2 with the same titles):**
  - Sec. D float definitions moved to the start of Sec. D, in the same order;
  - Tables 7 and 8 are no longer fixed in-place boxes (which left half-empty columns on pages 5–6); they now sit side by side in one full-width float, one per column, top-aligned;
  - the Sec. E float definitions moved just before "Leverage terms", in the same order, so Tables 9–11 print at the top of page 7. Before, they were printed after the references on a mostly empty page 8;
  - `\vfill` before the Sec. E heading: the spare line at the end of Sec. D goes to the column bottom instead of widening a paragraph gap.
- **Result:** 8 pages, as on the submitted day; every table and figure in numeric order and before the references; no half-empty columns or stretched gaps. Remaining white space: 0.24 in at the end of Sec. D (page 5), 0.39 in under Table 11 (page 7), and the space beside the shorter Table 8 in the pair.
  - Checked with `/tmp/gaps.py`-style column scans and page renders.
  - Source check: the prose is identical to the submitted day except the edits listed above.
- **Checks:** paper alone 10 pages, text identical to the submitted version, main-paper sources unchanged since `afb8898`; combined build 18 pages; supplement alone 8 pages. 0 errors, 0 undefined, 0 overfull, no "??", no external links, empty metadata.
