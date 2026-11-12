# KiteSkill

**A personal SCI research skill suite connecting questions, evidence, experiments and manuscripts.**

[中文](README.md) · [English usage guide](docs/USAGE.en.md) ·
[Chinese usage guide](docs/USAGE.zh-CN.md) · [Sources and optional tools](THIRD_PARTY.md)

Seven independently installable Agent Skills, designed primarily for Codex and
portable as complete `SKILL.md` folders to other compatible hosts. KiteSkill
reorganizes research work into original `kite-*` modules; it does not require
installing a large upstream research framework.

## Modules

| Invocation | Responsibility | Example task |
|---|---|---|
| [`$kite-research`](skills/kite-research/SKILL.md) | Route and coordinate the current research task | Continue the next consequential step without restarting completed work |
| [`$kite-ideation`](skills/kite-ideation/SKILL.md) | Mechanisms, questions, novelty boundaries and testable hypotheses | Compare closest primary studies and propose a discriminating pilot |
| [`$kite-literature`](skills/kite-literature/SKILL.md) | Discovery, close reading, evidence mapping and reference checks | Find real support and identify exact source passages |
| [`$kite-experiments`](skills/kite-experiments/SKILL.md) | Baselines, ablations, statistics, robustness, costs and bounded pilots | Design decisive comparisons around a concrete claim |
| [`$kite-writing`](skills/kite-writing/SKILL.md) | Drafting, restructuring, translation and polishing | Revise a manuscript while preserving meaning, numbers and citation scope |
| [`$kite-figures`](skills/kite-figures/SKILL.md) | Python plots, multi-panel evidence and method diagrams | Produce inspected PDF/SVG/PNG figures from real data |
| [`$kite-review`](skills/kite-review/SKILL.md) | Pre-submission review, targeted audits and reviewer responses | Align concerns, actual changes, evidence and manuscript locations |

## Research preferences

- Seek specific scientific or mechanistic contributions. Recombination, renamed
  metrics, more compute or better presentation alone do not establish novelty.
- Use credible matched comparisons and focused experiments that answer a claim.
- Use authentic, relevant citations. A full original manuscript may plan for
  30–50 verified references, subject to discipline, argument and venue; never pad.
- Discuss research naturally in Chinese when appropriate and adapt English prose
  to the target venue. Keep execution logs separate from the paper.
- Default quantitative plotting to Python; honor an explicit backend choice.
  Inspect exported figures rather than relying only on a successful script run.
- Use A100/Orin resources for specific questions, check current device/storage
  conditions, and distinguish runtime checks from research evidence.
- Load only the required module. Respect existing authorization and user scope.

## Install

Requires Python 3.10+ and Git. The installer uses only the standard library and
does not install models, GPU runtimes or paid services.

```bash
git clone https://github.com/sungkites/KiteSkill.git
cd KiteSkill
python scripts/install.py
python scripts/install.py --check
```

Default destination: `$CODEX_HOME/skills`, or `~/.codex/skills` when unset.
Use the skills on your next turn; reopen the session or restart the client if its
skill list does not refresh.

Install a subset:

```bash
python scripts/install.py --skills kite-writing kite-figures
```

For another compatible host, use its skill directory, for example
`python scripts/install.py --dest ~/.claude/skills`.
Actual tool access, permissions and skill discovery depend on the host.

## Update and protect local edits

```bash
git pull --ff-only
python scripts/install.py --update
python scripts/install.py --check
```

Different unmanaged folders are never overwritten. Updates stop when a managed
skill has local modifications. Existing managed versions are backed up under
`kite-skill-backups/` beside the destination skill directory before replacement.
A failed batch attempts to restore moved versions. Identical reinstalls do not
rewrite skill files. Maintain custom changes in the repository and then reinstall.

A host's GitHub skill installer can also install complete `skills/kite-*` folders.
Do not copy just `SKILL.md`: references, scripts and UI metadata belong with it.

## Invoke

```text
Use $kite-research to continue the current paper from its next missing dependency.

Use $kite-ideation to identify a mechanism-grounded question and the smallest useful pilot.

Use $kite-writing to translate this paragraph into scholarly English without changing its claims.

Use $kite-figures to inspect results.csv, define the conclusion and create checked exports.
```

You can also ask to use “my KiteSkill” and let the router choose a module.
Each specialist remains useful when the other modules are not installed.

## Bundled helpers and optional dependencies

| Capability | Helper / dependency | Scope |
|---|---|---|
| Install, update, compare content | `scripts/install.py`; standard library | Does not alter unrelated skills or client settings |
| DOI metadata checks | `skills/kite-literature/scripts/verify_doi.py`; standard library and Crossref access | DOI, title, year and first-author family name only; not claim support, full author order or validity |
| Basic CSV plots | `skills/kite-figures/scripts/plot_csv.py`; matplotlib | No automatic aggregation, interval estimation or significance testing |
| Package validation and tests | `requirements-dev.txt` | Packaging/helper checks do not validate scientific judgment |

For plotting: `python -m pip install "matplotlib>=3.8,<4"`.
Search, rendering and model access use capabilities already available in the host.
Zotero MCP, PaperQA, SciencePlots and AutoIllustrate are optional extensions listed
in [THIRD_PARTY.md](THIRD_PARTY.md), not automatically installed dependencies.

## Development and validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

GitHub Actions is configured to run these checks on Windows and Linux; consult
Actions for actual results. [Acceptance scenarios](docs/ACCEPTANCE.md) are reusable
manual tasks, not claims that agent-level evaluations have passed.

## Sources and license

Original code and instructions are MIT-licensed. The modules are independently
written workflows informed by the research needs and projects documented in
[THIRD_PARTY.md](THIRD_PARTY.md), not renamed copies of upstream bundles.
External projects retain their own licenses.

The suite assists research; it does not guarantee novelty, journal quartile or
acceptance. Authors remain responsible for data, references and scientific claims.
