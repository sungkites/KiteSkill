# Search and evidence protocol / 检索与证据协议

## Corpus record

Record source database, exact search string, date window, retrieval timestamp,
screening criteria, exclusions with reasons and deduplication key (DOI, PMID,
arXiv ID or verified title-author-year). Record accessible full text/supplements
and the local path if saved. Do not claim exhaustive recall from a single query.

For a systematic review, select discipline-appropriate reporting and bias tools,
document the actual screening process and disclose deviations. Do not infer that
a PRISMA-shaped diagram alone makes a review systematic. Registration and screening
independence are facts to document, not steps to claim retroactively.

## Claim–source matrix

| Manuscript claim | Source identifier | Exact location | Access | Relationship | Limits |
|---|---|---|---|---|---|
| Literal or narrowly paraphrased claim | DOI/PMID/arXiv | section/page/figure/table | full text / abstract | supports / partly supports / contradicts / unclear | population, setting, uncertainty |

Check that the cited paper establishes the exact mechanism or numerical statement,
not merely a neighboring topic. Use original method papers for technical claims.
Separate direct evidence from inference and unresolved hypotheses.

## Bibliography checks

1. Resolve identity via DOI/PMID/publisher or database records.
2. Compare author order, title, publication dates, venue, volume/issue and locator.
3. Check in-text citations and bibliography in both directions; identify duplicates.
4. Inspect the source passage for claim support and relevant limitations.
5. Check visible corrections/retractions when reviewing reliability; an absence of
   discovered notices is not a guarantee of validity.

`verify_doi.py` automates only a subset of steps 1–2 using Crossref. Some valid
DOIs use another registration agency; a Crossref 404 remains unverified. The script
never downloads paywalled content and does not consult retraction databases.
