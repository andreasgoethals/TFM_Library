#!/usr/bin/env python
"""File a new paper: the mechanical half of the add-a-paper procedure.

AGENTS.md rule 3 lists five steps. Three of them are pure bookkeeping and
are where the mistakes happen — a month prefix off by one, a name that
does not ASCII-fold, an entry inserted in the wrong chronological slot, a
forgotten timeline row. This script does those, and only those:

===  ===========================================================  =========
1.   File the PDF as ``papers/<year>/<MM>_Author_et_al._Title.pdf``  automated
2.   Extract text to ``papers/text/<year>/<same>.txt``               automated
3.   ``SUMMARIES.md`` entry + overview row                           scaffolded
4.   ``SYNTHESIS.md`` timeline row + appendix card                   scaffolded
5.   ``CHANGELOG.md`` line                                           scaffolded
===  ===========================================================  =========

"Scaffolded" means the script inserts a **placeholder** at the correct
position — the right chronological slot, the right table, the right
anchor — with the prose left as ``TODO(new-paper)``. It deliberately does
not write the prose: judging where a paper fits in the field is the
actual work, and a plausible-sounding auto-summary would be worse than an
empty one because nobody would notice it was never written. Every
placeholder is loud, and ``check_docs.py`` fails while any remains, so a
half-finished paper cannot be committed by accident.

Metadata comes from the arXiv API when the PDF carries an arXiv stamp,
otherwise from the PDF's own metadata and first page — both are guesses,
so the proposed filename is always shown for confirmation and every
field can be overridden.

Usage::

    python scripts/papers/new_paper.py ~/Downloads/2607.27546v1.pdf
    python scripts/papers/new_paper.py paper.pdf --title "TabX" --month 03
    python scripts/papers/new_paper.py paper.pdf --dry-run   # decide nothing
    python scripts/papers/new_paper.py paper.pdf --no-scaffold  # file only

Exit code 0 on success.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import shutil
import sys
import time as _time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.library import (  # noqa: E402
    CHANGELOG, MONTHS, PAPERS, SUMMARIES, SYNTHESIS,
    _ARXIV_STAMP, ascii_fold, house_filename,
)

TODO = "TODO(new-paper)"

_ARXIV_ANY = re.compile(r"arXiv[:\s]\s*(\d{4}\.\d{4,5})", re.I)
_ARXIV_API = "http://export.arxiv.org/api/query?id_list={ids}"
_ATOM = "{http://www.w3.org/2005/Atom}"
_UA = "tfm-library-maintenance/1.0"


@dataclass
class Meta:
    title: str
    authors: list[str]
    year: str
    month: str
    arxiv: str | None = None
    source: str = "?"

    @property
    def date(self) -> str:
        return f"{self.year}-{self.month}"

    @property
    def cite(self) -> str:
        """``Luo et al.`` — how the authors are named in prose."""
        if not self.authors:
            return TODO
        last = [a.split()[-1] for a in self.authors]
        if len(last) == 1:
            return last[0]
        if len(last) == 2:
            return f"{last[0]} and {last[1]}"
        return f"{last[0]} et al."

    @property
    def filename(self) -> str:
        return house_filename([a.split()[-1] for a in self.authors],
                              self.month, self.title)


# --------------------------------------------------------------------------
# metadata
# --------------------------------------------------------------------------

def pdf_text(pdf: Path, pages: int = 2) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf is required:  pip install -r requirements.txt")
    reader = PdfReader(str(pdf))
    return "\n".join((p.extract_text() or "") for p in reader.pages[:pages])


def from_arxiv(arxiv_id: str) -> Meta | None:
    url = _ARXIV_API.format(ids=arxiv_id)
    root = None
    # arXiv throttles hard and returns 429 rather than queueing, so a
    # single attempt fails often enough to be worth retrying: the fallback
    # (PDF metadata) guesses the *current month* for the date, which is
    # wrong for anything but a paper filed the week it appeared.
    for attempt, wait in enumerate((5, 15, 40)):
        req = urllib.request.Request(url, headers={"User-Agent": _UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                root = ET.fromstring(r.read())
            break
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 2:
                return None
            print(f"  arXiv API rate-limited; retrying in {wait}s")
            _time.sleep(wait)
        except (urllib.error.URLError, ET.ParseError, TimeoutError):
            return None
    if root is None:
        return None
    entry = root.find(f"{_ATOM}entry")
    if entry is None:
        return None
    title = " ".join((entry.findtext(f"{_ATOM}title") or "").split())
    authors = [" ".join((a.findtext(f"{_ATOM}name") or "").split())
               for a in entry.findall(f"{_ATOM}author")]
    # `updated` is the version on disk; `published` is v1. A re-filed v3
    # belongs in the folder of the version we actually hold.
    stamp = (entry.findtext(f"{_ATOM}updated")
             or entry.findtext(f"{_ATOM}published") or "")[:7]
    if not re.match(r"20\d\d-\d\d", stamp):
        return None
    return Meta(title=title, authors=authors, year=stamp[:4],
                month=stamp[5:7], arxiv=arxiv_id, source="arXiv API")


def from_pdf(pdf: Path) -> Meta:
    """Last-resort guess: PDF metadata, then the first non-empty text line."""
    try:
        from pypdf import PdfReader
        info = PdfReader(str(pdf)).metadata or {}
    except Exception:
        info = {}
    body = pdf_text(pdf, 1)
    title = " ".join(str(info.get("/Title") or "").split())
    author = str(info.get("/Author") or "")
    if not title or len(title) < 8 or title.lower().endswith(".dvi"):
        head = [l.strip() for l in body.splitlines() if l.strip()]
        title = next((l for l in head if len(l) > 12 and not l.startswith("arXiv")),
                     TODO)
    authors = [a.strip() for a in re.split(r",| and |;", author) if a.strip()]

    # The arXiv banner down the left margin carries the version's own date
    # ("arXiv:2607.27546v1 [cs.LG] 30 Jul 2026"). That is the date this
    # paper should be filed under, and it is right there in the PDF — far
    # better than today's date when the API is unreachable.
    stamp = _ARXIV_STAMP.search(body)
    if stamp:
        _, _, _, mon, year = stamp.groups()
        return Meta(title=title, authors=authors, year=year,
                    month=f"{MONTHS[mon]:02d}", source="PDF + arXiv banner")
    today = _dt.date.today()
    return Meta(title=title, authors=authors, year=str(today.year),
                month=f"{today.month:02d}", source="PDF metadata (unreliable)")


def resolve(pdf: Path, args: argparse.Namespace) -> Meta:
    meta: Meta | None = None
    aid = args.arxiv
    if not aid:
        m = _ARXIV_ANY.search(pdf_text(pdf))
        aid = m.group(1) if m else None
    if aid:
        meta = from_arxiv(aid)
        if meta is None:
            print(f"  arXiv:{aid} found in the PDF but the API did not answer;"
                  " falling back to PDF metadata")
    if meta is None:
        meta = from_pdf(pdf)
        meta.arxiv = aid
    if args.title:
        meta.title = args.title
    if args.authors:
        meta.authors = [a.strip() for a in args.authors.split(",") if a.strip()]
    if args.year:
        meta.year = args.year
    if args.month:
        meta.month = f"{int(args.month):02d}"
    return meta


# --------------------------------------------------------------------------
# scaffolding: insert placeholders at the right chronological position
# --------------------------------------------------------------------------

def _anchor(meta: Meta) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_fold(meta.title).lower()).strip("-")
    return "-".join(slug.split("-")[:3])


def _insert_sorted_line(lines: list[str], new: str, date: str,
                        pattern: str) -> list[str]:
    """Put ``new`` among the lines matching ``pattern``, keeping date order."""
    idx = [i for i, l in enumerate(lines) if re.match(pattern, l)]
    if not idx:
        return lines
    for i in idx:
        if (re.match(pattern, lines[i]).group(1)) > date:
            return lines[:i] + [new] + lines[i:]
    return lines[:idx[-1] + 1] + [new] + lines[idx[-1] + 1:]


def scaffold_summaries(meta: Meta, rel_pdf: str) -> str:
    text = SUMMARIES.read_text(encoding="utf-8")
    a = _anchor(meta)

    row = (f"| {meta.date} | {meta.cite} | {meta.title} | {TODO}: one-line "
           f"contribution. | [pdf]({rel_pdf}) |")
    lines = _insert_sorted_line(text.split("\n"), row, meta.date,
                                r"^\| (20\d\d-\d\d) \|")
    text = "\n".join(lines)

    ident = (f"**arXiv:** [{meta.arxiv}](https://arxiv.org/abs/{meta.arxiv})"
             if meta.arxiv else f"**Venue:** {TODO}")
    entry = (
        f'<a id="{a}"></a>\n\n'
        f"## {meta.date} — {meta.cite} — {meta.title}\n\n"
        f"{ident} · {TODO}: venue · {TODO}: affiliation ·\n"
        f"**PDF:** [open]({rel_pdf})\n\n"
        f"**Where it fits.** {TODO} — which paper(s) in this library does it\n"
        f"answer, extend or contradict? Link them by anchor.\n\n"
        f"**What it contains.** {TODO} — method, setup, headline numbers.\n\n"
        f"**Strengths.** {TODO}\n\n"
        f"**Limitations.** {TODO}\n\n"
        f"---\n"
    )
    heads = list(re.finditer(r"^## (20\d\d-\d\d) — ", text, re.M))
    later = [h for h in heads if h.group(1) > meta.date]
    if later:
        at = later[0].start()
        # keep an explicit anchor immediately above its heading
        pre = text.rfind('<a id="', 0, at)
        if pre != -1 and text[pre:at].strip().startswith('<a id="') \
                and "\n\n" not in text[text.index("\n", pre):at].strip():
            at = pre
        text = text[:at] + entry + "\n" + text[at:]
    elif heads:
        end = len(text)
        text = text[:end].rstrip("\n") + "\n\n" + entry
    SUMMARIES.write_text(text, encoding="utf-8", newline="\n")
    return a


def scaffold_synthesis(meta: Meta) -> None:
    text = SYNTHESIS.read_text(encoding="utf-8")
    short = f"{meta.cite.split()[0]} {meta.year}"

    row = f"| {meta.date} | {short} | {TODO}: what it establishes | {TODO} |"
    text = "\n".join(_insert_sorted_line(text.split("\n"), row, meta.date,
                                         r"^\| (20\d\d-\d\d) \|"))

    card = (f"**{meta.cite} {meta.date} — {meta.title}.** {TODO} — one line of\n"
            f"framing. *Method:* {TODO} *Strength:* {TODO} *Weakness:* {TODO}\n")
    cards = list(re.finditer(r"^\*\*[^*]*?(20\d\d-\d\d)", text, re.M))
    later = [c for c in cards if c.group(1) > meta.date]
    if later:
        at = later[0].start()
        text = text[:at] + card + "\n" + text[at:]
    elif cards:
        c = cards[-1]
        nxt = text.find("\n\n", c.end())
        end = text.find("\n## ", c.end())
        at = len(text) if end == -1 else end
        para_end = text.rfind("\n\n", 0, at) + 2 if nxt != -1 else at
        text = text[:para_end] + card + "\n" + text[para_end:]
    SYNTHESIS.write_text(text, encoding="utf-8", newline="\n")


def scaffold_changelog(meta: Meta) -> None:
    text = CHANGELOG.read_text(encoding="utf-8")
    today = _dt.date.today().isoformat()
    line = (f"- Added **{meta.cite} {meta.date} — {meta.title}**"
            f"{f' (arXiv {meta.arxiv})' if meta.arxiv else ''}. {TODO}: why it\n"
            f"  matters and what it changes in the synthesis.\n")
    if f"## {today}" in text:
        at = text.index(f"## {today}")
        at = text.index("\n", at) + 1
        while text[at] == "\n":
            at += 1
        text = text[:at] + line + text[at:]
    else:
        first = re.search(r"^## \d{4}-\d{2}-\d{2}", text, re.M)
        at = first.start() if first else len(text)
        text = text[:at] + f"## {today}\n\n{line}\n" + text[at:]
    CHANGELOG.write_text(text, encoding="utf-8", newline="\n")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdf", help="the downloaded PDF, from anywhere on disk")
    ap.add_argument("--title"), ap.add_argument("--arxiv", metavar="ID")
    ap.add_argument("--authors", metavar='"A Name, B Name"',
                    help="comma-separated, full names or surnames")
    ap.add_argument("--year", metavar="YYYY"), ap.add_argument("--month", metavar="MM")
    ap.add_argument("--move", action="store_true",
                    help="move the source PDF instead of copying it")
    ap.add_argument("--no-scaffold", action="store_true",
                    help="file and extract only; touch no document")
    ap.add_argument("--dry-run", action="store_true",
                    help="show the plan and change nothing")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation")
    args = ap.parse_args(argv)

    src = Path(args.pdf).expanduser()
    if not src.is_file():
        sys.exit(f"not found: {src}")

    meta = resolve(src, args)
    dest = PAPERS / meta.year / meta.filename
    rel = f"papers/{meta.year}/{meta.filename}"

    bar = "=" * 78
    print(bar)
    print("  New paper")
    print(bar)
    print(f"  metadata from : {meta.source}")
    print(f"  title         : {meta.title}")
    print(f"  authors       : {', '.join(meta.authors) or TODO}  -> {meta.cite}")
    stamped = meta.source in ("arXiv API", "PDF + arXiv banner")
    print(f"  date          : {meta.date}"
          f"{'   (arXiv version stamp)' if stamped else '   <- GUESSED: this'}"
          f"{'' if stamped else ' is todays month, not the papers'}")
    print(f"  arXiv         : {meta.arxiv or '-'}")
    print(f"  destination   : {rel}")
    print(bar)
    if TODO in (meta.title, meta.cite):
        print("  Some fields could not be determined. Re-run with --title /")
        print("  --authors / --year / --month rather than fixing it afterwards:")
        print("  the filename is what every document links to.")
    if dest.exists():
        print(f"  ALREADY FILED: {rel} exists. Nothing to do.")
        return 1
    if args.dry_run:
        print("  Dry run — nothing written.")
        return 0
    if not args.yes:
        if not sys.stdin.isatty():
            print("  Non-interactive: re-run with --yes to accept this plan.")
            return 2
        if input("  File it under this name? [y/N] ").strip().lower() != "y":
            return 2

    # ---- step 1: file the PDF -------------------------------------------
    dest.parent.mkdir(parents=True, exist_ok=True)
    (shutil.move if args.move else shutil.copy2)(str(src), str(dest))
    print(f"\n  [1/5] filed      {rel}")

    # ---- step 2: extract text -------------------------------------------
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from extract_paper_text import extract        # noqa: PLC0415
    print("  [2/5] extracting ", end="")
    extract(dest)

    if args.no_scaffold:
        print("\n  Documents untouched (--no-scaffold). Steps 3-5 are yours.")
        return 0

    # ---- steps 3-5: placeholders in the right places ---------------------
    anchor = scaffold_summaries(meta, rel)
    print(f"  [3/5] SUMMARIES.md   entry + overview row  (anchor #{anchor})")
    scaffold_synthesis(meta)
    print("  [4/5] SYNTHESIS.md   timeline row + appendix card")
    scaffold_changelog(meta)
    print("  [5/5] CHANGELOG.md   one line")

    print(f"\n{bar}")
    print(f"  Now write the prose. Every placeholder reads {TODO};")
    print("  check_docs.py fails while any of them survives, so nothing")
    print("  half-finished can be committed by accident:")
    print()
    print("      python scripts/checks/check_docs.py")
    print()
    print("  Read the neighbouring entries first — the house style is")
    print("  venue -> where it fits -> what it contains -> strengths ->")
    print("  limitations, and 'where it fits' must link existing papers.")
    print(bar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
