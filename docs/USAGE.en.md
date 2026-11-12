# KiteSkill usage guide

[中文](USAGE.zh-CN.md) · [Home](../README.en.md)

## Select the entry point

Invoke a specialist for a clear task, or `$kite-research` for routing. Execution
instructions are in English with bilingual discovery terms; conversation and
deliverable language follow the user's request.

| Available material | Module | Expected artifact |
|---|---|---|
| Topic and a few papers | `$kite-ideation` | Closest-work comparison, mechanism question, candidate hypotheses and pilot |
| Claims or search terms | `$kite-literature` | Search log, authentic sources and claim–passage mapping |
| Method and research question | `$kite-experiments` | Fair controls, decisive ablations, statistical units and budget |
| Results, figures or draft | `$kite-writing` | Evidence-grounded manuscript prose or precise revisions |
| CSV or method description | `$kite-figures` | Figure argument, code, inspected exports and caption |
| Manuscript or reviewer comments | `$kite-review` | Prioritized concerns or traceable responses and revisions |

## Example requests

```text
Use $kite-ideation to compare the closest primary studies, identify a specific
mechanistic question, and propose a small authentic-data experiment that changes
the decision to continue.
```

```text
Use $kite-literature to find support for these introduction claims. Record DOI,
title, year, exact source location, support boundaries and full-text access.
```

```text
Use $kite-writing to draft Results and Discussion from these artifacts. Keep
environment setup and execution logs in reproduction material, and match the venue.
```

```text
Use $kite-review to answer this decision letter. Separate completed changes from
proposed work, map each response to real evidence and locations, and implement
the revisions already authorized.
```

## DOI checks

Input CSV requires `doi`, with optional `title,year,first_author`. Use a family
name or collective author's full name for `first_author`. Column names are lowercase.
Only supplied fields are compared.

```bash
python skills/kite-literature/scripts/verify_doi.py references.csv --output research-output/doi-report.json
```

Statuses: `resolved_only` means a record was found; `metadata_match` means supplied
fields match; `needs_review` means a field differs; `unverified` means format,
network or provider lookup remains unresolved. A Crossref miss does not prove
nonexistence. The year check accepts recorded print/online years; venue-specific
year choice still requires inspection. Titles differing after normalization are
flagged. Every row includes `claim_support: not_checked`; inspect the paper itself.

## CSV plotting

```bash
python -m pip install "matplotlib>=3.8,<4"
python skills/kite-figures/scripts/plot_csv.py results.csv --kind line --x budget --y score --series method --xlabel "Budget" --ylabel "Score" --output research-output/figures/result
```

Kinds: `line/scatter/bar`. Bar x values can be categories; other plots use numeric
x. For supplied error half-widths add `--yerr sd --error-label "supplied SD"`.
No means or intervals are estimated. Duplicate x values within line/bar series
require explicit aggregation first; scatter allows repeated points. Missing and
nonfinite values are rejected rather than silently removed. Outputs are PDF, SVG,
PNG and provenance JSON. Existing outputs require explicit `--overwrite`.

`examples/demo.csv` contains synthetic values for software demonstration only.
Replace `results.csv` with that path to try the command; these values are not
research evidence.

## Capabilities and project state

Installing KiteSkill does not install database connectors, download backends or
image models. If search, rendering or GPU access is unavailable, the module names
the missing capability and continues independent work. Optional frameworks are
enabled only when needed; weights are not downloaded and manuscripts are not
uploaded automatically.

Store research notes/results in the user's project, never in the installed skills
or the public KiteSkill repository. A sentence edit does not require the complete
literature–experiment workflow; sustained work may benefit from a handoff record.
