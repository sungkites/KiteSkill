---
name: kite-figures
description: "Plan, generate and audit SCI data plots and method diagrams with explicit evidence logic, Python plotting and inspected exports. Use for 科研绘图、多面板图、框架图、图注 and publication figures; distinguish data figures from generated illustrations."
license: MIT
---

# Kite Figures / 科研绘图与示意图

Read [the figure protocol](references/figures.md) for multi-panel layouts, statistical
figures, architecture diagrams or submission export. Default quantitative plotting
to Python for this suite; honor an explicit user/backend choice without asking again.

## Decide before drawing

State the figure's scientific conclusion, source data, comparison and uncertainty.
Select panels that establish that conclusion, not a decorative chart collection.
Inspect data and units. Distinguish missing, excluded and zero values. Do not
infer a population effect from illustrative or synthetic values.

## Data figures

Use Python/matplotlib (optional seaborn/SciencePlots). Keep the generation script,
source-data mapping and editable vector export. Show uncertainty at the correct
experimental unit, define error bars, avoid hidden baseline/axis choices and use
accessible color plus shapes/line styles where needed. Keep the figure faithful to its data.

A bundled helper makes basic plots from existing CSV values without aggregation:

```bash
python scripts/plot_csv.py results.csv --kind line --x budget --y score \
  --series method --xlabel "Budget" --ylabel "Score" --output figures/result
```

Run from this skill's directory, or use its absolute script path. It writes
PDF/SVG/PNG and a provenance JSON. An optional `--yerr` column requires
`--error-label` describing SD, SE or the supplied symmetric interval half-width.
The helper does not calculate means, intervals, significance or independent sample
counts. Use a project-specific script for asymmetric intervals, paired effects,
complex designs or multi-panel figures.

## Method and mechanism diagrams

Prefer editable SVG, draw.io, Mermaid or code-native diagrams for labels, equations,
modules and arrows. AutoIllustrate is an optional backend; PlotNeuralNet is useful
for selected neural architectures. Image-generation tools/PaperVizAgent/PaperBanana
can draft conceptual illustrations when available. Keep generated illustrations
separate from measured evidence; inspect every scientific label, arrow and formula.
Do not auto-install a model backend or send unpublished material externally without
the user's scope/authorization covering it.

## Inspect and deliver

Render and view the exported figure at intended print width. Check panel alignment,
label collisions, clipping, font embedding, legends, units, contrast and consistency
with data/caption. Iterate on observed problems. Report render limitations honestly.
Deliver requested formats plus source code/data provenance and a standalone caption
with experimental unit, n and uncertainty only where actually known.
