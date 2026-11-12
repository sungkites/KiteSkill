# Figure protocol / 科研图片协议

## Choose by evidence question

| Question | Candidate display | Essential check |
|---|---|---|
| How does one method differ on the same units? | Paired points, effects with intervals | Preserve pairing; define uncertainty |
| How does behavior change with a parameter? | Curves with raw points/bands | Plot sampled support; don't invent interpolation certainty |
| What is the outcome distribution? | Points, ECDF, box/violin with n | Show meaningful tails; disclose density assumptions |
| Which mechanism explains a change? | Intervention/ablation plus matched control | Isolate capacity, data and compute confounds |
| What is the quality–cost trade-off? | Scatter/Pareto display | Same task/settings; define measured/estimated cost |
| How do method parts interact? | Editable flow/system diagram | Correct inputs, outputs, arrows and equations |

## Multi-panel evidence architecture

Give each panel a question and evidence role. Share meaningful axes and visual
encodings. Order panels so a reader can follow the scientific reasoning. Allocate
space by information density; do not force identical sizes where readability suffers.

## Honest export

Use PDF/SVG for quantitative vector content, high-resolution PNG/TIFF when required,
and dimensions/fonts set for the venue's actual print size. Do not claim universal
Nature compliance from a theme. A diagram's editable source does not guarantee that
embedded photographs or raster subplots are individually editable.

Inspect the final PDF/SVG rendering, not only a Python canvas. Check glyphs, math,
overlap, clipped legends, panel labels, image resolution and caption/data agreement.
Record any unperformed render or metadata checks. Include sample size and interval
definition in the caption only after verifying their source.
