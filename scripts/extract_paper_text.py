#!/usr/bin/env python
"""Extract a paper PDF's full text into ``papers/text/<same-basename>.txt``.

Step 2 of the add-a-paper procedure (see AGENTS.md §4). The text extractions
let agents grep/read papers without PDF tooling, so every PDF in ``papers/``
must have one.

Usage (from the library root)::

    python scripts/extract_paper_text.py papers/2026_Author_et_al._Title.pdf
    python scripts/extract_paper_text.py --all      # fill in any missing ones

Requires ``pypdf`` (``pip install pypdf``).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]


def extract(pdf: Path) -> Path:
    from pypdf import PdfReader

    out_dir = _ROOT / "papers" / "text"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (pdf.stem + ".txt")
    reader = PdfReader(str(pdf))
    text = "\n\n".join((page.extract_text() or "") for page in reader.pages)
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"{pdf.name}: {len(reader.pages)} pages, {len(text):,} chars -> {out.relative_to(_ROOT)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", nargs="?", help="path to one PDF under papers/")
    ap.add_argument("--all", action="store_true",
                    help="extract every papers/*.pdf that lacks a text file")
    args = ap.parse_args()

    if args.all:
        missing = [p for p in sorted((_ROOT / "papers").glob("*.pdf"))
                   if not (_ROOT / "papers" / "text" / (p.stem + ".txt")).exists()]
        if not missing:
            print("all PDFs already have text extractions")
            return 0
        for p in missing:
            extract(p)
        return 0

    if not args.pdf:
        ap.error("give a PDF path or --all")
    pdf = Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"not found: {pdf}")
    extract(pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
