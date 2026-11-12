---
name: kite-research
description: "Coordinate Kite's SCI research workflow across ideation, literature, experiments, writing, figures and review. Use for end-to-end research or when the user explicitly asks to use KiteSkill / Kite科研. Route a clearly scoped task to its module without restarting completed work."
license: MIT
---

# Kite Research / Kite 科研总入口

Turn the user's current research material into the next useful research artifact.
Reply in the user's language; default discussion to Chinese and manuscript prose
to the requested journal language. Read [the handoff contract](references/handoff.md)
for multi-stage work or when resuming a project.

## Route from the actual state

| Need | Preferred module | Useful fallback if unavailable |
|---|---|---|
| Find a scientific question or mechanism | `kite-ideation` | Compare closest primary papers, propose falsifiable candidates and decisive tests |
| Find, read or verify papers | `kite-literature` | Search real databases, record identifiers, map claims to source passages |
| Design, run or interpret experiments | `kite-experiments` | Define claim, experimental unit, fair baselines, mechanism tests and cost |
| Draft, translate or polish text | `kite-writing` | Write from supplied evidence; keep missing results explicitly unresolved |
| Plot data or explain a method visually | `kite-figures` | Use Python for data plots; editable diagrams for methods; inspect exports |
| Assess readiness or answer reviewers | `kite-review` | Prioritize validity concerns and draft traceable point-by-point responses |

Read only the selected module when available. A list of modules is not an
instruction to load all of them. For a narrow task, perform that task directly.
For a full project, identify what already exists and progress from the first
unresolved dependency; ask only for missing information that materially blocks it.

## Research decisions

- Aim for a specific scientific or methodological contribution. A stack of
  existing modules, a renamed metric, more compute or improved presentation alone
  does not establish novelty or journal readiness.
- Link each central claim to its strongest evidence and its closest competing
  explanation. Distinguish observations, interpretations and untested hypotheses.
- Prefer decisive comparisons and mechanism tests to repetitive grids. Keep
  comparisons matched and conclusions supported by the actual outputs.
- Use real, relevant references. For a full original paper, 30–50 verified items is
  a planning range, subordinate to discipline, relevance and venue requirements;
  never pad a bibliography or apply that range to a paragraph edit.
- Keep setup, environment debugging and raw execution logs outside manuscript prose.
- Use the host's available tools. If search, rendering, compute or credentials are
  unavailable, state the specific limitation; do not describe an unexecuted step as
  completed. Other installed skills and paid services are optional capabilities.

## Delivery

Produce the requested artifact, a concise evidence/limitation note, and the next
material dependency if any. For extended projects, keep a small handoff record in
the user's chosen project folder; use `research-output/` only if no convention exists.
Do not publish project artifacts, install frameworks, start standing automations,
or run costly experiments just because this router is invoked. Existing explicit
authorization remains valid; do not add a new approval checkpoint at every stage.
