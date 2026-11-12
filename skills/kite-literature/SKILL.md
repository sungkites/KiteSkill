---
name: kite-literature
description: "Search and critically read scholarly literature, map claims to sources, verify reference metadata and organize lawful full texts. Use for 查文献、综述、精读、找引用、DOI核验 and bibliography audits."
license: MIT
---

# Kite Literature / 文献与证据

Read [the search and evidence protocol](references/evidence.md) for corpus building,
reference audits or source-grounded synthesis. Use the script below for Crossref
metadata checks; it does not verify whether a paper supports a manuscript claim.

## Work from the requested unit

- **Search**: define the question, concepts/synonyms, dates and inclusion/exclusion
  criteria. Search suitable primary databases and backward/forward citations.
  Record database, exact query, retrieval date and screening decisions.
- **Read**: separate the paper's question, method, experimental unit, evidence,
  assumptions, limitations and implications for this project. Cite source passages,
  tables and figures; distinguish author claims from your interpretation.
- **Synthesize**: compare studies by mechanism, setting and evidence, not a sequence
  of abstracts. Explain conflicting evidence and coverage limitations.
- **Verify**: check identity/metadata separately from claim support and research
  validity. DOI resolution alone proves neither correctness nor relevance.

Prefer authentic, directly relevant primary work. For a full paper, use 30–50
verified references as a flexible planning range, not a quota. Confirm author order,
title, venue, year, volume, issue, pages/article ID and DOI against authoritative
records. Investigate online-first versus issue-year differences rather than silently
changing dates. Label unresolved fields and corrections/retractions when found.

Acquire OA or institutionally authorized full texts and available supplements.
Keep original PDFs, citation files and evidence notes together in the user's
project. If full text is unavailable, label abstract-only conclusions and continue
with lawful alternatives. Never imply access to a paywalled paper you did not read.

## Tools and fallbacks

Use host search and connected literature tools when available. Optional integrations:
paper-search-mcp for discovery, Zotero MCP for the user's library, PaperQA for
full-text questions. None is required or installed automatically. Without live
search, analyze supplied material and mark current coverage/verification unresolved.

For a CSV with `doi` and optional `title,year,first_author`:

```bash
python scripts/verify_doi.py references.csv --output doi-report.json
```

Run from this skill's directory, or use its absolute script path. Python standard
library only; internet access to Crossref is required. `metadata_match` refers
only to supplied fields and tolerances, not full bibliography or claim validation.
Inspect `field_checks` and provider metadata. HTTP or provider failures remain
`unverified`, not fabricated or invalid-paper verdicts.

## Delivery

Return the bibliography/evidence matrix or reading artifact requested, including
identifiers, provenance, access level, and unresolved items. Export BibTeX/RIS if
needed. Never manufacture citation keys or DOIs to complete a polished-looking list.
