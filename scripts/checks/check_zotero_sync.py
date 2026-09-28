#!/usr/bin/env python
"""Check this library's ``papers/`` against the mirroring Zotero collection.

Read-only on both sides. Query Zotero Desktop's live Local API, never
``zotero.sqlite``: even a database copy can lag the running application.
Nothing in Zotero or ``papers/`` is changed. Zotero must be running with
its Local API enabled; an unavailable API is an error, not a DB fallback.

What it compares
----------------
* **Presence** — every live reference in the Zotero collection should
  have a file in ``papers/<year>/``, and every file in ``papers/``
  should have a Zotero item.
* **Date** — the filed version's arXiv date vs the folder/month prefix;
  publication-date differences in Zotero are informational when the
  stored version's banner confirms the filename.
* **Metadata completeness** — items with no author (which breaks the
  filename convention) and items with neither DOI nor URL.
* **Broken links** — Zotero attachment paths that no longer resolve on
  disk.
* **Extraction parity** — PDFs with no ``papers/text/<year>/`` mirror.

The collection is selected by a unique name substring, not its numeric
prefix. Paginated API reads include all live top-level references, even
those without a PDF. Attachment paths are resolved by Zotero itself,
supporting both linked files and stored PDFs. Notes and trashed items
are excluded. The preferences helper below is retained for new_paper.py.

Usage::

    python scripts/checks/check_zotero_sync.py
    python scripts/checks/check_zotero_sync.py --collection "Foundation Models"
    python scripts/checks/check_zotero_sync.py --json

Exit code is 0 when nothing diverged, 1 for reported issues, and 2 when
the live audit could not be completed (so it can gate a maintenance run).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import MONTHS, _ARXIV_STAMP  # noqa: E402

_ROOT = Path(__file__).resolve().parents[2]
_PAPERS = _ROOT / "papers"

DEFAULT_COLLECTION = "Tabular Foundation Models"
LOCAL_API = "http://127.0.0.1:23119/api/users/0"


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
    def get(self, route: str, *, raw: bool = False):
        req = urllib.request.Request(
            LOCAL_API + route, headers={"Zotero-API-Version": "3"})
        with urllib.request.urlopen(req, timeout=30) as response:
            body = response.read().decode("utf-8")
        return body if raw else json.loads(body)

    def all(self, route: str) -> list[dict]:
        """Read every page, including collections and item children."""
        out: list[dict] = []
        start = 0
        while True:
            page = self.get(f"{route}?limit=100&start={start}")
            out.extend(page)
            if len(page) < 100:
                return out
            start += len(page)

    def collection(self, name: str) -> dict:
        matches = [c for c in self.all("/collections")
                   if name.casefold() in c["data"]["name"].casefold()]
        if len(matches) != 1:
            raise ValueError(f"expected one collection containing {name!r}; "
                             f"found {len(matches)}")
        return matches[0]

    def items(self, collection_key: str) -> list[dict]:
        return [i for i in self.all(f"/collections/{collection_key}/items/top")
                if not i["data"].get("deleted")
                and i["data"].get("itemType") not in
                ("attachment", "note", "annotation")]

    def pdfs(self, item_key: str) -> list[dict]:
        return [c for c in self.all(f"/items/{item_key}/children")
                if not c["data"].get("deleted")
                and c["data"].get("contentType") == "application/pdf"]

    def file_path(self, attachment_key: str) -> Path:
        url = self.get(f"/items/{attachment_key}/file/view/url", raw=True).strip()
        parts = urllib.parse.urlsplit(url)
        if parts.scheme != "file":
            raise ValueError(f"attachment {attachment_key} has no local file URL")
        path = (f"//{parts.netloc}" if parts.netloc else "") + parts.path
        return Path(urllib.request.url2pathname(path))


def filed_date(pdf: Path) -> tuple[str, str | None]:
    """Filename date and, if available, the exact stored arXiv version date."""
    filename_date = f"{pdf.parent.name}-{pdf.name[:2]}"
    mirror = _PAPERS / "text" / pdf.parent.name / (pdf.stem + ".txt")
    stamp = None
    if mirror.is_file():
        with mirror.open(encoding="utf-8") as stream:
            stamp = _ARXIV_STAMP.search(stream.read(16000))
    version_date = (f"{stamp.group(5)}-{MONTHS[stamp.group(4)]:02d}"
                    if stamp else None)
    return filename_date, version_date


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

    def render(self, stats: dict[str, int | str]) -> str:
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


def compare(z: ZoteroReader, collection: dict) -> tuple[dict, Report, list[str]]:
    rep = Report()
    notes: list[str] = []
    lib = library_papers()
    matched_lib: dict[str, str] = {}
    items = z.items(collection["key"])

    for item in items:
        d = item["data"]
        key = item["key"]
        title = d.get("title", "")
        label = f"{key} | {title}"
        date = item.get("meta", {}).get("parsedDate") or d.get("date", "")
        year_match = re.search(r"\b(20\d{2}|19\d{2})\b", date)
        year = year_match.group(1) if year_match else ""
        authors = [c for c in d.get("creators", [])
                   if c.get("creatorType") == "author"
                   and (c.get("lastName") or c.get("name"))]
        if not authors:
            rep.add("Zotero items with NO author", label)
        if not d.get("DOI") and not d.get("url"):
            rep.add("Zotero items with neither DOI nor URL", label)

        pdfs = z.pdfs(key)
        if not pdfs:
            rep.add("Zotero items with no PDF attachment", label)
        for attachment in pdfs:
            akey = attachment["key"]
            try:
                path = z.file_path(akey)
                if not path.is_file():
                    rep.add("Zotero attachment paths broken on disk",
                            f"{label} | attachment {akey}")
            except (urllib.error.URLError, ValueError) as exc:
                rep.add("Zotero PDF attachments unavailable",
                        f"{label} | attachment {akey}: {exc}")

        name = match_library_file(title, lib)
        if name is None:
            rep.add("In Zotero collection but NOT in papers/", label)
            continue
        if name in matched_lib:
            rep.add("Multiple Zotero items matched to one library PDF",
                    f"{matched_lib[name]} and {key} -> {name}")
        matched_lib[name] = key
        pdf = lib[name]
        filename_date, version_date = filed_date(pdf)
        if version_date:
            if filename_date != version_date:
                rep.add("Filed date disagrees with stored arXiv version",
                        f"{name}: filename {filename_date}, banner {version_date}")
            elif year and (year != version_date[:4]
                          or (re.match(r"\d{4}-\d{2}", date)
                              and date[:7] != version_date)):
                notes.append(f"{key}: Zotero date {date}; stored version "
                             f"{version_date} correctly retained ({name})")
        elif year and pdf.parent.name != year:
            rep.add("Year mismatch without an arXiv version date",
                    f"{label}: Zotero {year}, library {pdf.parent.name}")
        if not (_PAPERS / "text" / pdf.parent.name / (pdf.stem + ".txt")).is_file():
            rep.add("PDFs with no text extraction", f"{pdf.parent.name}/{name}")

    for name, path in sorted(lib.items()):
        if name not in matched_lib:
            rep.add("In papers/ but NOT in the Zotero collection",
                    f"{path.parent.name}/{name}")
    stats = {
        "Zotero collection": collection["data"]["name"],
        "source": "Zotero Desktop Local API (read-only)",
        "items in collection": len(items),
        "PDFs in papers/": len(lib),
        "matched": len(matched_lib),
    }
    return stats, rep, notes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--collection", default=DEFAULT_COLLECTION,
                    help="unique collection-name substring "
                         f"(default: {DEFAULT_COLLECTION!r})")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list-collections", action="store_true",
                    help="print every live Zotero collection name and exit")
    args = ap.parse_args(argv)
    z = ZoteroReader()
    try:
        if args.list_collections:
            for c in sorted(z.all("/collections"), key=lambda c: c["data"]["name"]):
                print(c["data"]["name"])
            return 0
        collection = z.collection(args.collection)
        stats, rep, notes = compare(z, collection)
    except (urllib.error.URLError, ValueError, OSError) as exc:
        message = (f"Cannot complete the live Zotero check: {exc}. "
                   "Zotero must be running with its Local API enabled. "
                   "No SQLite fallback was attempted.")
        if args.json:
            print(json.dumps({"error": message}, indent=2))
        else:
            print(f"ERROR: {message}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps({"stats": stats, "issues": rep.sections,
                          "version_notes": notes}, indent=2))
    else:
        print(rep.render(stats))
        if notes:
            print("  Informational publication/version date differences:")
            for note in notes:
                print(f"    - {note}")
    return 1 if rep.total else 0


if __name__ == "__main__":
    raise SystemExit(main())
