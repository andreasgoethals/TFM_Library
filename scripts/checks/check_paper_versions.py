#!/usr/bin/env python
"""Check whether newer arXiv versions exist than the PDFs on disk.

For every paper whose text extraction carries an arXiv stamp
(``arXiv:2507.03971v2 [cs.LG] 5 Jul 2025``), ask the arXiv API what the
current version is and report the ones worth re-downloading.

Deliberately **read-only**: it never downloads a PDF, never touches
``papers/``, and never edits a summary. Replacing a paper is a decision
with consequences — the year folder and month prefix may change, and
`SUMMARIES.md` may quote version-specific numbers — so it stays manual.

Papers with no arXiv stamp (journal versions, conference camera-readies,
blog posts) are listed as unverifiable rather than silently skipped.

Usage::

    python scripts/checks/check_paper_versions.py
    python scripts/checks/check_paper_versions.py --json

Requires network access. Exit code 1 if any paper is outdated.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_TEXT = _ROOT / "papers" / "text"

_API = "http://export.arxiv.org/api/query?id_list={ids}&max_results=100"
_ATOM = "{http://www.w3.org/2005/Atom}"

_STAMP = re.compile(
    r"arXiv:(\d{4}\.\d{4,5})(?:v(\d+))?\s*\[[a-zA-Z.\-]+\]\s*"
    r"(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})"
)
_MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


def local_papers() -> tuple[dict[str, dict], list[str]]:
    """Scan ``papers/text/<year>/`` for arXiv stamps.

    Returns ``({arxiv_id: {...}}, [unverifiable names])``.
    """
    found: dict[str, dict] = {}
    unverifiable: list[str] = []
    for txt in sorted(_TEXT.glob("*/*.txt")):
        body = txt.read_text(encoding="utf-8", errors="replace")
        m = _STAMP.search(body)
        rel = f"{txt.parent.name}/{txt.stem}"
        if not m:
            unverifiable.append(rel)
            continue
        aid, ver, day, mon, year = m.groups()
        found[aid] = {
            "paper": rel,
            "held_version": int(ver or 1),
            "held_date": f"{year}-{_MONTHS[mon]:02d}-{int(day):02d}",
            "folder_year": txt.parent.name,
            "month_prefix": txt.stem[:2],
        }
    return found, unverifiable


def query_arxiv(ids: list[str]) -> dict[str, dict]:
    """Ask arXiv for the current version of each id (one batched request).

    arXiv answers a busy moment with 429 rather than queueing, and this
    stage runs inside ``maintain.py`` — without a retry a transient
    throttle fails the whole sweep and says nothing about the papers.
    """
    url = _API.format(ids=",".join(ids))
    root = None
    for attempt, wait in enumerate((5, 15, 40)):
        req = urllib.request.Request(
            url, headers={"User-Agent": "tfm-library-maintenance/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                root = ET.fromstring(r.read())
            break
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 2:
                raise
            print(f"  arXiv rate-limited; retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    if root is None:
        raise urllib.error.URLError("arXiv did not answer")

    out: dict[str, dict] = {}
    for entry in root.findall(f"{_ATOM}entry"):
        raw = (entry.findtext(f"{_ATOM}id") or "").rsplit("/", 1)[-1]
        if "v" not in raw:
            continue
        base, _, ver = raw.rpartition("v")
        out[base] = {
            "latest_version": int(ver),
            "updated": (entry.findtext(f"{_ATOM}updated") or "")[:10],
            "title": " ".join((entry.findtext(f"{_ATOM}title") or "").split()),
        }
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    local, unverifiable = local_papers()
    if not local:
        print("no arXiv-stamped papers found under papers/text/", file=sys.stderr)
        return 2

    try:
        remote = query_arxiv(sorted(local))
    except (urllib.error.URLError, ET.ParseError, TimeoutError) as exc:
        print(f"ERROR: could not reach the arXiv API: {exc}", file=sys.stderr)
        return 2

    outdated, current, unknown = [], [], []
    for aid, info in sorted(local.items(), key=lambda kv: kv[1]["paper"]):
        r = remote.get(aid)
        if not r:
            unknown.append({"arxiv": aid, **info})
            continue
        row = {"arxiv": aid, **info, **r}
        (outdated if r["latest_version"] > info["held_version"]
         else current).append(row)

    if args.json:
        print(json.dumps({"outdated": outdated, "current": current,
                          "unknown": unknown,
                          "unverifiable": unverifiable}, indent=2))
        return 1 if outdated else 0

    bar = "-" * 78
    print(bar)
    print(f"  Paper version check    ({len(current)} current, "
          f"{len(outdated)} outdated, {len(unverifiable)} unverifiable)")
    print(bar)
    if outdated:
        print("\n  NEWER VERSION AVAILABLE")
        print("  " + "." * 74)
        for r in outdated:
            print(f"    - {r['paper']}")
            print(f"        held v{r['held_version']} ({r['held_date']})"
                  f"  ->  arXiv v{r['latest_version']} ({r['updated']})")
            print(f"        https://arxiv.org/abs/{r['arxiv']}")
        print("\n    Replacing a paper is manual on purpose: a new version can")
        print("    change its year folder and month prefix, and SUMMARIES.md may")
        print("    quote version-specific numbers. Re-run extract_paper_text.py")
        print("    afterwards.")
    if unknown:
        print("\n  ARXIV ID NOT RESOLVED (withdrawn, or a mis-scraped stamp)")
        print("  " + "." * 74)
        for r in unknown:
            print(f"    - {r['paper']}  (arXiv:{r['arxiv']})")
    if unverifiable:
        print("\n  NO ARXIV STAMP — cannot be version-checked automatically")
        print("  " + "." * 74)
        for name in unverifiable:
            print(f"    - {name}")
    if not outdated:
        print("\n  Every arXiv-stamped paper is at its latest version.")
    print(f"\n{bar}")
    return 1 if outdated else 0


if __name__ == "__main__":
    raise SystemExit(main())
