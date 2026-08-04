#!/usr/bin/env python
"""Check this library's ``papers/`` against the mirroring Zotero collection.

Read-only on both sides. Zotero's database is **copied** before being
queried (Zotero holds a write lock while running, and opening the live
file read-write risks corruption), and nothing in ``papers/`` is moved,
renamed, or written. The script only reports; you fix things by hand.

What it compares
----------------
* **Presence** — every PDF-bearing item in the Zotero collection should
  have a file in ``papers/<year>/``, and every file in ``papers/``
  should have a Zotero item.
* **Year** — the Zotero item's year vs the ``papers/<year>/`` folder.
* **Metadata completeness** — items with no author (which breaks the
  filename convention) and items with neither DOI nor arXiv URL.
* **Broken links** — Zotero attachment paths that no longer resolve on
  disk.
* **Extraction parity** — PDFs with no ``papers/text/<year>/`` mirror.

How the Zotero side is located
------------------------------
Zotero's own preferences are the source of truth, read from
``prefs.js`` in the Zotero profile:

* ``extensions.zotero.dataDir``          -> where ``zotero.sqlite`` lives
* ``extensions.zotero.baseAttachmentPath`` -> what ``attachments:`` means

Linked attachments are stored as ``attachments:<relative/path.pdf>``,
resolved against the base attachment path. Both are auto-detected;
override with ``--data-dir`` / ``--base-path`` if needed.

Usage::

    python scripts/check_zotero_sync.py
    python scripts/check_zotero_sync.py --collection "Foundation Models"
    python scripts/check_zotero_sync.py --json

Exit code is 0 when nothing diverged, 1 otherwise (so it can gate a
maintenance run).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sqlite3
import sys
import tempfile
import unicodedata
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_PAPERS = _ROOT / "papers"

DEFAULT_COLLECTION = "Foundation Models"

# Zotero itemAttachments.linkMode values
_LINK_MODE_IMPORTED_FILE = 0
_LINK_MODE_IMPORTED_URL = 1
_LINK_MODE_LINKED_FILE = 2
_LINK_MODE_LINKED_URL = 3


# --------------------------------------------------------------------------- #
# Locating Zotero
# --------------------------------------------------------------------------- #

def _candidate_prefs() -> list[Path]:
    home = Path.home()
    return [
        home / "Zotero" / "prefs.js",
        home / "AppData" / "Roaming" / "Zotero" / "Zotero" / "Profiles",
        home / ".zotero" / "zotero",
        home / "Library" / "Application Support" / "Zotero",
    ]


def read_zotero_prefs() -> dict[str, str]:
    """Scrape ``user_pref(...)`` lines out of Zotero's prefs.js, if found."""
    prefs: dict[str, str] = {}
    pat = re.compile(r'user_pref\("([^"]+)",\s*"?([^");]*)"?\);')
    for cand in _candidate_prefs():
        files: list[Path] = []
        if cand.is_file() and cand.name == "prefs.js":
            files = [cand]
        elif cand.is_dir():
            files = list(cand.rglob("prefs.js"))
        for f in files:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in pat.finditer(text):
                if m.group(1).startswith("extensions.zotero."):
                    prefs.setdefault(m.group(1), m.group(2).replace("\\\\", "\\"))
        if prefs:
            break
    return prefs


# --------------------------------------------------------------------------- #
# Library side
# --------------------------------------------------------------------------- #

def library_papers() -> dict[str, Path]:
    """``{filename: path}`` for every PDF under ``papers/<year>/``."""
    return {
        p.name: p
        for p in _PAPERS.glob("*/*.pdf")
        if p.parent.name != "text" and p.parent.name.isdigit()
    }


def ascii_fold(s: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch)
    )


def signature(s: str) -> str:
    """Comparison key: ASCII-folded, lowercase, alphanumerics only.

    Deliberately lossy so that a Zotero title and this library's filename
    for the same paper collapse to the same string despite differing
    punctuation, author prefixes, and separator conventions.
    """
    return re.sub(r"[^a-z0-9]+", "", ascii_fold(s).lower())


