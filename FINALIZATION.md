# Finalization: paper 3, "Auditing Unmarked Nodules in the Patient Alert Tail"

Scope set by the authors: figures plus minor structural and paragraph changes only. The scientific content, analyses and claims are unchanged, except where a sentence stated more than the evidence supports.

Contribution (working note): with all detector scores held fixed, which patients count as negative moves a low-alert threshold beyond random removal and shifts a method comparison. Meanwhile, a rank- and disagreement-guided audit reveals about 3× more unmarked nodules per review than mark-based review.

## Initial diagnosis (self-review)
Originality 6.5 · soundness 6.5 · evidence 6 · clarity 7 · presentation 6.5 → about 6.5 (medium confidence).

Priorities:
1. Fig. 1 does not show the pipeline.
2. Result figures have redundant titles and legends and do not state what the uncertainty covers.
3. The prose has a bulleted contribution list, headed related-work fragments, and a separate Discussion and Conclusion.

## Round 1: figures
- **Fig. 1** is now the graphical abstract plus method overview. (a) applies the allocation rules to a synthetic roster. (b) shows the real calibration maxima and both thresholds; the CT crop sits directly over its point and the recovered omission is linked to its star by a leader line. New (c) is a pipeline strip: frozen components are dashed, and the training (445), calibration (175) and test (265) patient sets are shown.
- **Figs. 3–6:**
  - "threshold" is used throughout, matching the text.
  - Panels have informative titles, and repeated x-labels became one legend.
  - Legends were moved off the data.
  - Captions now say what the intervals represent: 4,000 bootstrap resamples of 265 test patients, six matched draws.
  - Fig. 6 uses one scale-bar style.

## Round 2: structure and paragraphs
- Contributions are written as connected sentences opening "Our paper offers the following contributions.", with short bold labels.
- Related Work is two connected paragraphs; no citation was removed.
- The method's announcement of its own organization was removed.
- Discussion, limitations and conclusion are merged into one section, "Discussion and Conclusion", with no bold lead-ins.
- The page limit holds: the LLM statement is on page 8 and references start on page 9.

## Round 3: independent review and fixes
An independent reviewer read the compiled PDFs: originality 6 · soundness 6 · evidence 5 · clarity 6 · presentation 7 → **5/10 overall (moderate confidence)**. It confirmed that the headline numbers agree across the abstract, text, tables, figures and supplement.

All ten presentation-level findings were fixed:
1. "Every learned detector" now reads 280/283 and 202/283; in Sec. 5.2 it is "each of the six learned heads shown".
2. "Changes sign" became "the estimated gap moves from −4.0 to +3.6 points". The discussion notes that the shift's interval excludes zero but the new gap's does not, and the abstract says "follow-up analysis".
3. The Fig. 1b crop is now anchored to its star by a leader line.
4. Purple is used only for official-consensus patients. Fig. 3 uses open vs. filled markers, like Fig. 4.
5. Method names are unified: "Mark disc. (half)" and "Paired-tail disc. (half)" in Tab. 1, the figures and the supplement tables.
6. Three legends no longer cover data.
7. Fig. 6 scale bars use one style.
8. Notation:
   - The budget is now 𝓑, so it no longer collides with reader B.
   - Thresholds are T_α, then T_P / T_U / T.
   - The alert-rate guarantee is stated as an upper bound: "at most 6/68 = 8.8%", and "at most 5/54 = 9.3%" after exclusion.
9. The supplement column "Fits" is now "Score vectors" (283 distinct vectors from 302 fits).
10. Tab. 1 now states its alert denominator (105 C/D negatives), and the 7.5-point shift is marked "computed before rounding".

Not changed (content): "all three sampled maxima around the threshold" (Sec. 4.5) still does not say which draw or ranks. The authors should specify this.

## Remaining obstacles (require new science; out of scope)
1. The primary endpoint fails: −4.0 [−7.0, −1.4] against a −5 margin. The only learner is a linear head on a frozen embedding, so testing an end-to-end learner is the decisive next experiment.
2. The calibration effect rests on 67 negatives, 14 removed patients, one dataset and a post hoc replay. It needs an external cohort and adjudication of the disputed maxima.
3. There is no sensitivity analysis for the design constants in Eqs. 1–3.
4. The effect is shown at one operating point (α = 0.10); an α sweep would generalize it.

## Status
Checked against the official CVPR 2027 author kit in review mode: 8 content pages, then the LLM statement and references; anonymous; empty PDF metadata; no undefined references. Every page was rendered and inspected.
