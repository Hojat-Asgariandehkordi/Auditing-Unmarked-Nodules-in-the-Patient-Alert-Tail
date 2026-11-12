# Revision notes: paper 3, "Auditing Unmarked Nodules in the Patient Alert Tail"

Baseline: the source as received (first commit). No supervisor comments were provided, so the group's standing checklist was applied.

## Build
- `main.tex` (8 pages of content + LLM statement and references = 9 pages) and `supplement.tex` (7 pages) each compile on their own: `latexmk -pdf main.tex supplement.tex`.
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

## Figures (`figures/`, regenerated by `scripts/`)
| File | Figure | Script |
|---|---|---|
| `teaser.pdf` | Fig. 1 | `fig_teaser.py` |
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
4. **LLM statement.** Codex is credited with "experimental design", and a sentence about Claude was added. Check both against the CVPR 2027 policy.
5. **Anonymity.** This GitHub repo is public under a named account and has the paper's exact title. Consider making it private during review.
6. **Extended draft.** `extended.tex` was not updated. Delete it, or bring it in line with the new text.
7. **Optional experiments:**
   - an end-to-end or non-linear head trained on the paired-tail labels, to test whether more reach turns into more detection;
   - independent adjudication of the 14 excluded calibration patients' maxima;
   - the same replay on a second dataset.
