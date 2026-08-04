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
        total = len(iter_pdfs())
        print(f"{total} PDFs, {total - len(miss)} extracted, "
              f"{len(miss)} missing, {len(orph)} orphaned")
        return 1 if (miss or orph) else 0

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
