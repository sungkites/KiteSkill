---
name: kite-experiments
description: "Design and assess claim-driven experiments, credible baselines, mechanism ablations, robustness and resource costs; execute bounded research pilots when authorized. Use for 实验设计、消融、统计 and A100/Orin实验."
license: MIT
---

# Kite Experiments / 实验与统计

Read [the evidence design guide](references/design.md) when planning comparisons,
statistical analysis, device validation or compute runs.

## Start with the claim

Define the scientific claim and which result would falsify it. Identify the unit
of replication (person, site, run, dataset, model or device), target population,
primary outcome and uncertainty measure before choosing tests. Repeated samples
from one run are not independent experiments. Estimate power or precision when
the design and available information permit it; otherwise disclose that limitation.

Build a compact claim-to-experiment table: main matched comparison, essential
mechanism ablation/intervention, bounded robustness, and parameter/efficiency/cost
analysis only where they answer a real question. Do not multiply seeds, datasets
and knobs into a defensive grid without an evidence purpose.

## Fair evidence

- Choose credible and close baselines, public benchmarks when suitable, identical
  splits/preprocessing and comparable tuning/information/resource access. Report
  important mismatches; unmatched published numbers are contextual comparisons.
- Keep train/dev/test responsibilities separate. Freeze the final evaluation
  before interpreting it; distinguish exploratory findings from confirmatory tests.
- Report effect sizes and intervals with the correct unit and pairing; specify
  SD, SE, CI or quantiles. Account for dependence, multiplicity and missingness when
  they materially affect inference. Do not equate nonsignificance with equivalence.
- Ground reported findings in real measurements and describe relevant exclusions. Mock data,
  truncated attack outputs and successful environment checks do not establish
  performance. Paired bootstrap is an uncertainty tool, not scientific novelty.

## Execute only the useful bounded run

Use existing user authorization. Check actual resource availability and preserve
healthy unrelated jobs. Prefer a small real-model/data pilot with a stopping rule
before a costly sweep. For an external-disk device profile, verify its mount, free
space and a small write/readback before downloads; put models, caches, datasets
and outputs there. Do not assume an old host or disk snapshot is current.

A100 may support training/comparison, and Orin may support deployment/cost checks
when relevant. An Orin-only run is not independent replication of an A100 result;
report what actually differs and which claim each device can test. Do not stop
unrelated workloads, install drivers or expand a compute budget implicitly.

## Delivery

Produce the design, analysis or actual result artifacts requested, with claim,
baseline fairness, data/seed/config provenance, uncertainty, costs and limitations.
Keep run instructions and debugging logs in reproduction material outside the paper.
If compute or data is unavailable, deliver the concrete executable specification
and label execution pending. Optional: `kite-figures` for results and `kite-writing`
for interpretation; perform those focused steps directly if modules are absent.