def match_library_file(title: str, lib: dict[str, Path]) -> str | None:
    """Best library filename for a Zotero title, or None.

    Matching has to survive three real-world divergences: this library's
    names carry a ``MM_Author_et_al._`` prefix the Zotero title does not;
    Zotero truncates long filenames (so the stored title may be a prefix
    of the full one, or vice versa); and duplicate imports pick up a
    ``_1`` suffix. Containment handles the first two, fuzzy ratio the
    third.
    """
    import difflib

    tsig = signature(title)
    if not tsig:
        return None
    best, best_score = None, 0.0
    for name in lib:
        lsig = signature(Path(name).stem)
        if tsig in lsig:                     # exact title inside MM_Author_Title
            score = 1.0
        elif len(tsig) >= 25 and tsig[:25] in lsig:   # Zotero-side truncation
            score = 0.95
        else:
            score = difflib.SequenceMatcher(None, lsig, tsig).ratio()
        if score > best_score:
            best, best_score = name, score
    return best if best_score >= 0.80 else None


# --------------------------------------------------------------------------- #
# Zotero side
# --------------------------------------------------------------------------- #

class ZoteroReader:
    def __init__(self, sqlite_path: Path) -> None:
        # Copy first: the live DB is locked while Zotero runs.
        tmp = Path(tempfile.mkdtemp(prefix="zotero-check-")) / "zotero.sqlite"
        shutil.copy2(sqlite_path, tmp)
        self._tmp = tmp
        self.db = sqlite3.connect(f"file:{tmp}?mode=ro", uri=True)

    def close(self) -> None:
        self.db.close()
        shutil.rmtree(self._tmp.parent, ignore_errors=True)

    def collection_id(self, name: str) -> int | None:
        row = self.db.execute(
            "select collectionID from collections where collectionName=?", (name,)
        ).fetchone()
        return row[0] if row else None

    def collection_names(self) -> list[str]:
        return [r[0] for r in self.db.execute(
            "select collectionName from collections order by collectionName")]

    def field(self, item_id: int, name: str) -> str | None:
        row = self.db.execute(
            """select v.value from itemData d
                 join itemDataValues v on v.valueID = d.valueID
                 join fields f on f.fieldID = d.fieldID
                where d.itemID=? and f.fieldName=?""",
            (item_id, name),
        ).fetchone()
        return row[0] if row else None

    def creators(self, item_id: int) -> list[str]:
        return [r[0] for r in self.db.execute(
            """select c.lastName from itemCreators ic
                 join creators c on c.creatorID = ic.creatorID
                where ic.itemID=? order by ic.orderIndex""", (item_id,))]

    def items(self, collection_id: int) -> list[dict]:
        rows = self.db.execute(
            """select i.itemID, t.typeName from collectionItems ci
                 join items i on i.itemID = ci.itemID
                 join itemTypes t on t.itemTypeID = i.itemTypeID
                where ci.collectionID=?""", (collection_id,)).fetchall()
        out = []
        for item_id, type_name in rows:
            atts = self.db.execute(
                """select linkMode, path, contentType from itemAttachments
                    where parentItemID=?""", (item_id,)).fetchall()
            out.append({
                "itemID": item_id,
                "type": type_name,
                "title": self.field(item_id, "title") or "",
                "date": self.field(item_id, "date") or "",
                "doi": self.field(item_id, "DOI"),
                "url": self.field(item_id, "url"),
                "creators": self.creators(item_id),
                "attachments": atts,
            })
        return out


def author_segment(creators: list[str]) -> str:
    if not creators:
        return ""
    if len(creators) == 1:
        return creators[0]
    if len(creators) == 2:
        return f"{creators[0]} and {creators[1]}"
    return f"{creators[0]} et al."


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #

