"""Shared helpers for the maintenance scripts.

Everything that more than one script needs to know about the shape of this
repository lives here, so the scripts cannot drift apart in how they find
papers, parse identifiers, or slugify headings.

Import it from any script, at any nesting depth::

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from lib.library import ROOT, iter_papers
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

# scripts/lib/library.py -> scripts/lib -> scripts -> <repo root>
ROOT = Path(__file__).resolve().parents[2]

PAPERS = ROOT / "papers"
TEXT = PAPERS / "text"
REPOSITORIES = ROOT / "repositories"
DATA = ROOT / "data"

SUMMARIES = ROOT / "SUMMARIES.md"
SYNTHESIS = ROOT / "SYNTHESIS.md"
REPOS_DOC = ROOT / "REPOSITORIES.md"
CHANGELOG = ROOT / "CHANGELOG.md"

_ARXIV_STAMP = re.compile(
    r"arXiv:(\d{4}\.\d{4,5})(?:v(\d+))?\s*\[[a-zA-Z.\-]+\]\s*"
    r"(\d{1,2})\s+([A-Z][a-z]{2})\s+(\d{4})"
)
MONTHS = {m: i + 1 for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}


@dataclass
class Paper:
    """One paper in the library: ``papers/<year>/<MM>_<Author>_<Title>.pdf``."""
    pdf: Path
    year: str
    month: str
    stem: str

    @property
    def key(self) -> str:
        """Stable identifier, e.g. ``2026-05_Bouadi_et_al._Shaping_the_Prior``."""
        return f"{self.year}-{self.month}_{self.stem[3:]}"

    @property
    def date(self) -> str:
        return f"{self.year}-{self.month}"

    @property
    def text_path(self) -> Path:
        return TEXT / self.year / (self.stem + ".txt")

    @property
    def rel(self) -> str:
        return f"papers/{self.year}/{self.pdf.name}"

    def text(self) -> str:
        p = self.text_path
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""

    def short(self, width: int = 52) -> str:
        return self.key[:width]


def iter_papers() -> list[Paper]:
    """Every paper, chronologically by year then month prefix."""
    out: list[Paper] = []
    for pdf in sorted(PAPERS.glob("*/*.pdf")):
        year = pdf.parent.name
        if not (len(year) == 4 and year.isdigit()):
            continue
        out.append(Paper(pdf=pdf, year=year, month=pdf.name[:2], stem=pdf.stem))
    return sorted(out, key=lambda p: (p.year, p.month, p.stem))


def held_arxiv_version(paper: Paper) -> tuple[str, int, str] | None:
    """``(arxiv_id, version, YYYY-MM-DD)`` from the extraction's arXiv stamp."""
    m = _ARXIV_STAMP.search(paper.text())
    if not m:
        return None
    aid, ver, day, mon, year = m.groups()
    return aid, int(ver or 1), f"{year}-{MONTHS[mon]:02d}-{int(day):02d}"


def summaries_entries() -> dict[str, dict]:
    """Parse ``SUMMARIES.md`` into ``{paper_key: {...}}``.

    Each entry yields its heading, the linked PDF path, and any arXiv ID or
    DOI found in the entry body — which is what the citation lookup needs.
    """
    text = SUMMARIES.read_text(encoding="utf-8")
    heads = list(re.finditer(r"^## (20\d\d-\d\d) — (.+?)$", text, re.M))
    out: dict[str, dict] = {}
    for i, m in enumerate(heads):
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        pdf = re.search(r"\]\((papers/\d{4}/[^)]+\.pdf)\)", body)
        if not pdf:
            continue
        rel = pdf.group(1)
        key = f"{Path(rel).parent.name}-{Path(rel).name[:2]}_{Path(rel).stem[3:]}"
        arxiv = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", body)
        doi = re.search(r"doi\.org/(10\.[^\s)\]]+)", body)
        out[key] = {
            "date": m.group(1),
            "heading": m.group(2).strip(),
            "pdf": rel,
            "arxiv": arxiv.group(1) if arxiv else None,
            "doi": doi.group(1).rstrip(".,") if doi else None,
            "title": _title_from_heading(m.group(2)),
        }
    return out


def _title_from_heading(heading: str) -> str:
    """``2026-05 — Bouadi et al. — O'Prior (Shaping…)`` -> ``O'Prior (Shaping…)``."""
    parts = [p.strip() for p in heading.split("—")]
    return parts[-1] if parts else heading.strip()


def github_slug(heading: str) -> str:
    """Slugify a heading the way GitHub does.

    Lowercase, delete anything that is not a word character, space or
    hyphen, then replace each remaining space with a hyphen — **without**
    collapsing runs. ``Timeline & lineage`` becomes ``timeline--lineage``
    (two hyphens), because deleting the ``&`` leaves the spaces that
    surrounded it. Collapsing whitespace here produces a false failure on
    every heading containing punctuation.
    """
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return s.replace(" ", "-")


def ascii_fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s)
                   if not unicodedata.combining(c))


def house_filename(authors: list[str], month: str, title: str) -> str:
    """Build ``MM_Author_et_al._Title.pdf`` from metadata (AGENTS.md rule 3)."""
    def clean(s: str) -> str:
        s = ascii_fold(s)
        s = re.sub(r"[,?!:;'\"()\[\]&]", "", s)
        s = re.sub(r"[-–—/\s]+", "_", s)
        return re.sub(r"_+", "_", s).strip("_").rstrip(".")

    if not authors:
        seg = ""
    elif len(authors) == 1:
        seg = clean(authors[0])
    elif len(authors) == 2:
        seg = f"{clean(authors[0])}_and_{clean(authors[1])}"
    else:
        seg = f"{clean(authors[0])}_et_al."
    return f"{month}_{seg + '_' if seg else ''}{clean(title)}.pdf"
