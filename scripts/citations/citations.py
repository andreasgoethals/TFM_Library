#!/usr/bin/env python
"""How often is each paper in this library cited — and is that growing?

A citation count is a snapshot of attention. A *series* of snapshots is
the interesting thing: it shows which papers the field keeps returning to
and which ones landed once and went quiet. So this script does not just
report today's numbers, it **appends** them to ``data/citations.csv``,
which is tracked in git. Every run adds one row per paper per source and
never rewrites history, so the file grows into a record you can plot.

Where the numbers come from
---------------------------
========================  ====================================================
``openalex``   (default)  Open API, no key, no rate-limit problems. Counts
                          are conservative: they miss citations from venues
                          OpenAlex has not indexed.
``semanticscholar``       Open API, no key. Merges the arXiv preprint and
     (default)            the published version, so counts are usually the
                          highest of the two open sources.
``scholar``   (opt-in)    Google Scholar via ``scholarly``. The number
                          everyone quotes, and by far the most complete —
                          but scraping it is against Google's terms of
                          service and gets your IP blocked with a CAPTCHA
                          after a few dozen queries. Never runs unless you
                          ask for it and confirm.
========================  ====================================================

Each source is stored as its own row rather than merged into one number,
because they disagree by a factor of two or more and averaging them would
hide that. Compare a paper against itself over time within one source.

How a paper is matched
----------------------
By DOI if the summary entry has one, else by arXiv ID, else by a title
search whose result must pass a similarity threshold. The matched record's
id and title are stored in the CSV alongside the count, so a wrong match
is visible instead of silently poisoning a series. Papers that cannot be
matched at all (a blog post with no indexed record) are reported and
skipped, not written as zero — zero is a real citation count and would be
a lie here.

Usage::

    python scripts/citations/citations.py                  # snapshot + append
    python scripts/citations/citations.py --dry-run        # look, write nothing
    python scripts/citations/citations.py --only TabICL    # one paper
    python scripts/citations/citations.py --source scholar # add Google Scholar
    python scripts/citations/citations.py --report         # read the CSV only

The companion notebook ``Citations.ipynb`` reads the same CSV and plots
the evolution. Standard library only, so it runs without pandas.

Exit code 0 unless every paper failed to resolve.
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import difflib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import (  # noqa: E402
    DATA, ascii_fold, iter_papers, summaries_entries,
)

CSV_PATH = DATA / "citations.csv"
COLUMNS = ["date", "paper", "source", "citations", "match",
           "matched_id", "matched_title"]

DEFAULT_SOURCES = ("openalex", "semanticscholar")
ALL_SOURCES = ("openalex", "semanticscholar", "scholar")

# OpenAlex asks for a contact address in return for the fast "polite pool".
MAILTO = "andreas.goethals@kuleuven.be"
_UA = "tfm-library-maintenance/1.0 (+https://github.com/andreasgoethals/TFM_Library)"

_OPENALEX = "https://api.openalex.org/works"
_S2 = "https://api.semanticscholar.org/graph/v1/paper"

# a title match below this is treated as "not found" rather than guessed
TITLE_THRESHOLD = 0.82

# strips the author segment from `MM_Author_et_al._Title.pdf`.
# `[^_]` not `\w`: `\w` matches the underscore too, so a greedy `\w*` would
# swallow the whole filename and leave only the last word of the title.
_AUTHOR_SEG = re.compile(r"^[A-Z][^_]*(?:_et_al\.|_and_[A-Z][^_]*)?_")


# --------------------------------------------------------------------------
# what we are looking up
# --------------------------------------------------------------------------

@dataclass
class Target:
    """One paper, with everything needed to find it in a citation index."""
    key: str            # 2026-05_Bouadi_et_al._Shaping_the_Prior
    date: str           # 2026-05
    title: str          # Shaping the Prior How Synthetic Task Distributions…
    arxiv: str | None
    doi: str | None

    @property
    def months_old(self) -> int:
        y, m = (int(x) for x in self.date.split("-"))
        today = _dt.date.today()
        return max(1, (today.year - y) * 12 + today.month - m)


def _filename_title(stem: str, heading_authors: str) -> str:
    """Recover the paper title from `MM_Author_et_al._Title`.

    The filename is the most faithful copy of the title we hold (the
    SUMMARIES heading often carries a nickname and a parenthetical), so
    strip the author segment and turn underscores back into spaces.
    """
    body = stem[3:]
    if heading_authors:
        seg = _clean_for_filename(heading_authors)
        if body.startswith(seg + "_"):
            return body[len(seg) + 1:].replace("_", " ")
    m = _AUTHOR_SEG.match(body)          # fallback: pattern-match the segment
    if m and len(body) > m.end() + 8:
        body = body[m.end():]
    return body.replace("_", " ")


def _clean_for_filename(authors: str) -> str:
    """`den Breejen et al.` -> `Breejen_et_al.`, mirroring the naming rule."""
    s = ascii_fold(authors).replace("&", "and")
    s = re.sub(r"[,?!:;'\"()\[\]]", "", s)
    s = re.sub(r"[-–—/\s]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)


def targets(only: str | None = None) -> list[Target]:
    """Every paper in the library, paired with its identifiers."""
    entries = summaries_entries()
    out: list[Target] = []
    for p in iter_papers():
        e = entries.get(p.key, {})
        heading = e.get("heading", "")
        authors = heading.split("—")[0].strip() if "—" in heading else ""
        t = Target(
            key=p.key,
            date=p.date,
            title=_filename_title(p.stem, authors),
            arxiv=e.get("arxiv"),
            doi=e.get("doi"),
        )
        if only and only.lower() not in t.key.lower() and \
                only.lower() not in t.title.lower():
            continue
        out.append(t)
    return out


@dataclass
class Hit:
    source: str
    citations: int
    match: str          # doi | arxiv | title
    matched_id: str
    matched_title: str


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

# Semantic Scholar's unauthenticated pool is shared across all anonymous
# callers worldwide, so 429 is routine rather than a sign of abuse by us.
# Counting them lets the run distinguish "the index does not have this
# paper" from "we were throttled", which are opposite conclusions.
_BACKOFF = (5, 15, 40)
_THROTTLED: dict[str, int] = {}


def _get_json(url: str, *, tries: int = 4, timeout: int = 30) -> dict | None:
    """GET some JSON, backing off politely on rate limits and 5xx."""
    host = urllib.parse.urlsplit(url).netloc
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None                      # a real "not indexed"
            if exc.code == 429:
                _THROTTLED[host] = _THROTTLED.get(host, 0) + 1
            if exc.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(_BACKOFF[min(attempt, len(_BACKOFF) - 1)])
                continue
            return None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt < tries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            return None
    return None


def _similar(a: str, b: str) -> float:
    def norm(s: str) -> str:
        return re.sub(r"[^a-z0-9 ]", "", ascii_fold(s).lower()).strip()
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


# --------------------------------------------------------------------------
# sources
# --------------------------------------------------------------------------

def lookup_openalex(t: Target) -> Hit | None:
    def hit(work: dict, how: str) -> Hit:
        return Hit("openalex", int(work.get("cited_by_count") or 0), how,
                   (work.get("id") or "").rsplit("/", 1)[-1],
                   work.get("title") or work.get("display_name") or "")

    suffix = f"?mailto={MAILTO}"
    if t.doi:
        w = _get_json(f"{_OPENALEX}/doi:{urllib.parse.quote(t.doi)}{suffix}")
        if w:
            return hit(w, "doi")
    if t.arxiv:
        # OpenAlex indexes arXiv preprints under their DataCite DOI
        w = _get_json(f"{_OPENALEX}/doi:10.48550/arXiv.{t.arxiv}{suffix}")
        if w:
            return hit(w, "arxiv")
    q = urllib.parse.quote(t.title)
    r = _get_json(f"{_OPENALEX}?filter=title.search:{q}&per-page=5&mailto={MAILTO}")
    for w in (r or {}).get("results", []):
        name = w.get("title") or w.get("display_name") or ""
        if _similar(name, t.title) >= TITLE_THRESHOLD:
            return hit(w, "title")
    return None


def lookup_semanticscholar(t: Target) -> Hit | None:
    fields = "title,citationCount,externalIds,year"

    def hit(p: dict, how: str) -> Hit:
        return Hit("semanticscholar", int(p.get("citationCount") or 0), how,
                   p.get("paperId") or "", p.get("title") or "")

    if t.doi:
        p = _get_json(f"{_S2}/DOI:{urllib.parse.quote(t.doi)}?fields={fields}")
        if p:
            return hit(p, "doi")
    if t.arxiv:
        p = _get_json(f"{_S2}/arXiv:{t.arxiv}?fields={fields}")
        if p:
            return hit(p, "arxiv")
    q = urllib.parse.quote(t.title)
    r = _get_json(f"{_S2}/search?query={q}&limit=5&fields={fields}")
    for p in (r or {}).get("data", []):
        if _similar(p.get("title") or "", t.title) >= TITLE_THRESHOLD:
            return hit(p, "title")
    return None


def lookup_scholar(t: Target) -> Hit | None:
    """Google Scholar via ``scholarly`` — opt-in, see the module docstring."""
    try:
        from scholarly import scholarly       # noqa: PLC0415  (optional dep)
    except ImportError:
        print("    scholarly is not installed:  pip install scholarly",
              file=sys.stderr)
        return None
    try:
        for pub in scholarly.search_pubs(t.title):
            bib = pub.get("bib", {})
            name = bib.get("title", "")
            if _similar(name, t.title) >= TITLE_THRESHOLD:
                return Hit("scholar", int(pub.get("num_citations") or 0),
                           "title", str(pub.get("author_id") or
                                        pub.get("pub_url") or ""), name)
            break                              # only the top result is checked
    except Exception as exc:                   # scholarly raises many types
        print(f"    Google Scholar refused: {type(exc).__name__}: "
              f"{str(exc)[:80]}", file=sys.stderr)
    return None


LOOKUPS = {
    "openalex": lookup_openalex,
    "semanticscholar": lookup_semanticscholar,
    "scholar": lookup_scholar,
}


# --------------------------------------------------------------------------
# snapshot + storage
# --------------------------------------------------------------------------

def snapshot(sources: tuple[str, ...] = DEFAULT_SOURCES,
             only: str | None = None,
             date: str | None = None,
             pause: float = 1.0,
             verbose: bool = True) -> tuple[list[dict], list[str]]:
    """Query every source for every paper. Returns ``(rows, unresolved)``."""
    day = date or _dt.date.today().isoformat()
    rows: list[dict] = []
    unresolved: list[str] = []
    tg = targets(only)
    for i, t in enumerate(tg, 1):
        got = []
        for src in sources:
            h = LOOKUPS[src](t)
            if h is not None:
                rows.append({"date": day, "paper": t.key, "source": h.source,
                             "citations": h.citations, "match": h.match,
                             "matched_id": h.matched_id,
                             "matched_title": h.matched_title})
                got.append(f"{src[:4]}={h.citations}")
            time.sleep(pause)                  # be a good API citizen
        if not got:
            unresolved.append(t.key)
        if verbose:
            status = ", ".join(got) if got else "NOT FOUND"
            print(f"  [{i:2d}/{len(tg)}] {t.date}  {t.title[:44]:<44}  {status}",
                  flush=True)
    return rows, unresolved


def append_rows(rows: list[dict], path: Path = CSV_PATH) -> int:
    """Append to the CSV, creating it with a header if needed.

    Rows for a (date, paper, source) already present are dropped, so
    re-running on the same day is idempotent rather than duplicating.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_history(path)
    seen = {(r["date"], r["paper"], r["source"]) for r in existing}
    fresh = [r for r in rows if (r["date"], r["paper"], r["source"]) not in seen]
    new_file = not path.is_file()
    with path.open("a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        if new_file:
            w.writeheader()
        for r in fresh:
            w.writerow({c: r.get(c, "") for c in COLUMNS})
    return len(fresh)


def load_history(path: Path = CSV_PATH) -> list[dict]:
    """Every snapshot ever recorded, oldest first."""
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["citations"] = int(r["citations"] or 0)
    return sorted(rows, key=lambda r: (r["date"], r["paper"], r["source"]))


# --------------------------------------------------------------------------
# reading the history
# --------------------------------------------------------------------------

def series(source: str | None = None,
           path: Path = CSV_PATH) -> dict[str, list[tuple[str, int]]]:
    """``{paper: [(date, citations), …]}`` for one source.

    With no source, each paper uses the highest count available on each
    date — the most generous estimate, and stable across dates as long as
    the same sources keep running.
    """
    hist = load_history(path)
    if source:
        hist = [r for r in hist if r["source"] == source]
    best: dict[tuple[str, str], int] = {}
    for r in hist:
        k = (r["paper"], r["date"])
        best[k] = max(best.get(k, 0), r["citations"])
    out: dict[str, list[tuple[str, int]]] = {}
    for (paper, date), n in sorted(best.items()):
        out.setdefault(paper, []).append((date, n))
    return out


def growth(source: str | None = None, path: Path = CSV_PATH) -> list[dict]:
    """Per paper: first and latest count, absolute and relative change.

    ``per_month`` is the count divided by the paper's age in months — the
    one number that is comparable between a 2021 paper and a 2026 one,
    and the closest thing here to "how fast is this gaining relevance".
    """
    ser = series(source, path)
    ages = {t.key: (t.months_old, t.date, t.title) for t in targets()}
    out = []
    for paper, points in ser.items():
        first_d, first_n = points[0]
        last_d, last_n = points[-1]
        months, date, title = ages.get(paper, (1, paper[:7], paper))
        out.append({
            "paper": paper, "title": title, "published": date,
            "first_date": first_d, "first": first_n,
            "last_date": last_d, "last": last_n,
            "delta": last_n - first_n,
            "pct": (100.0 * (last_n - first_n) / first_n) if first_n else None,
            "months_old": months,
            "per_month": round(last_n / months, 1),
            "snapshots": len(points),
        })
    return sorted(out, key=lambda r: -r["last"])


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

_SCHOLAR_WARNING = """
  ------------------------------------------------------------------
  Google Scholar has no public API. Querying it means scraping, which
  violates Google's terms of service and typically ends in a CAPTCHA
  block on your IP after a few dozen queries — from this machine, for
  everything, not just this script.

  The default sources (OpenAlex + Semantic Scholar) need none of that
  and are enough to see a trend. Use Scholar only when you need the
  headline number, and rarely.
  ------------------------------------------------------------------
"""


def _print_report(source: str | None, path: Path) -> int:
    rows = growth(source, path)
    if not rows:
        print(f"  No history yet at {path}. Run without --report first.")
        return 0
    dates = sorted({d for r in rows for d in (r["first_date"], r["last_date"])})
    bar = "-" * 92
    print(bar)
    print(f"  Citations   ({len(rows)} papers, {len(dates)} snapshot date(s): "
          f"{dates[0]} .. {dates[-1]})")
    print(bar)
    print(f"  {'paper':<50} {'pub':<8} {'cites':>6} {'delta':>7} {'/month':>7}")
    print(f"  {'-' * 50} {'-' * 8} {'-' * 6} {'-' * 7} {'-' * 7}")
    for r in rows:
        delta = f"+{r['delta']}" if r["delta"] else "."
        print(f"  {r['title'][:50]:<50} {r['published']:<8} "
              f"{r['last']:>6} {delta:>7} {r['per_month']:>7}")
    print(bar)
    if len(dates) < 2:
        print("  Only one snapshot date so far — growth needs at least two.")
        print("  Run this again in a month to see movement.")
    print(f"  {path}")
    print(bar)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--source", action="append", default=[], metavar="NAME",
                    choices=list(ALL_SOURCES),
                    help=f"citation source, repeatable (default: "
                         f"{', '.join(DEFAULT_SOURCES)})")
    ap.add_argument("--only", metavar="TEXT",
                    help="restrict to papers whose key or title contains TEXT")
    ap.add_argument("--date", metavar="YYYY-MM-DD",
                    help="record under this date instead of today")
    ap.add_argument("--dry-run", action="store_true",
                    help="query and print, write nothing to the CSV")
    ap.add_argument("--report", action="store_true",
                    help="print the stored history, query nothing")
    ap.add_argument("--report-source", metavar="NAME", choices=list(ALL_SOURCES),
                    help="report on one source instead of the highest count")
    ap.add_argument("--csv", type=Path, default=CSV_PATH, metavar="PATH")
    ap.add_argument("--pause", type=float, default=1.0, metavar="SECONDS",
                    help="delay between API calls (default: 1.0)")
    ap.add_argument("--yes", action="store_true",
                    help="skip the Google Scholar confirmation prompt")
    args = ap.parse_args(argv)

    if args.report:
        return _print_report(args.report_source, args.csv)

    sources = tuple(args.source) or DEFAULT_SOURCES
    if "scholar" in sources and not args.yes:
        print(_SCHOLAR_WARNING)
        if not sys.stdin.isatty():
            print("  Refusing to scrape Scholar unattended. Re-run with --yes.")
            return 2
        if input("  Query Google Scholar anyway? [y/N] ").strip().lower() != "y":
            return 2

    bar = "=" * 92
    print(bar)
    print(f"  Citation snapshot   sources: {', '.join(sources)}"
          f"{'   (dry run)' if args.dry_run else ''}")
    print(bar)
    rows, unresolved = snapshot(sources, args.only, args.date, args.pause)

    print(bar)
    if unresolved:
        print(f"  {len(unresolved)} paper(s) not found in any source "
              f"(recorded as absent, not as zero):")
        for k in unresolved:
            print(f"    - {k}")
    if _THROTTLED:
        for host, n in sorted(_THROTTLED.items()):
            print(f"  {host} rate-limited us {n}x — some blanks above are")
            print("  throttling, not a missing paper. Re-run with a larger")
            print("  --pause, or --source openalex, to fill them in.")
    if args.dry_run:
        print(f"  Dry run: {len(rows)} row(s) would be appended to {args.csv}")
    else:
        added = append_rows(rows, args.csv)
        skipped = len(rows) - added
        print(f"  Wrote {added} row(s) to {args.csv}"
              f"{f' ({skipped} already recorded for this date)' if skipped else ''}")
        print("  Commit the CSV so the series survives — that is the point.")
    print(bar)
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
