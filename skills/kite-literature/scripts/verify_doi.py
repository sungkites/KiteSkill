#!/usr/bin/env python3
"""Compare supplied reference fields with Crossref, never infer claim support."""
import argparse
import csv
import difflib
import json
import math
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen


def normalize_doi(value):
    value = str(value or "").strip()
    if value.lower().startswith("doi:"):
        value = value[4:].strip()
    if value.lower().startswith(("https://", "http://")):
        parsed = urlsplit(value)
        if parsed.hostname not in ("doi.org", "dx.doi.org"):
            raise ValueError("Expected a DOI or doi.org URL")
        value = unquote(parsed.path.lstrip("/"))
    if not re.fullmatch(r"10\.\d{4,9}/\S+", value, re.I):
        raise ValueError("Malformed DOI; no identity verdict was made")
    return value.lower()


def normalized_text(value):
    value = unicodedata.normalize("NFKD", str(value)).casefold()
    return " ".join(re.findall(r"[^\W_]+", value, flags=re.UNICODE))


def fetch_crossref(doi, timeout=20):
    request = Request(
        "https://api.crossref.org/works/" + quote(doi, safe=""),
        headers={"User-Agent": "KiteSkill/0.1.0 (reference metadata verification)",
                 "Accept": "application/json"},
    )
    with urlopen(request, timeout=timeout) as response:
        return json.load(response)["message"]


def compare_reference(row, record):
    checks = {}
    title = (record.get("title") or [""])[0]
    dates = {}
    for key in ("published", "published-print", "published-online", "issued"):
        parts = record.get(key, {}).get("date-parts", [])
        if parts and parts[0]:
            dates[key] = parts[0][0]
    authors = record.get("author") or []
    if (row.get("title") or "").strip():
        expected, actual = normalized_text(row["title"]), normalized_text(title)
        similarity = difflib.SequenceMatcher(None, expected, actual).ratio()
        checks["title"] = {"status": "match" if expected == actual else "review",
                           "similarity": round(similarity, 4), "supplied": row["title"]}
    if (row.get("year") or "").strip():
        try:
            year = int(row["year"].strip())
        except ValueError:
            checks["year"] = {"status": "review", "reason": "Expected integer year"}
        else:
            checks["year"] = {"status": "match" if year in dates.values() else "review",
                              "supplied": year, "provider_dates": dates}
    if (row.get("first_author") or "").strip():
        # Input contract uses family name or a collective author's full name.
        first = authors[0] if authors else {}
        family = first.get("family") or first.get("name", "")
        checks["first_author"] = {
            "status": "match" if normalized_text(row["first_author"]) == normalized_text(family) else "review",
            "supplied": row["first_author"], "provider": family,
        }
    status = "resolved_only" if not checks else (
        "metadata_match" if all(c["status"] == "match" for c in checks.values()) else "needs_review")
    return {"status": status, "field_checks": checks,
            "provider_metadata": {"DOI": record.get("DOI"), "title": title,
                                  "authors": authors, "dates": dates,
                                  "venue": record.get("container-title", []),
                                  "volume": record.get("volume"), "issue": record.get("issue"),
                                  "page": record.get("page"), "article_number": record.get("article-number")}}


def verify_row(row, fetch=fetch_crossref):
    result = {"input": row, "verified_at": datetime.now(timezone.utc).isoformat(),
              "claim_support": "not_checked"}
    try:
        doi = normalize_doi(row.get("doi"))
    except ValueError as error:
        return {**result, "status": "unverified", "reason": str(error)}
    result.update(doi=doi, provider_url="https://api.crossref.org/works/" + quote(doi, safe=""))
    try:
        record = fetch(doi)
        if normalize_doi(record.get("DOI")) != doi:
            raise ValueError("Provider DOI does not match requested DOI")
        result.update(compare_reference(row, record))
    except HTTPError as error:
        result.update(status="unverified", reason=f"Crossref HTTP {error.code}; no validity verdict")
    except (URLError, TimeoutError, OSError, ValueError, KeyError, TypeError) as error:
        result.update(status="unverified", reason=f"Lookup failed: {type(error).__name__}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between unique DOI lookups")
    args = parser.parse_args()
    if not math.isfinite(args.delay) or args.delay < 0:
        parser.error("--delay must be finite and nonnegative")
    if args.output.exists():
        parser.error("Output exists; choose a new report path")
    if args.output.resolve() == args.csv.resolve():
        parser.error("Input and output must differ")
    with args.csv.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or "doi" not in reader.fieldnames:
            parser.error("CSV needs a lowercase doi column")
        rows = list(reader)
    cache = {}

    def cached_fetch(doi):
        if doi not in cache:
            if cache:
                time.sleep(args.delay)
            cache[doi] = fetch_crossref(doi)
        return cache[doi]

    results = [verify_row(row, cached_fetch) for row in rows]
    payload = {"tool": "KiteSkill DOI metadata verifier", "scope": "Crossref metadata only",
               "not_checked": ["claim support", "full author-order validation", "retractions", "study validity"],
               "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
    counts = {status: sum(r["status"] == status for r in results)
              for status in sorted({r["status"] for r in results})}
    print(json.dumps({"output": str(args.output), "rows": len(rows), "statuses": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