class Report:
    def __init__(self) -> None:
        self.sections: dict[str, list[str]] = {}

    def add(self, section: str, line: str) -> None:
        self.sections.setdefault(section, []).append(line)

    @property
    def total(self) -> int:
        return sum(len(v) for v in self.sections.values())

    def render(self, stats: dict[str, int]) -> str:
        bar = "-" * 78
        out = [bar, "  Zotero <-> TFM Library consistency check", bar]
        for k, v in stats.items():
            out.append(f"  {k:<44} {v}")
        out.append(bar)
        if not self.sections:
            out += ["", "  No inconsistencies found. Both sides agree.", ""]
            return "\n".join(out)
        for section, lines in self.sections.items():
            out.append("")
            out.append(f"  {section}  ({len(lines)})")
            out.append("  " + "." * 74)
            for line in lines:
                out.append(f"    - {line}")
        out += ["", bar, f"  {self.total} issue(s) to resolve by hand.", bar]
        return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--collection", default=DEFAULT_COLLECTION,
                    help=f"Zotero collection mirroring this library "
                         f"(default: {DEFAULT_COLLECTION!r})")
    ap.add_argument("--data-dir", help="Zotero data dir (contains zotero.sqlite)")
    ap.add_argument("--base-path", help="Zotero linked-attachment base directory")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list-collections", action="store_true",
                    help="print every Zotero collection name and exit")
    args = ap.parse_args(argv)

    prefs = read_zotero_prefs()
    data_dir = Path(args.data_dir or prefs.get("extensions.zotero.dataDir", ""))
    base_path = Path(args.base_path
                     or prefs.get("extensions.zotero.baseAttachmentPath", ""))

    sqlite_path = data_dir / "zotero.sqlite"
    if not sqlite_path.is_file():
        print(f"ERROR: zotero.sqlite not found at {sqlite_path}\n"
              f"       pass --data-dir explicitly.", file=sys.stderr)
        return 2

    z = ZoteroReader(sqlite_path)
    try:
        if args.list_collections:
            for n in z.collection_names():
                print(n)
            return 0

        cid = z.collection_id(args.collection)
        if cid is None:
            print(f"ERROR: no Zotero collection named {args.collection!r}.\n"
                  f"       Available: {', '.join(z.collection_names())}",
                  file=sys.stderr)
            return 2

        rep = Report()
        lib = library_papers()
        matched_lib: set[str] = set()
        items = z.items(cid)

        for it in items:
            title = it["title"]
            short = title[:62]
            year = (it["date"] or "")[:4]
            linked = [p for lm, p, _ in it["attachments"]
                      if lm == _LINK_MODE_LINKED_FILE and p
                      and p.startswith("attachments:")]
            stored_pdf = [p for lm, p, ct in it["attachments"]
                          if lm in (_LINK_MODE_IMPORTED_FILE, _LINK_MODE_IMPORTED_URL)
                          and (ct or "") == "application/pdf"]

            # --- metadata completeness -------------------------------------
            if not it["creators"]:
                rep.add("Zotero items with NO author (breaks the filename rule)",
                        f"{year} | {short}")
            if not it["doi"] and not (it["url"] or ""):
                rep.add("Zotero items with neither DOI nor URL", f"{year} | {short}")

            # --- attachment health -----------------------------------------
            if not linked:
                kind = ("PDF sits in Zotero storage, not linked to the base dir"
                        if stored_pdf else "no PDF attachment at all")
                rep.add("Zotero items with no linked PDF in the base directory",
                        f"{year} | {short}  [{kind}]")
            for rel in linked:
                relpath = rel.split(":", 1)[1]
                if not (base_path / relpath).is_file():
                    rep.add("Zotero attachment paths broken on disk",
                            f"{year} | {short}  -> {relpath}")

            # --- presence + year, independent of attachment state ----------
            name = match_library_file(title, lib)
            if name is None:
                rep.add("In Zotero collection but NOT in papers/", f"{year} | {short}")
                continue
            matched_lib.add(name)
            folder = lib[name].parent.name
            if year and folder != year:
                rep.add("Year mismatch (Zotero vs papers/<year>/)",
                        f"{short}: Zotero {year} vs library {folder}")
            if not (_PAPERS / "text" / folder / (lib[name].stem + ".txt")).is_file():
                rep.add("PDFs with no text extraction", f"{folder}/{name}")

        for name, path in sorted(lib.items()):
            if name not in matched_lib:
                rep.add("In papers/ but NOT in the Zotero collection",
                        f"{path.parent.name}/{name}")

        stats = {
            "Zotero collection": args.collection,
            "items in collection": len(items),
            "PDFs in papers/": len(lib),
            "matched": len(matched_lib),
        }

        if args.json:
            print(json.dumps({"stats": stats, "issues": rep.sections}, indent=2))
        else:
            print(rep.render(stats))
        return 1 if rep.total else 0
    finally:
        z.close()


if __name__ == "__main__":
    raise SystemExit(main())
