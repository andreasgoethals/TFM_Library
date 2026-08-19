#!/usr/bin/env python
"""Check the library's documents for internal consistency.

This is the canonical implementation of the checks that are otherwise easy
to re-derive slightly differently each time — and getting them subtly wrong
is worse than not running them. It validates:

* **Coverage.** Every PDF has a text extraction, a `SUMMARIES.md` entry, a
  `SUMMARIES.md` overview row and a `SYNTHESIS.md` timeline row — and the
  counts all agree.
* **Completeness.** Every `SUMMARIES.md` entry carries all four house
  sections: where it fits, what it contains, strengths, limitations.
* **Chronology.** Entries, rows and timeline are sorted by `YYYY-MM`, and
  the `SUMMARIES.md` table order matches the entry order.
* **Links.** Every relative link resolves to a file that exists.
* **Anchors.** Every `#fragment` resolves either to an explicit
  `<a id="...">` or to a heading, using **GitHub's** slug rules.
* **Changelog.** Sections are strictly descending by date, with no
  duplicates and no date in the future.
* **Project neutrality.** The shared documents contain no consuming
  project's name or pipeline paths (AGENTS.md rule 1).
* **No unfinished scaffolding.** `new_paper.py` inserts `TODO(new-paper)`
  placeholders at the right positions and leaves the prose to a human;
  this check is what stops a half-written entry being committed.

The anchor check deserves a note, because the naive version is wrong.
GitHub slugifies a heading by lowercasing, deleting characters that are
not word characters / spaces / hyphens, and then replacing each remaining
space with a hyphen — *without* collapsing runs. So "Timeline & lineage"
becomes ``timeline--lineage`` with two hyphens, since deleting the ``&``
leaves the spaces on either side of it. Collapsing whitespace produces
``timeline-lineage`` and reports a false failure on every heading that
contains punctuation. The rule lives in ``lib/library.py`` rather than
here, because this script having its own copy is exactly how the wrong
version got written the first time.

Usage::

    python scripts/checks/check_docs.py
    python scripts/checks/check_docs.py --quiet   # only the summary line

Exit code 0 when everything is consistent, 1 otherwise, so it composes
with ``maintain.py`` and works as a pre-commit hook.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import ROOT as _ROOT, github_slug  # noqa: E402

DOCS = ["README.md", "AGENTS.md", "SUMMARIES.md", "SYNTHESIS.md",
        "REPOSITORIES.md", "CHANGELOG.md", "PROJECT_SPECIFIC.template.md"]

# Shared documents that must not mention any consuming project.
NEUTRAL_DOCS = ["SUMMARIES.md", "SYNTHESIS.md", "REPOSITORIES.md"]
PROJECT_MARKERS = ["CreditPFN", "CreditICL"]
PROJECT_PATHS = [r"\bsrc/train\b", r"\bsrc/eval\b", r"\bsrc/data\b",
                 r"\bsrc/model\b", r"\bconfig/train\b", r"\bconfig/data\b",
                 r"\bdata/processed\b", r"\bsanitize\.py\b"]


class Report:
    def __init__(self) -> None:
        self.problems: list[str] = []
        self.notes: list[str] = []

    def fail(self, msg: str) -> None:
        self.problems.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


def check_coverage(rep: Report) -> dict[str, int]:
    pdfs = sorted(p for p in (_ROOT / "papers").glob("*/*.pdf")
                  if p.parent.name.isdigit())
    txts = sorted((_ROOT / "papers" / "text").glob("*/*.txt"))
    for p in pdfs:
        mirror = _ROOT / "papers" / "text" / p.parent.name / (p.stem + ".txt")
        if not mirror.is_file():
            rep.fail(f"no text extraction for {p.parent.name}/{p.name}")
    wanted = {(_ROOT / "papers" / "text" / p.parent.name / (p.stem + ".txt"))
              for p in pdfs}
    for t in txts:
        if t not in wanted:
            rep.fail(f"orphan extraction (no PDF): {t.parent.name}/{t.name}")

    s = (_ROOT / "SUMMARIES.md").read_text(encoding="utf-8")
    y = (_ROOT / "SYNTHESIS.md").read_text(encoding="utf-8")
    entries = re.findall(r"^## (20\d\d-\d\d) — ", s, re.M)
    rows = re.findall(r"^\| (20\d\d-\d\d) \|", s, re.M)
    timeline = re.findall(r"^\| (20\d\d-\d\d) \|", y, re.M)

    # SYNTHESIS no longer carries a per-paper appendix: it is a synthesis,
    # and the complete per-paper reference lives in SUMMARIES.md. Coverage
    # of the synthesis is therefore checked against its timeline, which is
    # the one place every paper must still appear.
    counts = {"papers": len(pdfs), "texts": len(txts),
              "SUMMARIES entries": len(entries), "SUMMARIES rows": len(rows),
              "SYNTHESIS timeline": len(timeline)}
    if len(set(counts.values())) != 1:
        rep.fail("counts disagree: "
                 + ", ".join(f"{k}={v}" for k, v in counts.items()))

    for label, seq in (("SUMMARIES entries", entries), ("SUMMARIES rows", rows),
                       ("SYNTHESIS timeline", timeline)):
        if seq != sorted(seq):
            rep.fail(f"{label} are not in chronological order")
    if rows != entries:
        rep.fail("SUMMARIES overview-table order does not match entry order")
    if sorted(timeline) != sorted(entries):
        rep.fail("SYNTHESIS timeline and SUMMARIES entries cover different papers")

    # every entry must carry the four house sections (AGENTS.md rule 3)
    heads = list(re.finditer(r"^## (20\d\d-\d\d) — (.+?)$", s, re.M))
    for i, m in enumerate(heads):
        body = s[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(s)]
        missing = [sec for sec in ("Where it fits", "What it contains",
                                   "Strengths", "Limitations")
                   if f"**{sec}" not in body]
        if missing:
            rep.fail(f"SUMMARIES.md: '{m.group(2)[:40]}' is missing "
                     f"{', '.join(missing)}")
    return counts


def check_links_and_anchors(rep: Report) -> None:
    for doc in DOCS:
        path = _ROOT / doc
        if not path.is_file():
            rep.fail(f"missing document: {doc}")
            continue
        text = path.read_text(encoding="utf-8")

        for m in re.finditer(r"\]\((?!https?://|#|mailto:)([^)#]+)\)", text):
            target = m.group(1).strip()
            if not (_ROOT / target).exists():
                rep.fail(f"{doc}: broken link -> {target}")

        ids = set(re.findall(r'<a id="([^"]+)"', text))
        slugs = {github_slug(h)
                 for h in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.M)}
        for frag in set(re.findall(r"\]\(#([^)]+)\)", text)):
            if frag not in ids and frag not in slugs:
                rep.fail(f"{doc}: unresolved anchor -> #{frag}")


def check_changelog(rep: Report) -> None:
    text = (_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    dates = re.findall(r"^## (\d{4}-\d{2}-\d{2})", text, re.M)
    if not dates:
        rep.fail("CHANGELOG.md has no dated sections")
        return
    today = datetime.date.today().isoformat()
    for d in dates:
        if d > today:
            rep.fail(f"CHANGELOG.md has a future-dated section: {d} (today is {today})")
    dupes = {d for d in dates if dates.count(d) > 1}
    if dupes:
        rep.fail(f"CHANGELOG.md has duplicate sections: {sorted(dupes)} "
                 f"(one dated section per day)")
    if dates != sorted(dates, reverse=True):
        rep.fail("CHANGELOG.md sections are not newest-first")


def check_neutrality(rep: Report) -> None:
    for doc in NEUTRAL_DOCS:
        text = (_ROOT / doc).read_text(encoding="utf-8")
        for marker in PROJECT_MARKERS:
            n = text.count(marker)
            if n:
                rep.fail(f"{doc}: mentions consuming project {marker!r} "
                         f"{n}x — shared docs must stay project-neutral "
                         f"(AGENTS.md rule 1)")
        for pat in PROJECT_PATHS:
            hits = re.findall(pat, text)
            if hits:
                rep.fail(f"{doc}: contains project pipeline path {hits[0]!r} "
                         f"— belongs in PROJECT_SPECIFIC.md")


def check_placeholders(rep: Report) -> None:
    """Fail while any `new_paper.py` scaffold is still unwritten.

    The scaffolding script puts a paper in the right chronological slot in
    four documents and leaves the prose as a marker. Without this check
    the markers would be committable, and a placeholder that nobody
    notices is worse than a missing entry — coverage counts would say the
    paper is covered.
    """
    # Only the documents the scaffolder actually writes into, and only
    # bare occurrences: the scaffolder emits the marker as plain text,
    # while README/AGENTS/CHANGELOG name it inside backticks to explain
    # the convention. Stripping code spans separates the two reliably.
    for doc in ("SUMMARIES.md", "SYNTHESIS.md", "CHANGELOG.md"):
        path = _ROOT / doc
        if not path.is_file():
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            if "TODO(new-paper)" in re.sub(r"`[^`]*`", "", line):
                rep.fail(f"{doc}:{i}: unfinished new_paper.py scaffold "
                         f"— write the entry or remove it")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quiet", action="store_true",
                    help="print only the final summary line")
    args = ap.parse_args(argv)

    rep = Report()
    counts = check_coverage(rep)
    check_links_and_anchors(rep)
    check_changelog(rep)
    check_neutrality(rep)
    check_placeholders(rep)

    bar = "-" * 78
    if not args.quiet:
        print(bar)
        print("  Document consistency check")
        print(bar)
        for k, v in counts.items():
            print(f"  {k:<22} {v}")
        print(bar)
        if rep.problems:
            for p in rep.problems:
                print(f"  [PROBLEM] {p}")
            print(bar)
    n = len(rep.problems)
    print(f"  {n} problem(s)." if n else
          "  Documents are internally consistent.")
    return 1 if n else 0


if __name__ == "__main__":
    raise SystemExit(main())
