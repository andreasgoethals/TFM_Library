#!/usr/bin/env python
"""Extract a paper PDF's full text into ``papers/text/<year>/<same-name>.txt``.

Step 2 of the add-a-paper procedure (see AGENTS.md). The text extractions
let agents grep/read papers without PDF tooling, so every PDF under
``papers/<year>/`` must have one.

Layout (mirrored, year folder for year folder)::

    papers/2026/06_Kong_and_Das_Introducing_TabFM.pdf
    papers/text/2026/06_Kong_and_Das_Introducing_TabFM.txt

Usage (from the library root)::

    python scripts/extract_paper_text.py papers/2026/06_Author_et_al._Title.pdf
    python scripts/extract_paper_text.py --all      # fill in any missing ones
    python scripts/extract_paper_text.py --check    # report gaps, write nothing

Requires ``pypdf`` (``pip install -r requirements.txt``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_PAPERS = _ROOT / "papers"
_TEXT = _PAPERS / "text"


def text_path_for(pdf: Path) -> Path:
    """Mirror ``papers/<year>/<name>.pdf`` to ``papers/text/<year>/<name>.txt``.

    The year is taken from the PDF's parent directory, which is the single
    source of truth for a paper's year in this repository.
    """
    pdf = pdf.resolve()
    year = pdf.parent.name
    if not (len(year) == 4 and year.isdigit()):
        raise SystemExit(
            f"expected papers/<year>/<file>.pdf, got: {pdf.relative_to(_ROOT)}\n"
            f"(the parent directory must be a 4-digit year)"
        )
    return _TEXT / year / (pdf.stem + ".txt")


def iter_pdfs() -> list[Path]:
    """Every PDF under ``papers/<year>/``, chronologically."""
    return sorted(
        p for p in _PAPERS.glob("*/*.pdf") if p.parent.name != "text"
    )


def _strip_line_number_gutters(text: str, min_run: int = 8) -> str:
    """Drop the numbered margin that ICLR/NeurIPS submission templates print.

    Those templates put a line number beside every line, and pypdf emits
    them as a long run of bare integers before the page body. In the worst
    case seen here (den Breejen 2024) they were 48 % of the file, which
    makes the extraction useless to grep and skews any word counting.

    Only runs of at least ``min_run`` consecutive bare-integer lines are
    removed, so a short column of numbers inside a real table survives.
    """
    lines = text.split("\n")
    keep = [True] * len(lines)
    run: list[int] = []
    for i, line in enumerate(lines + [""]):        # sentinel flushes the tail
        if line.strip().isdigit():
            run.append(i)
            continue
        if len(run) >= min_run:
            for j in run:
                keep[j] = False
        run = []
    return "\n".join(l for l, k in zip(lines, keep) if k)


def extract(pdf: Path) -> Path:
    from pypdf import PdfReader

    out = text_path_for(pdf)
    out.parent.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(pdf))
    text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
    # Broken font maps sometimes make pypdf emit NUL and other control
    # bytes; a single NUL makes grep treat the whole file as binary,
    # defeating the point of these extractions. Strip everything below
    # 0x20 except newline and tab.
    text = "".join(ch for ch in text if ch in "\n\t" or ord(ch) >= 32)
    text = _strip_line_number_gutters(text)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"{pdf.parent.name}/{pdf.name}: {len(reader.pages)} pages, "
          f"{len(text):,} chars -> {out.relative_to(_ROOT)}")
    return out


def missing() -> list[Path]:
    return [p for p in iter_pdfs() if not text_path_for(p).exists()]


def orphans() -> list[Path]:
    """Text files with no corresponding PDF."""
    wanted = {text_path_for(p) for p in iter_pdfs()}
    return sorted(p for p in _TEXT.glob("*/*.txt") if p not in wanted)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", nargs="?", help="path to one PDF under papers/<year>/")
    ap.add_argument("--all", action="store_true",
                    help="extract every papers/<year>/*.pdf that lacks a text file")
    ap.add_argument("--check", action="store_true",
                    help="report missing/orphaned extractions and exit non-zero")
    args = ap.parse_args()

    if args.check:
        miss, orph = missing(), orphans()
        for p in miss:
            print(f"MISSING TEXT : {p.relative_to(_ROOT)}")
        for p in orph:
            print(f"ORPHAN TEXT  : {p.relative_to(_ROOT)}")
        # Quality checks. These exist because 27 of the original extractions
        # turned out to be Latin-1 with CRLF endings — i.e. produced by
        # something other than this script — which mangled every non-ASCII
        # author name and crashed any tool reading them as UTF-8.
        bad = 0
        for p in sorted(_TEXT.glob("*/*.txt")):
            raw = p.read_bytes()
            rel = p.relative_to(_ROOT)
            try:
                body = raw.decode("utf-8")
            except UnicodeDecodeError:
                print(f"NOT UTF-8    : {rel}  (re-run extraction)")
                bad += 1
                continue
            if b"\r\n" in raw:
                print(f"CRLF ENDINGS : {rel}  (.gitattributes wants LF)")
                bad += 1
            if any(b < 9 or b == 11 or 13 < b < 32 for b in raw):
                print(f"CONTROL BYTES: {rel}  (breaks grep)")
                bad += 1
            run = longest = 0
            for line in body.split("\n"):
                run = run + 1 if line.strip().isdigit() else 0
                longest = max(longest, run)
            if longest >= 8:
                print(f"LINE GUTTER  : {rel}  ({longest} bare-integer lines)")
                bad += 1
        total = len(iter_pdfs())
        print(f"{total} PDFs, {total - len(miss)} extracted, "
              f"{len(miss)} missing, {len(orph)} orphaned, "
              f"{bad} quality issue(s)")
        return 1 if (miss or orph or bad) else 0

    if args.all:
        miss = missing()
        if not miss:
            print("all PDFs already have text extractions")
            return 0
        for p in miss:
            extract(p)
        return 0

    if not args.pdf:
        ap.error("give a PDF path, --all, or --check")
    pdf = Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"not found: {pdf}")
    extract(pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
